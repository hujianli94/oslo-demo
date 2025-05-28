#!/usr/bin/env python3
# -*- coding:utf8 -*-
import oslo_messaging as messaging
from oslo_config import cfg

# 配置相关
CONF = cfg.CONF
rabbit_opts = [
    cfg.StrOpt('rabbit_host', default='localhost',
               help='RabbitMQ host'),
    cfg.IntOpt('rabbit_port', default=5672,
               help='RabbitMQ port'),
    cfg.StrOpt('rabbit_userid', default='guest',
               help='RabbitMQ user ID'),
    cfg.StrOpt('rabbit_password', default='guest',
               help='RabbitMQ password'),
    cfg.StrOpt('rabbit_virtual_host', default='myRabbit',
               help='RabbitMQ virtual host')
]
CONF.register_opts(rabbit_opts, group='rabbit')


def load_config(config_file='settings.cfg'):
    """加载配置文件"""
    try:
        CONF(['--config-file', config_file])
    except cfg.ConfigFilesNotFoundError:
        raise FileNotFoundError(f"Config file '{config_file}' not found.")


def get_rpc_transport():
    """获取 RPC transport"""
    return messaging.get_rpc_transport(CONF)


def get_client(target, timeout=60):
    """创建 RPC 客户端"""
    transport = get_rpc_transport()
    return messaging.get_rpc_client(target=target, transport=transport, timeout=timeout)


def get_server(target, endpoints, executor='eventlet'):
    """创建 RPC 服务端"""
    return messaging.get_rpc_server(
        transport=get_rpc_transport(),
        target=target,
        endpoints=endpoints,
        executor=executor
    )
