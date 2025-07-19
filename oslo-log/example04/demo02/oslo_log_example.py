#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
from oslo_config import cfg
from oslo_log import log as logging
import itertools
import time

# 定义配置选项
mongo_OPTS = [
    cfg.StrOpt('database',
               default='mongodb',
               help='database'),
]

OPTS = [
    cfg.IntOpt('max_retries',
               default=3,
               help="max connection to database times"),
    cfg.IntOpt('retry_interval',
               default=60,
               help='connection timeout 60 seconds'),
    cfg.StrOpt('connection',
               default='mongodb://192.168.1.111:27017,'
                       '192.168.1.112:27017,'
                       '192.168.1.113:27017/test',
               help='connection mongodb url'),
]

LOGGING_OPTS = [
    cfg.StrOpt('log_file',
               default='example.log',
               help='Log file to output to.'),
    cfg.IntOpt('log_level',
               default=30,  # logging.INFO
               help='Log level.'),
    cfg.BoolOpt('debug',
                default=False,
                help='Enable debug logging.'),
]


# 将配置项注册到相应的分组中
def list_opts():
    return [
        ('MONGO', itertools.chain(mongo_OPTS)),
        ('DEFAULT', itertools.chain(OPTS)),
        ('log', itertools.chain(LOGGING_OPTS))
    ]


# 初始化配置对象
conf = cfg.ConfigOpts()

# 注册配置项
for group, options in list_opts():
    conf.register_opts(list(options), group=None if group == "DEFAULT" else group)

# 设置日志
logging.register_options(conf)

if __name__ == '__main__':
    # 解析命令行参数
    conf(sys.argv[1:], project='oslo_log_example', default_config_files=['./settings.conf'])

    # 获取日志文件位置
    log_file = conf.log.log_file
    log_level = conf.log.log_level
    debug_mode = conf.log.debug

    # 设置日志输出
    logging.setup(conf, 'oslo_log_example')
    LOG = logging.getLogger(__name__)

    # 设置日志级别
    if debug_mode:
        LOG.setLevel(logging.DEBUG)
    else:
        LOG.setLevel(log_level)

    # 输出日志信息
    LOG.debug(f'Logging to {log_file} with log level {log_level}')


    def connect_to_database():
        max_retries = conf.max_retries
        retry_interval = conf.retry_interval
        connection_str = conf.connection

        db = conf.MONGO.database
        LOG.debug(f'Connecting to MongoDB at {connection_str}{db}...')

        for attempt in range(max_retries):
            try:
                LOG.info(f'Attempting to connect to MongoDB at {connection_str}{db}...')
                time.sleep(1)  # 模拟连接延迟
                LOG.info('Connected to MongoDB successfully!')
                return
            except Exception as e:
                LOG.error(f'Connection attempt {attempt + 1} failed: {e}')
                time.sleep(retry_interval)

        LOG.critical('Failed to connect to the database after multiple attempts.')


    connect_to_database()
