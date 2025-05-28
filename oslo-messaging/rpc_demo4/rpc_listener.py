#!/usr/bin/env python
# -*- coding: utf-8 -*-
from rpc import get_notification_listener
from oslo_log import log as logging
import oslo_messaging as messaging
from oslo_context import context
from oslo_service import service

LOG = logging.getLogger(__name__)

ctxt = context.get_current()


class NotificationEndpoint(object):
    # 修改 info 方法以接受 metadata 参数
    def info(self, ctxt, publisher_id, event_type, payload, metadata):
        LOG.info(f"Received notification: publisher_id={publisher_id}, event_type={event_type}, payload={payload}")
        return messaging.NotificationResult.HANDLED


class NotificationService(service.Service):
    def __init__(self):
        super(NotificationService, self).__init__()
        self.endpoints = [NotificationEndpoint()]
        self.listener = get_notification_listener(self.endpoints)

    def start(self):
        if self.listener:
            LOG.info("Starting the notification listener...")
            self.listener.start()

    def stop(self):
        if self.listener:
            LOG.info("Stopping the notification listener...")
            self.listener.stop()
            self.listener.wait()


if __name__ == '__main__':
    from rpc import CONF

    launcher = service.launch(CONF, NotificationService())
    launcher.wait()
