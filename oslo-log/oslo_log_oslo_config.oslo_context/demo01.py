#!/usr/bin/env python
# -*- coding:utf8 -*-
from oslo_config import cfg
from oslo_context import context
from oslo_log import log as logging
import sys

# 配置选项
_LOGGING_OPTS = [
    cfg.StrOpt('log_file',
               default='example.log',
               help='Log file to output to.'),
    cfg.IntOpt('log_level',
               default=logging.INFO,
               help='Log level.'),
    cfg.BoolOpt('debug',
                default=False,
                help='Enable debug logging.'),
]

# 定义configOpts实例
CONF = cfg.CONF
# 配置分组定义
log_group = cfg.OptGroup(name="log", title="log cfg")

# 注册分组
CONF.register_group(log_group)
# 注册配置选项
CONF.register_opts(_LOGGING_OPTS, group='log')

# 注册命令行选项
CONF.register_cli_opts(_LOGGING_OPTS, group=log_group)

# 注册日志选项
logging.register_options(CONF)
# 日志配置
logging.register_options(CONF)

# 获取参数，默认配置也可以通过--config-file来指定
CONF(sys.argv[1:], default_config_files=['settings.conf'])
DOMAIN = "demo"
# 初始化日志
logging.setup(CONF, DOMAIN)

LOG = logging.getLogger(__name__)
# 设置日志级别
if CONF.log.debug:
    LOG.setLevel(logging.DEBUG)
else:
    # print(CONF.log.log_level)
    LOG.setLevel(CONF.log.log_level)

LOG.debug(f'Logging to {CONF.log.log_file} with log level {CONF.log.log_level}')


def main():
    # 创建一个上下文对象
    ctx = context.RequestContext(user_id='6ce90b4d',
                                 project_id='d6134462',
                                 domain_id='a6b9360e',
                                 request_id='req-123456789')

    # 记录日志，包含上下文信息
    LOG.info("This is an info message without context")
    LOG.info("This is an info message with context", context=ctx)
    LOG.warning("This is a warning message with context", context=ctx)
    LOG.error("This is an error message with context", context=ctx)
    LOG.critical("This is a critical message with context", context=ctx)


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        LOG.exception("Unhandled error: %s", e)
