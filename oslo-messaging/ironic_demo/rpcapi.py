"""
Generic RPC API implementation based on oslo.messaging
"""
import oslo_messaging as messaging
from oslo_service import service
from oslo_log import log

LOG = log.getLogger(__name__)


class GenericRPCClient(object):
    """Generic RPC client wrapper for oslo.messaging"""

    def __init__(self, topic, transport=None, version='1.0',
                 serializer=None, version_cap=None):
        self.topic = topic
        self.version = version
        self.transport = transport

        # Create target and client following Ironic's pattern
        target = messaging.Target(topic=self.topic, version=self.version)
        self.client = messaging.get_rpc_client(
            self.transport, target,
            version_cap=version_cap,
            serializer=serializer
        )
        self.timeout = 60  # 默认超时时间

    def call(self, context, method, timeout=None, **kwargs):
        """Synchronous RPC call"""
        current_timeout = timeout if timeout is not None else self.timeout
        cctxt = self.client.prepare(timeout=current_timeout)
        try:
            return cctxt.call(context, method, **kwargs)
        except messaging.MessagingTimeout:
            LOG.error("RPC call timed out: %s", method)
            raise
        except Exception as e:
            LOG.error("Unexpected error in RPC call: %s", str(e))
            raise

    def cast(self, context, method, **kwargs):
        """Asynchronous RPC call"""
        cctxt = self.client.prepare()
        return cctxt.cast(context, method, **kwargs)

    def prepare_call(self, topic=None, version=None):
        """Prepare specific RPC call context"""
        return self.client.prepare(topic=topic or self.topic, version=version)


class GenericRPCServer(service.Service):
    """Generic RPC server wrapper for oslo.messaging"""

    def __init__(self, topic, endpoints, host=None, transport=None,
                 serializer=None):
        super().__init__()
        self.topic = topic
        self.endpoints = endpoints
        self.host = host or 'localhost'
        self.transport = transport

        # Create target and server following Ironic's pattern
        target = messaging.Target(topic=self.topic, server=self.host)
        self.rpcserver = messaging.get_rpc_server(
            self.transport, target, self.endpoints,
            executor='eventlet', serializer=serializer
        )

    def start(self):
        """Start RPC server"""
        super().start()
        self.rpcserver.start()
        LOG.info('Started RPC server for topic %(topic)s on host %(host)s',
                 {'topic': self.topic, 'host': self.host})

    def stop(self, graceful=False):
        """Stop RPC server"""
        if self.rpcserver:
            self.rpcserver.stop()
        super().stop()
