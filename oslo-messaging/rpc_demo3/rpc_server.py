#!/usr/bin/env python
# -*- coding: utf-8 -*-
from rpc import ServerControlEndpoint, CONF
from rpc import get_rpc_server
import subprocess
from oslo_log import log as logging
from oslo_context import context
from oslo_service import service

LOG = logging.getLogger(__name__)


def exec_cmd(cmd):
    try:
        with subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as p:
            stdout, stderr = p.communicate()
            code = p.returncode
            if code != 0:
                LOG.error(f"Command execution failed: {cmd}, error: {stderr.decode(errors='replace')}")

            return code, stdout, stderr
    except Exception as e:
        error_msg = f"Command execution raised exception: {str(e)}"
        LOG.error(error_msg)
        return -1000, None, error_msg.encode()


class TestEndpoint(object):
    def docker_all_images(self, ctx, arg):
        ctxt = context.get_current()
        LOG.info(f"Received request in docker_images method with context: {ctxt}, arg: {arg}")
        docker_cmd = """docker images|grep -v REPOSITORY|awk '{print $1 ":"$2}'"""
        code, stdout, stderr = exec_cmd(docker_cmd)
        if code != 0:
            return 'error'
        return stdout.decode('utf-8')

    def docker_one_images(self, ctx, arg):
        ctxt = context.get_current()
        LOG.info(f"Received request in docker_ps method with context: {ctxt}, arg: {arg}")
        docker_cmd = f"""docker images|grep {arg}|awk '{{print $1 ":"$2}}'"""
        code, stdout, stderr = exec_cmd(docker_cmd)
        if code != 0:
            return 'error'
        return stdout.decode('utf-8')


class RpcService(service.Service):
    def __init__(self):
        super(RpcService, self).__init__()
        self.endpoints = [ServerControlEndpoint(None), TestEndpoint(), ]
        self.rpc_server = get_rpc_server(self.endpoints)

    def start(self):
        if self.rpc_server:
            logging.getLogger(__name__).info("Starting the RPC server...")
            self.rpc_server.start()

    def stop(self):
        if self.rpc_server:
            logging.getLogger(__name__).info("Stopping the RPC server...")
            self.rpc_server.stop()
            self.rpc_server.wait()


if __name__ == '__main__':
    launcher = service.launch(CONF, RpcService())
    launcher.wait()
