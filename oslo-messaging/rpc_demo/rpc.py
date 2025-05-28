import oslo_messaging as messaging
from oslo_config import cfg

CONF = cfg.CONF

# 定义 RabbitMQ 配置选项
rabbit_opts = [
    cfg.StrOpt('rabbit_host', default='localhost',
               help='RabbitMQ host'),
    cfg.IntOpt('rabbit_port', default=5672,
               help='RabbitMQ port'),
    cfg.StrOpt('rabbit_userid', default='guest',
               help='RabbitMQ user ID'),
    cfg.StrOpt('rabbit_password', default='guest',
               help='RabbitMQ password'),
    cfg.StrOpt('rabbit_virtual_host', default='/',
               help='RabbitMQ virtual host')
]
CONF.register_opts(rabbit_opts, group='rabbit')

# 从配置文件加载配置
CONF(['--config-file', 'settings.cfg'])

# 创建传输对象
transport = messaging.get_transport(CONF)

# 目标定义
target = messaging.Target(topic='test', server='server1')


def get_rpc_server(endpoints):
    return messaging.get_rpc_server(transport, target, endpoints, executor='threading')


def get_rpc_client():
    return messaging.RPCClient(transport, target)
