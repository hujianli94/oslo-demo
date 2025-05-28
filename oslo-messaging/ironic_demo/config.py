"""
Configuration management for generic RPC system
"""
from oslo_config import cfg
from oslo_log import log
import oslo_messaging as messaging

LOG = log.getLogger(__name__)

# Configuration options following Ironic's pattern
rabbit_opts = [
    cfg.StrOpt('rabbit_host',
               default='localhost',
               help='RabbitMQ host address'),
    cfg.PortOpt('rabbit_port',
                default=5672,
                help='RabbitMQ port'),
    cfg.StrOpt('rabbit_userid',
               default='guest',
               help='RabbitMQ username'),
    cfg.StrOpt('rabbit_password',
               default='guest',
               secret=True,
               help='RabbitMQ password'),
    cfg.StrOpt('rabbit_virtual_host',
               default='/',
               help='RabbitMQ virtual host'),
]

default_opts = [
    cfg.StrOpt('host',
               default='localhost',
               help='Service hostname'),
]

CONF = cfg.CONF
TRANSPORT = None


def register_opts():
    """Register configuration options"""
    CONF.register_opts(default_opts)
    CONF.register_opts(rabbit_opts, group='rabbit')
    # 注册 oslo.log 的配置选项
    log.register_options(CONF)


def setup_logging():
    """Setup logging"""
    log.setup(CONF, 'generic-rpc')


def get_transport_url(url_str=None):
    """Get transport URL following Ironic's pattern"""
    if url_str:
        return messaging.TransportURL.parse(CONF, url_str)

    # Build transport URL from config
    # 构建 transport URL
    transport_url = (
        f"rabbit://{CONF.rabbit.rabbit_userid}:{CONF.rabbit.rabbit_password}@"
        f"{CONF.rabbit.rabbit_host}:{CONF.rabbit.rabbit_port}/"
        f"{CONF.rabbit.rabbit_virtual_host}"
    )
    return messaging.TransportURL.parse(CONF, transport_url)


def get_transport():
    """Get RPC transport"""
    global TRANSPORT
    if TRANSPORT is None:
        transport_url = get_transport_url()
        TRANSPORT = messaging.get_rpc_transport(CONF, url=str(transport_url))
        LOG.info('Created RPC transport with URL: %s',
                 str(transport_url).replace(CONF.rabbit.rabbit_password, '***'))
    return TRANSPORT


def load_config(config_file=None):
    """Load configuration file"""
    register_opts()

    if config_file:
        CONF(default_config_files=[config_file])
    else:
        CONF()

    setup_logging()
    return CONF
