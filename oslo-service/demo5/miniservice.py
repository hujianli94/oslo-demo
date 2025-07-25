#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import sys
from webob import Request
# 引入配置文件
from oslo_config import cfg
# 引入带调用链的日志
from oslo_log import log as logging
from oslo_context import context
# 引入REST服务
from oslo_service import service
from oslo_service import wsgi

CONF = cfg.CONF
LOG = logging.getLogger(__name__)
logging.register_options(CONF)
logging.setup(CONF, "m19k")


# mini服务
class MiniService:
    def __init__(self, host="0.0.0.0", port="9000", workers=1, use_ssl=False, cert_file=None, ca_file=None):
        self.host = host
        self.port = port
        self.workers = workers
        self.use_ssl = use_ssl
        self.cert_file = cert_file
        self.ca_file = ca_file
        self._actions = {}

    def add_action(self, url_path, action):
        if (url_path.lower() == "default") or (url_path == "/") or (url_path == ""):
            url_path = "default"
        elif (not url_path.startswith("/")):
            url_path = "/" + url_path
        self._actions[url_path] = action

    def _app(self, environ, start_response):
        context.RequestContext()
        LOG.debug("start action.")
        request = Request(environ)
        action = self._actions.get(environ['PATH_INFO'])
        if action is None:
            action = self._actions.get("default")

        if action is not None:
            result = action(environ, request.method, request.path_info, request.query_string, request.body)
            try:
                status_code, response_body = result
            except Exception as e:
                status_code = '500 Internal Server Error'
                response_body = str(result)

            # 确保Content-Type为application/json
            response_headers = [('Content-Type', 'application/json')]
            start_response(status_code, response_headers)
            return [response_body.encode('utf-8')]

    def start(self):
        self.server = wsgi.Server(CONF,
                                  "m19k",
                                  self._app,
                                  host=self.host,
                                  port=self.port,
                                  use_ssl=self.use_ssl)
        launcher = service.ProcessLauncher(CONF)
        launcher.launch_service(self.server, workers=self.workers)
        LOG.debug("launch service (%s:%s)." % (self.host, self.port))
        launcher.wait()
