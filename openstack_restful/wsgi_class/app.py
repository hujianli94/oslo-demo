#!/usr/bin/env python3
# -*- coding:utf8 -*-
from webob import Response
from webob import Request
from webob.dec import wsgify
from webob import exc

class Hello(object):
    """
    实现hello应用程序的类
    """

    @wsgify(RequestClass=Request)
    def __call__(self, request):
        return Response('Hello, Secret World of WebOb !\n')

def app_factory(global_config, **local_config):
    return Hello()
