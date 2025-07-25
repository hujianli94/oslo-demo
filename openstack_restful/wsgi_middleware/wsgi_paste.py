from webob import Response
from webob.dec import wsgify
from paste import httpserver
from paste.deploy import loadapp
import os
import sys

ini_path = os.path.normpath(
    os.path.join(os.path.abspath(sys.argv[0]),
                 os.pardir,
                 'api-paste.ini')
)


@wsgify
def application(request):
    return Response('Hello, World of WebOb !\n')


def app_factory(global_config, **local_config):
    return application


if not os.path.isfile(ini_path):
    print("Cannot find api-paste.ini.\n")
    exit(1)

wsgi_app = loadapp('config:' + ini_path)
httpserver.serve(wsgi_app, host='127.0.0.1', port=8080)

"""
curl http://localhost:8080/    # 未设置X-Auth-Token头，返回HTTPForbidden错误
<html>
 <head>
  <title>403 Forbidden</title>
 </head>
 <body>
  <h1>403 Forbidden</h1>
  Access was denied to this resource.<br /><br />



 </body>
</html>(

curl -H "X-Auth-Token: open-sesame" http://localhost:8080/
Hello, World of WebOb !
"""