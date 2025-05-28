#!/usr/bin/env python
# -*- coding:utf8 -*-
from oslo_config import cfg
from oslo_context import context
from oslo_log import log as logging

# 配置选项
opts = [
    cfg.StrOpt('domain_id', help='Domain ID', default='a6b9360e'),
]

CONF = cfg.CONF
CONF.register_opts(opts)

# 日志配置
logging.register_options(CONF)
logging.setup(CONF, 'demo')
LOG = logging.getLogger(__name__)


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
        CONF(default_config_files=['demo.conf'])
        main()
    except Exception as e:
        LOG.exception("Unhandled error: %s", e)
