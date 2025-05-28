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

transport = messaging.get_notification_transport(CONF)  # 使用 get_notification_transport 获取通知传输实例

# 创建通知器，移除 topic 参数
notifier = messaging.Notifier(transport, driver='messaging', publisher_id='my_service')

# 创建通知监听器目标
target = messaging.Target(topic='notifications', server='server1')


def get_notification_listener(endpoints):
    try:
        return messaging.get_notification_listener(transport, [target], endpoints, executor='eventlet')
    except Exception as e:
        logging.getLogger(__name__).error(f"Failed to create notification listener: {e}")
        return None