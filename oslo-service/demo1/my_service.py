#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import logging
from oslo_service import service
from oslo_config import cfg

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
LOG = logging.getLogger(__name__)


class MyService(service.Service):
    def __init__(self, conf=None):
        self.conf = conf
        super(MyService, self).__init__()

    def start(self):
        LOG.info("服务开始...")
        while True:
            # 模拟服务的工作
            time.sleep(1)
            LOG.info("服务正在运行...")

    def stop(self):
        LOG.info("服务停止...")
        super(MyService, self).stop()


def main():
    # 配置选项
    conf = cfg.ConfigOpts()
    server = MyService(conf)
    launcher = service.launch(conf, server)

    try:
        launcher.wait()  # 等待服务运行
    except KeyboardInterrupt:
        LOG.info("服务被用户中断.")
        server.stop()
        launcher.stop()


if __name__ == '__main__':
    main()
