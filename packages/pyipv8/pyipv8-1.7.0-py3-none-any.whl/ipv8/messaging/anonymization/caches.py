from __future__ import absolute_import

import logging
import time

from twisted.internet.defer import Deferred

from .tunnel import CIRCUIT_STATE_CLOSING, CIRCUIT_STATE_READY, PING_INTERVAL
from ...requestcache import NumberCache, RandomNumberCache


class CircuitRequestCache(NumberCache):
    """
    Used to track the total circuit creation time
    """
    def __init__(self, community, circuit, timeout):
        super(CircuitRequestCache, self).__init__(community.request_cache, u"circuit", circuit.circuit_id)
        self.community = community
        self.circuit = circuit
        self.timeout = timeout

    @property
    def timeout_delay(self):
        return float(self.timeout)

    def on_timeout(self):
        if self.circuit.state != CIRCUIT_STATE_READY:
            reason = 'timeout on CircuitRequestCache, state = %s, candidate = %s' % (
                self.circuit.state, self.circuit.peer.address)
            self.community.remove_circuit(self.number, reason)


class CreateRequestCache(NumberCache):
    """
    Used to track outstanding create messages
    """
    def __init__(self, community, to_circuit_id, from_circuit_id, peer, to_peer):
        super(CreateRequestCache, self).__init__(community.request_cache, u"create", to_circuit_id)
        self.community = community
        self.to_circuit_id = to_circuit_id
        self.from_circuit_id = from_circuit_id
        self.peer = peer
        self.to_peer = to_peer

    def on_timeout(self):
        to_circuit = self.community.circuits.get(self.to_circuit_id)
        if to_circuit and to_circuit.state != CIRCUIT_STATE_READY:
            self.community.remove_relay(self.to_circuit_id)


class CreatedRequestCache(NumberCache):
    """
    Used to track outstanding created messages
    """
    def __init__(self, community, circuit_id, candidate, candidates, timeout):
        super(CreatedRequestCache, self).__init__(community.request_cache, u"created", circuit_id)
        self.circuit_id = circuit_id
        self.candidate = candidate
        self.candidates = candidates
        self.timeout = timeout

    @property
    def timeout_delay(self):
        return float(self.timeout)

    def on_timeout(self):
        pass


class RetryRequestCache(NumberCache):
    """
    Used to retry adding additional hops to the circuit.
    """
    def __init__(self, community, circuit, candidates, retry_func, timeout):
        super(RetryRequestCache, self).__init__(community.request_cache, u"retry", circuit.circuit_id)
        self.community = community
        self.circuit = circuit
        self.candidates = candidates
        self.retry_func = retry_func
        self.timeout = timeout

    @property
    def timeout_delay(self):
        return float(self.timeout)

    def on_timeout(self):
        if not self.candidates or self.circuit.state == CIRCUIT_STATE_CLOSING:
            return

        def retry_later(_):
            self.retry_func(self.circuit, self.candidates)

        later = Deferred()
        self.community.request_cache.register_anonymous_task("retry-later", later, delay=0.0)
        later.addCallbacks(retry_later, lambda _: None)


class PingRequestCache(RandomNumberCache):

    def __init__(self, community, circuit):
        super(PingRequestCache, self).__init__(community.request_cache, u"ping")
        self.logger = logging.getLogger(__name__)
        self.circuit = circuit
        self.community = community

    @property
    def timeout_delay(self):
        return PING_INTERVAL + 5

    def on_timeout(self):
        if self.circuit.last_activity < time.time() - self.timeout_delay:
            self.logger.info("PingRequestCache: no response on ping, circuit %d timed out",
                             self.circuit.circuit_id)
            self.community.remove_circuit(self.circuit.circuit_id, 'ping timeout')


class IPRequestCache(RandomNumberCache):

    def __init__(self, community, circuit):
        super(IPRequestCache, self).__init__(community.request_cache, u"establish-intro")
        self.logger = logging.getLogger(__name__)
        self.circuit = circuit
        self.community = community

    def on_timeout(self):
        self.logger.info("IPRequestCache: no response on establish-intro (circuit %d)", self.circuit.circuit_id)
        self.community.remove_circuit(self.circuit.circuit_id, 'establish-intro timeout')


class RPRequestCache(RandomNumberCache):

    def __init__(self, community, rp):
        super(RPRequestCache, self).__init__(community.request_cache, u"establish-rendezvous")
        self.logger = logging.getLogger(__name__)
        self.community = community
        self.rp = rp

    def on_timeout(self):
        self.logger.info("RPRequestCache: no response on establish-rendezvous (circuit %d)",
                         self.rp.circuit.circuit_id)
        self.community.remove_circuit(self.rp.circuit.circuit_id, 'establish-rendezvous timeout')


class KeyRequestCache(RandomNumberCache):

    def __init__(self, community, circuit, sock_addr, info_hash):
        super(KeyRequestCache, self).__init__(community.request_cache, u"key-request")
        self.logger = logging.getLogger(__name__)
        self.circuit = circuit
        self.sock_addr = sock_addr
        self.info_hash = info_hash
        self.community = community

    def on_timeout(self):
        self.logger.info("KeyRequestCache: no response on key-request to %s",
                         self.sock_addr)
        if self.info_hash in self.community.infohash_pex:
            self.logger.info("Remove peer %s from the peer exchange cache", repr(self.sock_addr))
            peers = self.community.infohash_pex[self.info_hash]
            for peer in peers.copy():
                peer_sock, _ = peer
                if self.sock_addr == peer_sock:
                    self.community.infohash_pex[self.info_hash].remove(peer)


class DHTRequestCache(RandomNumberCache):

    def __init__(self, community, circuit, info_hash):
        super(DHTRequestCache, self).__init__(community.request_cache, u"dht-request")
        self.circuit = circuit
        self.info_hash = info_hash

    def on_timeout(self):
        pass


class KeyRelayCache(KeyRequestCache):

    def __init__(self, community, circuit, identifier, sock_addr, info_hash):
        super(KeyRelayCache, self).__init__(community, circuit, sock_addr, info_hash)
        self.identifier = identifier
        self.return_sock_addr = sock_addr

    def on_timeout(self):
        pass


class E2ERequestCache(RandomNumberCache):

    def __init__(self, community, info_hash, circuit, hop, sock_addr):
        super(E2ERequestCache, self).__init__(community.request_cache, u"e2e-request")
        self.circuit = circuit
        self.hop = hop
        self.info_hash = info_hash
        self.sock_addr = sock_addr

    def on_timeout(self):
        pass


class LinkRequestCache(RandomNumberCache):

    def __init__(self, community, circuit, info_hash):
        super(LinkRequestCache, self).__init__(community.request_cache, u"link-request")
        self.circuit = circuit
        self.info_hash = info_hash

    def on_timeout(self):
        pass
