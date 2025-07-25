#!/usr/bin/env python3
# -*- coding:utf8 -*-
import eventlet;
eventlet.monkey_patch()
import eventlet.wsgi
import greenlet
import sys
import os
from paste import deploy


class Loader(object):
    def load_app(self):
        """
        加载paste.deploy配置文件
        """
        ini_path = os.path.normpath(
            os.path.join(os.path.abspath(sys.argv[0]),
                         os.pardir,
                         'api-paste.ini')
        )
        if not os.path.isfile(ini_path):
            print("Cannot find api-paste.ini.\n")
            exit(1)

        return deploy.loadapp('config:' + ini_path)


class Server(object):
    """
    实现一个WSGI服务器，可以加载paste.deploy配置文件，并启动WSGI服务器。主要实现对线程的创建、管理和配置
    """
    def __init__(self, app, host='0.0.0.0', port=0):
        # 线程池,允许并行访问
        self._pool = eventlet.GreenPool(10)
        # wsgi服务的应用程序
        self.app = app
        # 创建监听套接字
        self._socket = eventlet.listen((host, port), backlog=10)
        # 获取监听套接字的地址和端口
        (self.host, self.port) = self._socket.getsockname()
        print("Listening on %(host)s:%(port)s" % self.__dict__)

    # 启动WSGI服务器，创建线程
    def start(self):
        self._server = eventlet.spawn(eventlet.wsgi.server,
                                      self._socket,
                                      self.app,
                                      protocol=eventlet.wsgi.HttpProtocol,
                                      custom_pool=self._pool)
    # 停止WSGI服务器，停止线程
    def stop(self):
        if self._server is not None:
            self._pool.resize(0)
            self._server.kill()

    # 监听 http 请求
    def wait(self):
        try:
            self._server.wait()
        except greenlet.GreenletExit:
            print("WSGI server has stopped.")
