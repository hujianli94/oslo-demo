#!/usr/bin/env python
# -*- coding: utf-8 -*-
import oslo_messaging as messaging
from oslo_config import cfg
from oslo_log import log as logging

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

# 从配置文件加载配置
CONF(['--config-file', 'settings.cfg'])

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
            self.server.stop()


transport = messaging.get_transport(CONF)
target = messaging.Target(topic='test',
                          server='server1')


def get_rpc_server(endpoints):
    return messaging.get_rpc_server(transport, target, endpoints, executor='threading')


def get_rpc_client():
    return messaging.RPCClient(transport, target)
