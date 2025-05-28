#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
from rpc import ServerControlEndpoint
from rpc import get_rpc_server
import subprocess
from oslo_log import log as logging
from oslo_context import context

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


if __name__ == '__main__':
    endpoints = [
        ServerControlEndpoint(None),
        TestEndpoint(),
    ]
    server = get_rpc_server(endpoints)
    try:
        LOG.info('Starting server...')
        server.start()
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        LOG.info('Stopping server...')
        server.stop()

    server.wait()
