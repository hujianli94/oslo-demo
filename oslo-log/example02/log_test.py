#!/usr/bin/env python3
# -*- coding:utf8 -*-
from oslo_log import log
from oslo_config import cfg
import sys

LOG = log.getLogger(__name__)


def prepare_service(argv=None, config_file=None):
    log.register_options(cfg.CONF)  # 注册配置项
    log_level = cfg.CONF.default_log_levels  # 设置默认日志级别INFO
    log.set_defaults(default_log_levels=log_level)
    if argv is None:
        argv = sys.argv
    cfg.CONF(argv[1:], project='ceilometer', default_config_files=config_file)  # 将进程中配置文件或日志文件注册在配置项中
    log.setup(cfg.CONF, 'ceilometer')


def print_log():
    LOG.info("===>I LOVE YOU CAESAR<=====")


prepare_service()
print_log()
