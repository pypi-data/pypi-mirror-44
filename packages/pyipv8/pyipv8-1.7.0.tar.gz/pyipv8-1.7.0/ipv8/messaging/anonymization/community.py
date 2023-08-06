"""
The tunnel community.

Author(s): Egbert Bouman
"""
from __future__ import absolute_import
from __future__ import division

import random
from binascii import hexlify, unhexlify

from twisted.internet.task import LoopingCall

from .caches import *
from .payload import *
from .tunnel import *
from .tunnelcrypto import CryptoException, TunnelCrypto
from ...community import Community
from ...lazy_community import lazy_wrapper, lazy_wrapper_unsigned, lazy_wrapper_unsigned_wd
from ...messaging.deprecated.encoding import decode, encode
from ...messaging.payload_headers import BinMemberAuthenticationPayload
from ...peer import Peer
from ...requestcache import RequestCache
from ...util import addCallback

message_to_payload = {
    u"data": (0, DataPayload),
    u"cell": (1, CellPayload),
    u"create": (2, CreatePayload),
    u"created": (3, CreatedPayload),
    u"extend": (4, ExtendPayload),
    u"extended": (5, ExtendedPayload),
    u"ping": (6, PingPayload),
    u"pong": (7, PongPayload),
    u"destroy": (10, DestroyPayload),
    u"establish-intro": (11, EstablishIntroPayload),
    u"intro-established": (12, IntroEstablishedPayload),
    u"key-request": (13, KeyRequestPayload),
    u"key-response": (14, KeyResponsePayload),
    u"establish-rendezvous": (15, EstablishRendezvousPayload),
    u"rendezvous-established": (16, RendezvousEstablishedPayload),
    u"create-e2e": (17, CreateE2EPayload),
    u"created-e2e": (18, CreatedE2EPayload),
    u"link-e2e": (19, LinkE2EPayload),
    u"linked-e2e": (20, LinkedE2EPayload),
    u"dht-request": (21, DHTRequestPayload),
    u"dht-response": (22, DHTResponsePayload)
}


def tc_lazy_wrapper_unsigned(*payloads):
    """
    This function wrapper will unpack just the normal payloads for you, and handle a singular circuit_id parameter at
    the end of the parameter list

    You can now write your non-authenticated and signed functions as follows:

    ::

        @tc_lazy_wrapper_unsigned(GlobalTimeDistributionPayload, IntroductionRequestPayload,
                                  IntroductionResponsePayload, circuit_id)
        def on_message(source_address, payload1, payload2):
            '''
            :type source_address: str
            :type payload1: IntroductionRequestPayload
            :type payload2: IntroductionResponsePayload
            '''
            pass
    """
    def decorator(func):
        def wrapper(self, source_address, data, circuit_id=None):

            @lazy_wrapper_unsigned(*payloads)
            def inner_wrapper(inner_self, inner_source_address, *pyls):
                combo = list(pyls) + [circuit_id]
                return func(inner_self, inner_source_address, *combo)

            return inner_wrapper(self, source_address, data)
        return wrapper
    return decorator


class TunnelSettings(object):

    def __init__(self):
        self.crypto = TunnelCrypto()

        self.min_circuits = 1
        self.max_circuits = 8
        self.max_joined_circuits = 100

        # Maximum number of seconds that a circuit should exist
        self.max_time = 10 * 60
        # Maximum number of seconds before a circuit is considered inactive (and is removed)
        self.max_time_inactive = 20
        self.max_traffic = 250 * 1024 * 1024

        self.max_packets_without_reply = 50
        self.dht_lookup_interval = 30
        # Maximum number of seconds circuit creation is allowed to take. Within this time period, the unverified hop
        # of the circuit can still change in case it is unresponsive.
        # TODO: set this to ~60s next time we change the community ID, or after enough nodes are using the newer code
        self.circuit_timeout = 10
        # Maximum number of seconds that a hop allows us to change the next hop
        self.unstable_timeout = 60
        # Maximum number of seconds adding a single hop to a circuit is allowed to take.
        self.next_hop_timeout = 10

        # We have a small delay when removing circuits/relays/exit nodes. This is to allow some post-mortem data
        # to flow over the circuit (i.e. bandwidth payouts to intermediate nodes in a circuit).
        self.remove_tunnel_delay = 5

        self.become_exitnode = False


class RoundRobin(object):

    def __init__(self, community):
        self.community = community
        self.index = -1

    def has_options(self, hops):
        return len(self.community.active_data_circuits(hops)) > 0

    def select(self, destination, hops):
        if destination and destination[1] == CIRCUIT_ID_PORT:
            circuit_id = self.community.ip_to_circuit_id(destination[0])
            circuit = self.community.circuits.get(circuit_id, None)

            if circuit and circuit.state == CIRCUIT_STATE_READY and \
               circuit.ctype == CIRCUIT_TYPE_RENDEZVOUS:
                return circuit

        circuit_ids = sorted(self.community.active_data_circuits(hops).keys())

        if not circuit_ids:
            return None

        self.index = (self.index + 1) % len(circuit_ids)
        circuit_id = circuit_ids[self.index]
        return self.community.active_data_circuits().get(circuit_id, None)


class TunnelCommunity(Community):

    version = b'\x02'
    master_peer = Peer(unhexlify("3081a7301006072a8648ce3d020106052b8104002703819200040733caf0902748547efc04be6a7e0"
                                 "64384e1939622b38cde42237eff06674e07f8c4dd364e207a8c3eee30cd5751bed76d7071e8af7b91"
                                 "0a62ccf9fbbfde7eb724a8ebdb54b738e306744ad6b96ef4549f6335c4bac10799fbe63477d8fd939"
                                 "5e8439685de72fabf3efc32f6cb28075fff6ad605891eaba161ecec2f9b65aab45e121defa47d098f"
                                 "16bad7dac6025687"))

    def __init__(self, *args, **kwargs):
        self.settings = kwargs.pop('settings', TunnelSettings())
        if isinstance(self.settings, dict):
            settings = TunnelSettings()
            for k, v in self.settings.items():
                setattr(settings, k, v)
            self.settings = settings

        super(TunnelCommunity, self).__init__(*args, **kwargs)

        self.request_cache = RequestCache()

        # Messages that can arrive from the socket
        self.decode_map.update({
            chr(1): self.on_cell,
            chr(10): self.on_destroy
        })

        # Messages that can arrive from a circuit (i.e., they are wrapped in a cell)
        self.decode_map_private = {
            chr(0): self.on_data,
            chr(2): self.on_create,
            chr(3): self.on_created,
            chr(4): self.on_extend,
            chr(5): self.on_extended,
            chr(6): self.on_ping,
            chr(7): self.on_pong
        }

        self.circuits = {}
        self.directions = {}
        self.relay_from_to = {}
        self.relay_session_keys = {}
        self.exit_sockets = {}
        self.circuits_needed = defaultdict(int)
        self.num_hops_by_downloads = defaultdict(int)  # Keeps track of the number of hops required by downloads
        self.exit_candidates = {}  # Keeps track of the candidates that want to be an exit node
        self.selection_strategy = RoundRobin(self)
        self.creation_time = time.time()

        self.crypto = self.settings.crypto

        self.logger.info("Setting become_exitnode = %s", self.settings.become_exitnode)

        self.crypto.initialize(self.my_peer.key)

        self.register_task("do_circuits", LoopingCall(self.do_circuits)).start(5, now=True)
        self.register_task("do_ping", LoopingCall(self.do_ping)).start(PING_INTERVAL)

    def become_exitnode(self):
        return self.settings.become_exitnode

    def unload(self):
        # Remove all circuits/relays/exitsockets
        for circuit_id in list(self.circuits.keys()):
            self.remove_circuit(circuit_id, 'unload', remove_now=True, destroy=True)
        for circuit_id in list(self.relay_from_to.keys()):
            self.remove_relay(circuit_id, 'unload', remove_now=True, destroy=True, both_sides=False)
        for circuit_id in list(self.exit_sockets.keys()):
            self.remove_exit_socket(circuit_id, 'unload', remove_now=True, destroy=True)

        self.request_cache.shutdown()

        super(TunnelCommunity, self).unload()

    def get_session_keys(self, keys, direction):
        # increment salt_explicit
        keys[direction + 4] += 1
        return keys[direction], keys[direction + 2], keys[direction + 4]

    def _generate_circuit_id(self):
        circuit_id = random.getrandbits(32)

        # Prevent collisions.
        while circuit_id in self.circuits:
            circuit_id = random.getrandbits(32)

        return circuit_id

    def do_circuits(self):
        for circuit_length, num_circuits in self.circuits_needed.items():
            num_to_build = max(0, num_circuits - len(self.data_circuits(circuit_length)))
            self.logger.info("Want %d data circuits of length %d", num_to_build, circuit_length)
            for _ in range(num_to_build):
                if not self.create_circuit(circuit_length):
                    self.logger.info("circuit creation of %d circuits failed, no need to continue", num_to_build)
                    break
        self.do_remove()

    def build_tunnels(self, hops):
        if hops > 0:
            self.circuits_needed[hops] = max(self.settings.max_circuits,
                                             min(self.settings.max_circuits, self.circuits_needed.get(hops, 0) + 1))
            self.do_circuits()

    def tunnels_ready(self, hops):
        if hops > 0 and self.circuits_needed.get(hops, 0):
            return len(self.active_data_circuits(hops)) / float(self.circuits_needed[hops])
        return 1.0

    def do_remove(self):
        # Remove circuits that are inactive / are too old / have transferred too many bytes.
        for key, circuit in self.circuits.items():
            if circuit.state == CIRCUIT_STATE_READY and \
               circuit.last_activity < time.time() - self.settings.max_time_inactive:
                self.remove_circuit(key, 'no activity')
            elif circuit.creation_time < time.time() - self.settings.max_time:
                self.remove_circuit(key, 'too old')
            elif circuit.bytes_up + circuit.bytes_down > self.settings.max_traffic:
                self.remove_circuit(key, 'traffic limit exceeded')

        # Remove relays that are inactive / are too old / have transferred too many bytes.
        for key, relay in self.relay_from_to.items():
            if relay.last_activity < time.time() - self.settings.max_time_inactive:
                self.remove_relay(key, 'no activity', both_sides=False)
            elif relay.creation_time < time.time() - self.settings.max_time:
                self.remove_relay(key, 'too old', both_sides=False)
            elif relay.bytes_up + relay.bytes_down > self.settings.max_traffic:
                self.remove_relay(key, 'traffic limit exceeded', both_sides=False)

        # Remove exit sockets that are too old / have transferred too many bytes.
        for circuit_id, exit_socket in self.exit_sockets.items():
            if exit_socket.last_activity < time.time() - self.settings.max_time_inactive:
                self.remove_exit_socket(circuit_id, 'no activity')
            elif exit_socket.creation_time < time.time() - self.settings.max_time:
                self.remove_exit_socket(circuit_id, 'too old')
            elif exit_socket.bytes_up + exit_socket.bytes_down > self.settings.max_traffic:
                self.remove_exit_socket(circuit_id, 'traffic limit exceeded')

        # Remove exit_candidates that are not returned as dispersy verified candidates
        current_peers = set(p.public_key.key_to_bin() for p in self.network.get_peers_for_service(self.master_peer.mid))
        ckeys = list(self.exit_candidates.keys())
        for pubkey in ckeys:
            if pubkey not in current_peers:
                self.exit_candidates.pop(pubkey)
                self.logger.info("Removed candidate from exit_candidates dictionary")

    @property
    def compatible_candidates(self):
        return [p for p in self.network.get_peers_for_service(self.master_peer.mid)
                if self.crypto.is_key_compatible(p.public_key)]

    def create_circuit(self, goal_hops, ctype=CIRCUIT_TYPE_DATA, callback=None, required_exit=None, info_hash=None):

        self.logger.info("Creating a new circuit of length %d (type: %s)", goal_hops, ctype)

        # Determine the last hop
        if not required_exit:
            if ctype == CIRCUIT_TYPE_DATA:
                required_exit = random.choice(list(self.exit_candidates.values())) if self.exit_candidates else None
            else:
                # For exit nodes that don't exit actual data, we prefer verified candidates,
                # but we also consider exit candidates.
                if self.compatible_candidates:
                    required_exit = random.choice(self.compatible_candidates)
                elif self.exit_candidates:
                    required_exit = random.choice(list(self.exit_candidates.values()))

        if not required_exit:
            self.logger.info("Could not create circuit, no available exit-nodes")
            return False

        # Determine the first hop
        if goal_hops == 1 and required_exit:
            # If the number of hops is 1, it should immediately be the required_exit hop.
            self.logger.info("First hop is required exit")
            possible_first_hops = [required_exit]
        else:
            self.logger.info("Look for a first hop that is not an exit node and is not used before")
            first_hops = set([c.peer.address for c in self.circuits.values()])
            possible_first_hops = [c for c in self.compatible_candidates
                                   if c.address not in first_hops and c.address != required_exit.address]

        if not possible_first_hops:
            self.logger.info("Could not create circuit, no first hop available")
            return False

        # Finally, construct the Circuit object and send the CREATE message
        circuit_id = self._generate_circuit_id()
        self.circuits[circuit_id] = circuit = Circuit(circuit_id, goal_hops, ctype, callback, required_exit, info_hash)
        self.request_cache.add(CircuitRequestCache(self, circuit, self.settings.circuit_timeout))
        self.send_initial_create(circuit, possible_first_hops)

        return circuit_id

    def send_initial_create(self, circuit, candidate_list):
        if self.request_cache.has(u"retry", circuit.circuit_id):
            self.request_cache.pop(u"retry", circuit.circuit_id)

        first_hop = random.choice(candidate_list)
        alt_first_hops = [c for c in candidate_list if c != first_hop]

        circuit.unverified_hop = Hop(first_hop.public_key)
        circuit.unverified_hop.address = first_hop.address
        circuit.unverified_hop.dh_secret, circuit.unverified_hop.dh_first_part = self.crypto.generate_diffie_secret()

        self.logger.info("Adding first hop %s:%d to circuit %d", *(first_hop.address + (circuit.circuit_id,)))

        self.request_cache.add(RetryRequestCache(self, circuit, alt_first_hops,
                                                 self.send_initial_create, self.settings.next_hop_timeout))

        self.increase_bytes_sent(circuit, self.send_cell([first_hop],
                                                         u"create",
                                                         CreatePayload(circuit.circuit_id,
                                                                       self.my_peer.public_key.key_to_bin(),
                                                                       circuit.unverified_hop.dh_first_part)))

    def remove_circuit(self, circuit_id, additional_info='', remove_now=False, destroy=False):
        """
        Remove a circuit and return a deferred that fires when all data associated with the circuit is destroyed.
        Optionally send a destroy message.
        """
        circuit_to_remove = self.circuits.get(circuit_id, None)
        if circuit_to_remove is None:
            self.logger.warning('Cannot remove unknown circuit %d', circuit_id)
            return

        remove_deferred = Deferred()
        self.logger.info("Removing circuit %d " + additional_info, circuit_id)

        if destroy:
            self.destroy_circuit(circuit_to_remove)

        def remove_circuit_info():
            circuit = self.circuits.pop(circuit_id, None)
            if circuit:
                self.logger.info("Removed circuit %d " + additional_info, circuit_id)

            # Clean up the directions dictionary
            self.directions.pop(circuit_id, None)

            remove_deferred.callback(circuit_id)

        circuit_to_remove.close()

        if self.settings.remove_tunnel_delay == 0 or remove_now:
            remove_circuit_info()
        elif not self.is_pending_task_active("remove_circuit_%s" % circuit_id):
            self.register_task("remove_circuit_%s" % circuit_id,
                               reactor.callLater(self.settings.remove_tunnel_delay, remove_circuit_info))

        return remove_deferred

    def remove_relay(self, circuit_id, additional_info='', remove_now=False, destroy=False,
                     got_destroy_from=None, both_sides=True):
        """
        Remove a relay and all information associated with the relay. Return the relays that have been removed.
        """
        to_remove = [circuit_id]
        if both_sides:
            # Find other side of relay
            for k, v in self.relay_from_to.items():
                if circuit_id == v.circuit_id:
                    to_remove.append(k)

        # Send destroy
        if destroy:
            self.destroy_relay(to_remove, got_destroy_from=got_destroy_from)

        removed_relays = []
        for cid in to_remove:
            def remove_relay_info(cid_to_remove):
                # Remove the relay
                self.logger.info("Removing relay %d %s", cid_to_remove, additional_info)

                relay = self.relay_from_to.pop(cid_to_remove, None)
                if relay:
                    removed_relays.append(relay)

                # Remove old session key
                self.relay_session_keys.pop(cid_to_remove, None)

                # Clean directions dictionary
                self.directions.pop(cid_to_remove, None)

            if self.settings.remove_tunnel_delay == 0 or remove_now:
                remove_relay_info(cid)
            elif not self.is_pending_task_active("remove_relay_%s" % cid):
                self.register_task("remove_relay_%s" % cid,
                                   reactor.callLater(self.settings.remove_tunnel_delay,
                                                     lambda cid_copy=cid: remove_relay_info(cid_copy)))

        return removed_relays

    def remove_exit_socket(self, circuit_id, additional_info='', remove_now=False, destroy=False):
        """
        Remove an exit socket. Send a destroy message if necessary.
        """
        exit_socket_to_destroy = self.exit_sockets.get(circuit_id, None)
        if exit_socket_to_destroy and destroy:
            self.destroy_exit_socket(exit_socket_to_destroy)

        def remove_exit_socket_info():
            exit_socket = self.exit_sockets.pop(circuit_id, None)
            if exit_socket:
                # Close socket
                if exit_socket.enabled:
                    self.logger.info("Removing exit socket %d %s", circuit_id, additional_info)

                    def on_exit_socket_closed(_):
                        # Remove old session key
                        self.relay_session_keys.pop(circuit_id, None)

                    addCallback(exit_socket.close(), on_exit_socket_closed)

        if self.settings.remove_tunnel_delay == 0 or remove_now:
            remove_exit_socket_info()
        elif not self.is_pending_task_active("remove_exit_socket_%s" % circuit_id):
            self.register_task("remove_exit_socket_%s" % circuit_id,
                               reactor.callLater(self.settings.remove_tunnel_delay, remove_exit_socket_info))

    def destroy_circuit(self, circuit, reason=0):
        sock_addr = circuit.peer.address
        self.send_destroy(sock_addr, circuit.circuit_id, reason)
        self.logger.info("destroy_circuit %s %s", circuit.circuit_id, sock_addr)

    def destroy_relay(self, circuit_ids, reason=0, got_destroy_from=None):
        relays = {cid_from: (self.relay_from_to[cid_from].circuit_id,
                             self.relay_from_to[cid_from].peer.address) for cid_from in circuit_ids
                  if cid_from in self.relay_from_to}

        if got_destroy_from and got_destroy_from not in relays.values():
            self.logger.error("%s not allowed send destroy for circuit %s", *reversed(got_destroy_from))
            return

        for cid_from, (cid_to, sock_addr) in relays.items():
            self.logger.info("Found relay %s -> %s (%s)", cid_from, cid_to, sock_addr)
            if (cid_to, sock_addr) != got_destroy_from:
                self.send_destroy(sock_addr, cid_to, reason)
                self.logger.info("Fw destroy to %s %s", cid_to, sock_addr)

    def destroy_exit_socket(self, exit_socket, reason=0):
        sock_addr = exit_socket.peer.address
        self.send_destroy(sock_addr, exit_socket.circuit_id, reason)
        self.logger.info("Destroy_exit_socket %s %s", exit_socket.circuit_id, sock_addr)

    def data_circuits(self, hops=None):
        return {cid: c for cid, c in self.circuits.items()
                if c.ctype == CIRCUIT_TYPE_DATA and (hops is None or hops == c.goal_hops)}

    def active_data_circuits(self, hops=None):
        return {cid: c for cid, c in self.circuits.items()
                if c.state == CIRCUIT_STATE_READY and c.ctype == CIRCUIT_TYPE_DATA
                and (hops is None or hops == c.goal_hops)}

    def is_relay(self, circuit_id):
        return circuit_id > 0 and circuit_id in self.relay_from_to

    def is_circuit(self, circuit_id):
        return circuit_id > 0 and circuit_id in self.circuits

    def is_exit(self, circuit_id):
        return circuit_id > 0 and circuit_id in self.exit_sockets

    def send_cell(self, candidates, message_type, payload, circuit_id=None):
        message_id, _ = message_to_payload[message_type]
        circuit_id = circuit_id or payload.circuit_id
        message = self.serializer.pack_multiple(payload.to_pack_list()[1:])[0]
        cell = CellPayload(circuit_id, message_id, message)
        cell.encrypt(self.crypto, self.circuits.get(circuit_id), self.relay_session_keys.get(circuit_id))
        packet = self._ez_pack(self._prefix, 1, [cell.to_pack_list()], False)
        return self.send_packet(candidates, packet)

    def send_data(self, candidates, circuit_id, dest_address, source_address, data):
        payload = DataPayload(circuit_id, dest_address, source_address, data)
        return self.send_cell(candidates, u"data", payload, circuit_id)

    def send_packet(self, candidates, packet):
        for candidate in candidates:
            address = candidate if isinstance(candidate, tuple) else candidate.address
            self.endpoint.send(address, packet)
        return len(packet)

    def send_destroy(self, candidate, circuit_id, reason):
        auth = BinMemberAuthenticationPayload(self.my_peer.public_key.key_to_bin()).to_pack_list()
        payload = DestroyPayload(circuit_id, reason).to_pack_list()
        packet = self._ez_pack(self._prefix, 10, [auth, payload])
        self.send_packet([candidate], packet)

    def relay_cell(self, cell):
        next_relay = self.relay_from_to[cell.circuit_id]
        try:
            if next_relay.rendezvous_relay:
                cell.decrypt(self.crypto, relay_session_keys=self.relay_session_keys[cell.circuit_id])
                cell.encrypt(self.crypto, relay_session_keys=self.relay_session_keys[next_relay.circuit_id])
            else:
                direction = self.directions[cell.circuit_id]
                if direction == ORIGINATOR:
                    cell.encrypt(self.crypto, relay_session_keys=self.relay_session_keys[cell.circuit_id])
                elif direction == EXIT_NODE:
                    cell.decrypt(self.crypto, relay_session_keys=self.relay_session_keys[cell.circuit_id])
        except CryptoException as e:
            self.logger.warning(str(e))
            return

        cell.circuit_id = next_relay.circuit_id
        packet = self._ez_pack(self._prefix, 1, [cell.to_pack_list()], False)
        self.increase_bytes_sent(next_relay, self.send_packet([next_relay.peer], packet))

    def _ours_on_created_extended(self, circuit, payload):
        if self.request_cache.has(u"retry", payload.circuit_id):
            self.request_cache.pop(u"retry", payload.circuit_id)

        hop = circuit.unverified_hop

        try:
            shared_secret = self.crypto.verify_and_generate_shared_secret(hop.dh_secret, payload.key,
                                                                          payload.auth, hop.public_key.key.pk)
            hop.session_keys = self.crypto.generate_session_keys(shared_secret)

        except CryptoException:
            self.remove_circuit(circuit.circuit_id, "error while verifying shared secret, bailing out.")
            return

        circuit.add_hop(hop)
        circuit.unverified_hop = None

        if circuit.state == CIRCUIT_STATE_EXTENDING:
            candidate_list_enc = payload.candidate_list
            _, candidate_list = decode(self.crypto.decrypt_str(candidate_list_enc,
                                                               hop.session_keys[EXIT_NODE],
                                                               hop.session_keys[EXIT_NODE_SALT]))
            self.send_extend(circuit, candidate_list)

        elif circuit.state == CIRCUIT_STATE_READY:
            self.request_cache.pop(u"circuit", circuit.circuit_id)

            # Execute callback
            if circuit.callback:
                circuit.callback(circuit)
                circuit.callback = None
        else:
            return

    def send_extend(self, circuit, candidate_list):
        ignore_candidates = [self.crypto.key_to_bin(chop.public_key) for chop in circuit.hops] + \
                            [self.my_peer.public_key]
        if circuit.required_exit:
            ignore_candidates.append(circuit.required_exit.public_key.key_to_bin())

        become_exit = circuit.goal_hops - 1 == len(circuit.hops)
        if become_exit and circuit.required_exit:
            # Set the required exit according to the circuit setting (e.g. for linking e2e circuits)
            extend_hop_public_bin = circuit.required_exit.public_key.key_to_bin()
            extend_hop_addr = circuit.required_exit.address

        else:
            # The next candidate is chosen from the returned list of possible candidates
            for ignore_candidate in ignore_candidates:
                if ignore_candidate in candidate_list:
                    candidate_list.remove(ignore_candidate)

            for i in range(len(candidate_list) - 1, -1, -1):
                public_key = self.crypto.key_from_public_bin(candidate_list[i])
                if not self.crypto.is_key_compatible(public_key):
                    candidate_list.pop(i)

            pub_key = next(iter(candidate_list), None)
            extend_hop_public_bin = pub_key
            extend_hop_addr = None

        if extend_hop_public_bin:
            extend_hop_public_key = self.crypto.key_from_public_bin(extend_hop_public_bin)
            circuit.unverified_hop = Hop(extend_hop_public_key)
            circuit.unverified_hop.dh_secret, circuit.unverified_hop.dh_first_part = \
                self.crypto.generate_diffie_secret()

            self.logger.info("Extending circuit %d with %s", circuit.circuit_id, hexlify(extend_hop_public_bin))

            # Only retry if we are allowed to use another node
            if not become_exit or not circuit.required_exit:
                alt_candidates = [c for c in candidate_list if c != extend_hop_public_bin]
                self.request_cache.add(RetryRequestCache(self, circuit, alt_candidates,
                                                         self.send_extend, self.settings.next_hop_timeout))

            self.increase_bytes_sent(circuit, self.send_cell([circuit.peer],
                                                             u"extend",
                                                             ExtendPayload(circuit.circuit_id,
                                                                           circuit.unverified_hop.node_public_key,
                                                                           extend_hop_addr,
                                                                           circuit.unverified_hop.dh_first_part)))

        else:
            self.remove_circuit(circuit.circuit_id, "no candidates to extend, bailing out.")

    def update_exit_candidates(self, peer, become_exit):
        public_key = peer.public_key
        if become_exit:
            self.exit_candidates[public_key.key_to_bin()] = peer
        else:
            self.exit_candidates.pop(public_key.key_to_bin(), None)

    def parse_extra_bytes(self, extra_bytes):
        if not extra_bytes:
            return False

        payload = self.serializer.unpack_to_serializables([ExtraIntroductionPayload], extra_bytes)[0]
        return payload.exitnode

    def introduction_request_callback(self, peer, dist, payload):
        self.update_exit_candidates(peer, self.parse_extra_bytes(payload.extra_bytes))

    def introduction_response_callback(self, peer, dist, payload):
        self.update_exit_candidates(peer, self.parse_extra_bytes(payload.extra_bytes))

    def create_introduction_request(self, socket_address, extra_bytes=b''):
        extra_payload = ExtraIntroductionPayload(self.become_exitnode())
        extra_bytes = self.serializer.pack_multiple(extra_payload.to_pack_list())[0]
        return super(TunnelCommunity, self).create_introduction_request(socket_address, extra_bytes)

    def create_introduction_response(self, lan_socket_address, socket_address, identifier,
                                     introduction=None, extra_bytes=b''):
        extra_payload = ExtraIntroductionPayload(self.become_exitnode())
        extra_bytes = self.serializer.pack_multiple(extra_payload.to_pack_list())[0]
        return super(TunnelCommunity, self).create_introduction_response(lan_socket_address, socket_address,
                                                                         identifier, introduction, extra_bytes)

    @lazy_wrapper_unsigned_wd(CellPayload)
    def on_cell(self, source_address, cell, data):
        message_type = [k for k, v in message_to_payload.items() if v[0] == cell.message_type][0]
        circuit_id = cell.circuit_id
        self.logger.debug("Got %s (%d) from %s, I am %s", message_type, circuit_id, source_address, self.my_peer)

        if self.is_relay(circuit_id):
            next_relay = self.relay_from_to[circuit_id]
            this_relay = self.relay_from_to.get(next_relay.circuit_id, None)
            if this_relay:
                this_relay.beat_heart()
                self.increase_bytes_received(this_relay, len(data))
            self.logger.debug("Relaying %s from %d to %d", message_type, circuit_id, next_relay.circuit_id)
            self.relay_cell(cell)
            return

        circuit = self.circuits.get(circuit_id, None)
        try:
            cell.decrypt(self.crypto, circuit=circuit, relay_session_keys=self.relay_session_keys.get(circuit_id))
        except CryptoException:
            if circuit:
                self.send_destroy(circuit.peer, circuit_id, 0)
            return
        self.on_packet_from_circuit(source_address, cell.unwrap(self._prefix), circuit_id)

        if circuit:
            circuit.beat_heart()
            self.increase_bytes_received(circuit, len(data))

    def on_packet_from_circuit(self, source_address, data, circuit_id):
        if self._prefix != data[:22]:
            return
        msg_id = chr(ord(data[22:23]))
        if msg_id in self.decode_map_private:
            try:
                self.decode_map_private[msg_id](source_address, data, circuit_id)
            except:
                self.logger.error("Exception occurred while handling packet!\n"
                                  + ''.join(format_exception(*sys.exc_info())))

    def should_join_circuit(self, create_payload, previous_node_address):
        """
        Check whether we should join a circuit.
        Returns a deferred that fires with a boolean.
        """
        if self.settings.max_joined_circuits <= len(self.relay_from_to) + len(self.exit_sockets):
            self.logger.warning("Too many relays (%d)", (len(self.relay_from_to) + len(self.exit_sockets)))
            return succeed(False)

        return succeed(True)

    def join_circuit(self, create_payload, previous_node_address):
        """
        Actively join a circuit and send a created message back
        """
        circuit_id = create_payload.circuit_id

        self.directions[circuit_id] = EXIT_NODE
        self.logger.info('We joined circuit %d with neighbour %s', circuit_id, previous_node_address)

        shared_secret, key, auth = self.crypto.generate_diffie_shared_secret(create_payload.key)
        self.relay_session_keys[circuit_id] = self.crypto.generate_session_keys(shared_secret)

        peers_list = [peer for peer in self.compatible_candidates
                      if peer.public_key.key_to_bin() not in self.exit_candidates][:4]
        peers_keys = {c.public_key.key_to_bin(): c for c in peers_list}

        peer = Peer(create_payload.node_public_key, previous_node_address)
        self.request_cache.add(CreatedRequestCache(self, circuit_id, peer, peers_keys, self.settings.unstable_timeout))
        self.exit_sockets[circuit_id] = TunnelExitSocket(circuit_id, peer, self)

        keys_list_enc = self.crypto.encrypt_str(encode(list(peers_keys.keys())),
                                                *self.get_session_keys(self.relay_session_keys[circuit_id], EXIT_NODE))
        self.send_cell([Peer(create_payload.node_public_key, previous_node_address)], u"created",
                       CreatedPayload(circuit_id, key, auth, keys_list_enc))

    @tc_lazy_wrapper_unsigned(CreatePayload)
    def on_create(self, source_address, payload, _):
        if self.request_cache.has(u"created", payload.circuit_id):
            self.logger.warning("Already have a request for this circuit_id")
            return

        def determined_to_join(result):
            if result:
                self.join_circuit(payload, source_address)
            else:
                self.logger.warning("We're not joining circuit with ID %s", payload.circuit_id)

        addCallback(self.should_join_circuit(payload, source_address), determined_to_join)

    @tc_lazy_wrapper_unsigned(CreatedPayload)
    def on_created(self, source_address, payload, _):
        circuit_id = payload.circuit_id
        self.directions[circuit_id] = ORIGINATOR

        if self.request_cache.has(u"create", payload.circuit_id):
            request = self.request_cache.pop(u"create", circuit_id)

            self.logger.info("Got CREATED message forward as EXTENDED to origin.")

            self.relay_from_to[request.to_circuit_id] = relay = RelayRoute(request.from_circuit_id, request.peer)
            self.relay_from_to[request.from_circuit_id] = RelayRoute(request.to_circuit_id, request.to_peer)
            self.relay_session_keys[request.to_circuit_id] = self.relay_session_keys[request.from_circuit_id]

            self.directions[request.from_circuit_id] = EXIT_NODE
            self.remove_exit_socket(request.from_circuit_id)

            self.send_cell([relay.peer], u"extended", ExtendedPayload(relay.circuit_id,
                                                                      payload.key,
                                                                      payload.auth,
                                                                      payload.candidate_list))
        elif self.request_cache.has(u"circuit", payload.circuit_id) and \
                self.request_cache.has(u"retry", payload.circuit_id):
            circuit = self.circuits[circuit_id]
            self._ours_on_created_extended(circuit, payload)
        else:
            self.logger.warning("Received unexpected created for circuit %d", payload.circuit_id)

    @tc_lazy_wrapper_unsigned(ExtendPayload)
    def on_extend(self, source_address, payload, _):
        if not self.request_cache.has(u"created", payload.circuit_id):
            self.logger.warning("Received unexpected extend for circuit %d", payload.circuit_id)
            return

        circuit_id = payload.circuit_id
        # Leave the RequestCache in case the circuit owner wants to reuse the tunnel for a different next-hop
        request = self.request_cache.get(u"created", circuit_id)
        if not (payload.node_addr or payload.node_public_key in request.candidates):
            self.logger.warning("Node public key not in request candidates and no ip specified")
            return

        if payload.node_public_key in request.candidates:
            extend_candidate = request.candidates[payload.node_public_key]
        else:
            extend_candidate = self.network.get_verified_by_public_key_bin(payload.node_public_key)
            if not extend_candidate:
                extend_candidate = Peer(payload.node_public_key, payload.node_addr)

        self.logger.info("On_extend send CREATE for circuit (%s, %d) to %s:%d", source_address,
                         circuit_id, *extend_candidate.address)

        to_circuit_id = self._generate_circuit_id()

        if circuit_id in self.circuits:
            candidate = self.circuits[circuit_id].peer
        elif circuit_id in self.exit_sockets:
            candidate = self.exit_sockets[circuit_id].peer
        elif circuit_id in self.relay_from_to:
            candidate = self.relay_from_to[circuit_id].peer
        else:
            self.logger.error("Got extend for unknown source circuit_id")
            return

        self.logger.info("Extending circuit, got candidate with IP %s:%d from cache", *extend_candidate.address)

        self.request_cache.add(CreateRequestCache(self, to_circuit_id, circuit_id,
                                                  candidate, extend_candidate))

        self.send_cell([extend_candidate], u"create",
                       CreatePayload(to_circuit_id, self.my_peer.public_key.key_to_bin(), payload.key))

    @tc_lazy_wrapper_unsigned(ExtendedPayload)
    def on_extended(self, source_address, payload, _):
        if not self.request_cache.has(u"circuit", payload.circuit_id):
            self.logger.warning("Received unexpected extended for circuit %s", payload.circuit_id)
            return

        circuit_id = payload.circuit_id
        circuit = self.circuits[circuit_id]
        self._ours_on_created_extended(circuit, payload)

    def on_raw_data(self, circuit, origin, data):
        """
        Handle data, coming from a specific circuit and origin.
        This method is usually implemented in subclasses of this community.
        """
        pass

    @tc_lazy_wrapper_unsigned(DataPayload)
    def on_data(self, sock_addr, payload, _):
        # If its our circuit, the messenger is the candidate assigned to that circuit and the DATA's destination
        # is set to the zero-address then the packet is from the outside world and addressed to us from.
        circuit_id = payload.circuit_id
        destination = payload.dest_address
        origin = payload.org_address
        data = payload.data

        self.logger.debug("Got data (%d) from %s", circuit_id, sock_addr)

        circuit = self.circuits.get(circuit_id, None)
        if circuit and origin and sock_addr == circuit.peer.address:
            circuit.beat_heart()

            if DataChecker.could_be_ipv8(data):
                self.logger.debug("Giving incoming data packet to IPv8 (circuit ID %d)", circuit_id)
                self.on_packet_from_circuit(origin, data, circuit_id)
            else:
                # We probably received raw data, handle it
                self.on_raw_data(circuit, origin, data)

        # It is not our circuit so we got it from a relay, we need to EXIT it!
        else:
            self.logger.debug("Data for circuit %d exiting tunnel (%s)", circuit_id, destination)
            if destination != ('0.0.0.0', 0):
                self.exit_data(circuit_id, sock_addr, destination, data)
            else:
                self.logger.warning("Cannot exit data, destination is 0.0.0.0:0")

    @tc_lazy_wrapper_unsigned(PingPayload)
    def on_ping(self, source_address, payload, _):
        if not (payload.circuit_id in self.circuits
                or payload.circuit_id in self.exit_sockets
                or payload.circuit_id in self.relay_from_to):
            return

        exit_socket = self.exit_sockets.get(payload.circuit_id)
        if exit_socket:
            exit_socket.beat_heart()

        self.send_cell([source_address], u"pong", PongPayload(payload.circuit_id, payload.identifier))
        self.logger.debug("Got ping from %s", source_address)

    @tc_lazy_wrapper_unsigned(PongPayload)
    def on_pong(self, source_address, payload, _):
        if not self.request_cache.has(u"ping", payload.identifier):
            self.logger.warning("Invalid ping circuit_id")
            return

        self.request_cache.pop(u"ping", payload.identifier)
        self.logger.debug("Got pong from %s", source_address)

    def do_ping(self):
        # Ping circuits. Pings are only sent to the first hop, subsequent hops will relay the ping.
        for circuit in self.circuits.values():
            if circuit.state in [CIRCUIT_STATE_READY, CIRCUIT_STATE_EXTENDING] and \
               circuit.ctype != CIRCUIT_TYPE_RENDEZVOUS:
                cache = self.request_cache.add(PingRequestCache(self, circuit))
                self.increase_bytes_sent(circuit, self.send_cell([circuit.peer],
                                                                 u"ping",
                                                                 PingPayload(circuit.circuit_id, cache.number)))

    @lazy_wrapper(DestroyPayload)
    def on_destroy(self, peer, payload):
        source_address = peer.address
        circuit_id = payload.circuit_id
        self.logger.info("Got destroy from %s for circuit %s", source_address, circuit_id)

        if circuit_id in self.relay_from_to:
            self.remove_relay(circuit_id, "Got destroy", destroy=True, got_destroy_from=(circuit_id, source_address))

        elif circuit_id in self.exit_sockets and source_address == self.exit_sockets[circuit_id].peer.address:
            self.logger.info("Got an exit socket %s %s", circuit_id, source_address)
            self.remove_exit_socket(circuit_id, "Got destroy")

        elif circuit_id in self.circuits and source_address == self.circuits[circuit_id].peer.address:
            self.logger.info("Got a circuit %s %s", circuit_id, source_address)
            self.remove_circuit(circuit_id, "Got destroy")

        else:
            self.logger.warning("Invalid or unauthorized destroy")

    def exit_data(self, circuit_id, sock_addr, destination, data):
        if not self.become_exitnode() and not DataChecker.could_be_ipv8(data):
            self.logger.error("Dropping data packets, refusing to be an exit node for data")

        elif circuit_id in self.exit_sockets:
            if not self.exit_sockets[circuit_id].enabled:
                # Check that we got the data from the correct IP.
                if sock_addr[0] == self.exit_sockets[circuit_id].peer.address[0]:
                    self.exit_sockets[circuit_id].enable()
                else:
                    self.logger.error("Dropping outbound relayed packet: IP's are %s != %s",
                                      str(sock_addr), str(self.exit_sockets[circuit_id].peer.address))
            try:
                self.exit_sockets[circuit_id].sendto(data, destination)
            except:
                self.logger.warning("Dropping data packets while EXITing")
        else:
            self.logger.error("Dropping data packets with unknown circuit_id")

    def increase_bytes_sent(self, obj, num_bytes):
        if isinstance(obj, Circuit):
            obj.bytes_up += num_bytes
        elif isinstance(obj, RelayRoute):
            obj.bytes_up += num_bytes
        elif isinstance(obj, TunnelExitSocket):
            obj.bytes_up += num_bytes
        else:
            raise TypeError("Increase_bytes_sent() was called with an object that is not a Circuit, "
                            + "RelayRoute or TunnelExitSocket")

    def increase_bytes_received(self, obj, num_bytes):
        if isinstance(obj, Circuit):
            obj.bytes_down += num_bytes
        elif isinstance(obj, RelayRoute):
            obj.bytes_down += num_bytes
        elif isinstance(obj, TunnelExitSocket):
            obj.bytes_down += num_bytes
        else:
            raise TypeError("Increase_bytes_received() was called with an object that is not a Circuit, "
                            + "RelayRoute or TunnelExitSocket")
