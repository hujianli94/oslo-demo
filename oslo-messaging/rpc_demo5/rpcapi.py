from rpc import get_rpc_client

class DemoAPI(object):
    def __init__(self):
        self.client = get_rpc_client()

    def check_ssh_service_status(self, context):
        return self.client.call(context, 'check_ssh_service_status')

    def check_docker_service_status(self, context):
        return self.client.call(context, 'check_docker_service_status')

    def get_container_status(self, context, container_id):
        return self.client.call(context, 'get_container_status', container_id=container_id)

    def restart_container(self, context, container_id):
        return self.client.call(context, 'restart_container', container_id=container_id)
