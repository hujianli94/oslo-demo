#!/usr/bin/env python
# -*- coding: utf-8 -*-
import oslo_messaging as messaging
from rpc import get_rpc_server, CONF
from manager import DemoManager
from oslo_log import log as logging
from oslo_context import context
from oslo_service import service

LOG = logging.getLogger(__name__)


class DemoEndpoint(object):
    target = messaging.Target(namespace='demo',
                              version='2.0')

    def __init__(self):
        self.manager = DemoManager()

    def check_ssh_service_status(self, ctx):
        return self.manager.check_ssh_service_status(ctx)

    def check_docker_service_status(self, ctx):
        return self.manager.check_docker_service_status(ctx)

    def get_container_status(self, ctx, container_id):
        return self.manager.get_container_status(ctx, container_id)

    def restart_container(self, ctx, container_id):
        return self.manager.restart_container(ctx, container_id)


class RpcService(service.Service):
    def __init__(self):
        super(RpcService, self).__init__()
        self.endpoints = [DemoEndpoint()]
        self.rpc_server = get_rpc_server(self.endpoints)

    def start(self):
        try:
            if self.rpc_server:
                LOG.info("Starting the RPC server...")
                self.rpc_server.start()
        except Exception as e:
            LOG.error("Failed to start the RPC server: %s", e)
            raise

    def stop(self, graceful=True):
        try:
            if self.rpc_server:
                LOG.info("Stopping the RPC server...")
                self.rpc_server.stop(graceful=graceful)
                self.rpc_server.wait()
        except Exception as e:
            LOG.error("Failed to stop the RPC server: %s", e)
            raise


if __name__ == '__main__':
    launcher = service.launch(CONF, RpcService())
    launcher.wait()
