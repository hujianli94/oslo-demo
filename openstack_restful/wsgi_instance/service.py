#!/usr/bin/env python3
# -*- coding:utf8 -*-

import wsgi


class WSGIService(object):
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
###列出集合中的所有虚拟机记录
# curl -X GET http://localhost:8080/instances
curl -H "X-Auth-Token: open-sesame" http://localhost:8080/instances

###添加一条虚拟机记录
# curl -X POST -H "Content-Type: application/json" -d '{"name":"inst-3"}' http://localhost:8080/instances
curl -X POST -H "X-Auth-Token: open-sesame" -d '{"name":"inst-3"}' http://localhost:8080/instances


###获取一条虚拟机记录的信息
# curl -X GET http://localhost:8080/instances/f0f7f8b9-6297-4928-8729-a7ce3f0e1a8b
curl -X GET -H "X-Auth-Token: open-sesame" http://localhost:8080/instances/f0f7f8b9-6297-4928-8729-a7ce3f0e1a8b


###更新一条虚拟机记录的信息
# curl -X PUT -H "Content-Type: application/json" -d '{"name":"inst-3-updated"}' http://localhost:8080/instances/f0f7f8b9-6297-4928-8729-a7ce3f0e1a8b
curl -X PUT -H "X-Auth-Token: open-sesame" -H "Content-Type: application/json" -d '{"name":"inst-113-updated"}' http://localhost:8080/instances/f0f7f8b9-6297-4928-8729-a7ce3f0e1a8b


###删除一条虚拟机记录
# curl -X DELETE http://localhost:8080/instances/f0f7f8b9-6297-4928-8729-a7ce3f0e1a8b
curl -X DELETE -H  "X-Auth-Token: open-sesame" http://localhost:8080/instances/f0f7f8b9-6297-4928-8729-a7ce3f0e1a8b
"""