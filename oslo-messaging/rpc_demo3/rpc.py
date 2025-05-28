#!/usr/bin/env python
# -*- coding: utf-8 -*-
import oslo_messaging as messaging
from oslo_config import cfg
from oslo_log import log as logging
import eventlet
eventlet.monkey_patch()

CONF = cfg.CONF
# 注册 oslo_log 选项
logging.register_options(CONF)

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

try:
    # 从配置文件加载配置
    CONF(['--config-file', 'settings.cfg'])
except cfg.ConfigFilesNotFoundError:
    logging.getLogger(__name__).error("Config file 'settings.cfg' not found.")
    raise

# 初始化日志
logging.setup(CONF, __name__)


class ServerControlEndpoint(object):
    target = messaging.Target(namespace='controle',
                              version='2.0')

    def __init__(self, server):
        self.server = server

    def stop(self, ctx):
        if self.server:
            logging.getLogger(__name__).info("Stopping the server...")
            try:
                self.server.stop()
            except Exception as e:
                logging.getLogger(__name__).error(f"Failed to stop the server: {e}")


transport = messaging.get_transport(CONF)
target = messaging.Target(topic='test',
                          server='server1')


def get_rpc_server(endpoints):
    try:
        # return messaging.get_rpc_server(transport, target, endpoints, executor='threading')
        return messaging.get_rpc_server(transport, target, endpoints, executor='eventlet')
    except Exception as e:
        logging.getLogger(__name__).error(f"Failed to create RPC server: {e}")
        return None


def get_rpc_client():
    try:
        return messaging.RPCClient(transport, target)
    except Exception as e:
        logging.getLogger(__name__).error(f"Failed to create RPC client: {e}")
        return None

