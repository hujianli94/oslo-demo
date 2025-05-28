#!/usr/bin/env python
# -*- coding: utf-8 -*-
from rpc import get_rpc_client
from oslo_log import log as logging
from oslo_context import context

LOG = logging.getLogger(__name__)

if __name__ == '__main__':
    client = get_rpc_client()
    ctx = context.RequestContext()
    LOG.info(f"Sending request to server with context: {ctx}")
    fun_1 = client.call(ctx.to_dict(), method='docker_all_images', arg='')
    LOG.info(f"Received response: {fun_1}")

    LOG.info(f"Sending request to server with context: {ctx}")
    fun_2 = client.call(ctx.to_dict(), method='docker_one_images', arg='centos')
    LOG.info(f"Received response: {fun_2}")
