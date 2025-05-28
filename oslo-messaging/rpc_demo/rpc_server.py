import socket
import psutil
from rpc import get_rpc_server


class ServerEndpoint(object):
    def get_hostname(self, ctx):
        return socket.gethostname()

    def get_cpu_info(self, ctx):
        return psutil.cpu_percent(interval=1)

    def get_mem_info(self, ctx):
        return psutil.virtual_memory().percent

    def get_disk_info(self, ctx):
        return psutil.disk_usage('/').percent


if __name__ == '__main__':
    endpoints = [ServerEndpoint()]
    server = get_rpc_server(endpoints)
    print("Starting server...")
    server.start()
    try:
        server.wait()
    except KeyboardInterrupt:
        print("Stopping server...")
        server.stop()
        server.wait()
