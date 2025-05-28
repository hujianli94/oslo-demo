import oslo_messaging as messaging
from oslo_service import service
import eventlet

eventlet.monkey_patch()

from rpc_utils import load_config, get_server, get_rpc_transport, CONF
import log

Domain = "rpc-server"
log.rpc_log_prepare(Domain)
LOG = log.logname(__name__)


# 定义计算端点
class CalculatorEndpoint(object):
    target = messaging.Target(version='1.0')

    def calculate(self, ctx, operation, num1, num2):
        if operation == 'add':
            return num1 + num2
        elif operation == 'subtract':
            return num1 - num2
        elif operation == 'multiply':
            return num1 * num2
        elif operation == 'divide':
            if num2 == 0:
                raise ZeroDivisionError("Division by zero is not allowed")
            return num1 / num2
        else:
            raise ValueError("Unsupported operation")


# 加载配置
try:
    load_config('settings.cfg')
except Exception as e:
    LOG.error(str(e))
    raise


class RpcService(service.Service):
    """
    RPC service class for RPC messaging.
    This class extends the oslo_service.Service class to provide an RPC service
    that listens for incoming messages and processes them using the specified
    endpoints.
    Attributes:
        endpoints (list): A list of endpoint objects that handle incoming RPC
            messages.
        transport (messaging.Transport): The transport object used for
            communication between the service and the messaging server.
        server (messaging.RPCServer): The RPC server object that listens for
            incoming messages and dispatches them to the appropriate endpoint.
    """

    def __init__(self):
        super(RpcService, self).__init__()
        self.endpoints = [CalculatorEndpoint()]
        self.transport = get_rpc_transport()
        # 添加 server 名称
        self.server = get_server(
            messaging.Target(topic='calculator', server='server1'),
            self.endpoints,
            executor='eventlet'
        )

    def start(self):
        """
        Start the RPC service.
        """
        LOG.info(f"Starting RPC service for topic 'calculator'")
        super(RpcService, self).start()
        self.server.start()

    def stop(self, graceful=True):
        """
        Stop the RPC service.
        """
        LOG.info("Stopping RPC server...")
        super(RpcService, self).stop()
        self.server.stop()
        self.server.wait()


if __name__ == '__main__':
    launcher = service.launch(CONF, RpcService())
    launcher.wait()
