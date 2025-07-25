#!/usr/bin/env python3
# -*- coding:utf8 -*-
import wsgi


class WSGIService(object):
    """
    用于wsgi服务的管理，包括服务的启动、停止、等待等
    """

    def __init__(self):
        self.loader = wsgi.Loader()
        self.app = self.loader.load_app()
        self.server = wsgi.Server(self.app,
                                  '0.0.0.0',
                                  8080)

    def start(self):
        self.server.start()

    def wait(self):
        self.server.wait()

    def stop(self):
        self.server.stop()


if __name__ == "__main__":
    server = WSGIService()
    server.start()
    server.wait()


"""
$ curl http://127.0.0.1:8080
<html>
 <head>
  <title>403 Forbidden</title>
 </head>
 <body>
  <h1>403 Forbidden</h1>
  Access was denied to this resource.<br /><br />



 </body>

$ curl -H "X-Auth-Token: open-sesame" http://localhost:8080/
Hello, Secret World of WebOb !
"""