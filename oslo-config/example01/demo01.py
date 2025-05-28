#!/usr/bin/env python3
# -*- coding:utf8 -*-
import sys

from oslo_config import cfg
from oslo_config import types

"""
$ python demo01.py
debug: False, verbose: False

$ python demo01.py --logger-debug
debug: True, verbose: False

$ python demo01.py --logger-verbose
debug: False, verbose: True

$ python demo01.py --logger-nodebug --logger-noverbose
debug: False, verbose: False

$ python demo01.py --logger-debug --logger-verbose
debug: True, verbose: True
"""

# 创建参数组
logger_group = cfg.OptGroup(name='logger',
                            title='logger options')

logger_opts = [
    cfg.BoolOpt('debug',
                default=False,
                help='Enable debug log or not.'),
    cfg.BoolOpt('verbose',
                default=False,
                help='Enable verbose log or not.')
]


def main():
    conf = cfg.CONF
    conf.register_group(logger_group)
    conf.register_opts(logger_opts, logger_group)

    conf.register_cli_opts(logger_opts)
    conf.register_cli_opts(logger_opts, logger_group)
    conf(args=sys.argv[1:])
    conf(default_config_files=['settings.conf'])

    debug_mode = conf.logger.debug
    verbose_mode = conf.logger.verbose
    print(f"debug: {debug_mode}, verbose: {verbose_mode}")


if __name__ == "__main__":
    main()
