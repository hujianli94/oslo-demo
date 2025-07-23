# -*- coding: utf-8 -*-
import json
import sys
from oslo_config import cfg
from oslo_log import log as logging
import miniservice

CONF = cfg.CONF
LOG = logging.getLogger(__name__)


def default_action(env, method, path, query, body):
    LOG.info("demo action (method:%s, path:%s, query:%s, body:%s)"
             % (method, path, query, body))
    response_data = {'message': 'default', 'status': 'success'}
    response_json = json.dumps(response_data)
    return ("200 OK", response_json)


def test_action(env, method, path, query, body):
    LOG.info("test (method:%s, path:%s, query:%s, body:%s)"
             % (method, path, query, body))
    response_data = {'message': 'test', 'status': 'success'}
    response_json = json.dumps(response_data)
    return ("200 OK", response_json)


if __name__ == "__main__":
    CONF(sys.argv[1:])
    host = getattr(CONF, "host", "0.0.0.0")
    port = getattr(CONF, "port", "9001")
    # 创建MiniService实例
    service = miniservice.MiniService(host, port)
    # 添加路由和处理函数
    service.add_action("", default_action)
    service.add_action("test", test_action)

    # 启动服务
    service.start()
