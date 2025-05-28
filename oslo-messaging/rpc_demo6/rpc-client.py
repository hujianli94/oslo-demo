#!/usr/bin/env python3
# -*- coding:utf8 -*-
from oslo_config import cfg
import log
import oslo_messaging as messaging
from rpc_utils import get_client, load_config

DOMAIN = "rpc-client"
log.rpc_log_prepare(DOMAIN)
LOG = log.logname(__name__)

# 加载配置
try:
    load_config('settings.cfg')
except Exception as e:
    LOG.error(str(e))
    raise

# 创建 RPC 客户端
target = messaging.Target(topic='calculator', server='server1')
client = get_client(target)


def perform_operation(operation, num1, num2):
    try:
        LOG.info(f"Performing {operation} on {num1} and {num2}")
        result = client.call({}, 'calculate', operation=operation, num1=num1, num2=num2)
        LOG.info(f"Result of {operation}: {result}")
    except Exception as e:
        LOG.error(f"Error performing {operation}: {e}")


if __name__ == "__main__":
    perform_operation('add', 5, 3)
    perform_operation('subtract', 10, 4)
    perform_operation('multiply', 6, 7)
    perform_operation('divide', 12, 3)
