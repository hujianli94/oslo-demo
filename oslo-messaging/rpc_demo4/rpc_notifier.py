#!/usr/bin/env python
# -*- coding: utf-8 -*-
from rpc import notifier
from oslo_log import log as logging
from oslo_context import context

LOG = logging.getLogger(__name__)

if __name__ == '__main__':
    ctx = context.RequestContext()
    # 发送通知消息时移除多余的 topic 参数
    notifier.info(ctx.to_dict(), 'my_event', {'message': 'This is a test notification'})
    LOG.info("Notification sent.")
