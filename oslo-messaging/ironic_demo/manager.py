# manager.py
"""
RPC Manager for handling RPC clients and servers
"""
from oslo_context import context
from oslo_log import log
import threading
import rpcapi

LOG = log.getLogger(__name__)


class RPCManager(object):
    """RPC Manager providing unified RPC interface"""

    def __init__(self, transport=None, host=None):
        self.transport = transport
        self.host = host or 'localhost'
        self.clients = {}
        self.servers = {}
        self._lock = threading.Lock()

    def create_client(self, topic, version='1.0', serializer=None):
        """Create RPC client"""
        with self._lock:
            client_key = f"{topic}:{version}"
            if client_key not in self.clients:
                self.clients[client_key] = rpcapi.GenericRPCClient(
                    topic=topic,
                    transport=self.transport,
                    version=version,
                    serializer=serializer
                )
                LOG.info('Created RPC client for topic: %s', topic)
            return self.clients[client_key]

    def create_server(self, topic, endpoints, host=None, serializer=None):
        """Create RPC server"""
        with self._lock:
            if topic not in self.servers:
                self.servers[topic] = rpcapi.GenericRPCServer(
                    topic=topic,
                    endpoints=endpoints,
                    host=host or self.host,
                    transport=self.transport,
                    serializer=serializer
                )
                LOG.info('Created RPC server for topic: %s', topic)
            return self.servers[topic]

    def call(self, topic, method, context=None, version='1.0', **kwargs):
        """Convenient synchronous RPC call method"""
        client = self.create_client(topic, version)
        ctx = context or self._get_default_context()
        return client.call(ctx, method, **kwargs)

    def cast(self, topic, method, context=None, version='1.0', **kwargs):
        """Convenient asynchronous RPC call method"""
        client = self.create_client(topic, version)
        ctx = context or self._get_default_context()
        return client.cast(ctx, method, **kwargs)

    def start_server(self, topic):
        """Start specified RPC server"""
        if topic in self.servers:
            self.servers[topic].start()
            LOG.info('Started RPC server for topic: %s', topic)
        else:
            raise ValueError(f"Server for topic '{topic}' not found")

    def stop_server(self, topic):
        """Stop specified RPC server"""
        if topic in self.servers:
            self.servers[topic].stop()
            LOG.info('Stopped RPC server for topic: %s', topic)

    def stop_all_servers(self):
        """Stop all RPC servers"""
        for topic, server in self.servers.items():
            server.stop()
            LOG.info('Stopped RPC server for topic: %s', topic)

    def _get_default_context(self):
        """Get default context"""
        return context.RequestContext()
