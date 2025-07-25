import logging
from paste import httpserver

logging.basicConfig(level=logging.INFO)
LOG = logging.getLogger(__name__)


def application(environ, start_response):
    start_response('200 OK', [('Content-type', 'text/html')])
    LOG.info('request: %s', environ)
    return [b'Hello World\n']  # 将字符串编码为字节


httpserver.serve(application, host='127.0.0.1', port=8080)
