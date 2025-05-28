from rpcapi import DemoAPI


def run_client():
    api = DemoAPI()
    context = {}

    print("Checking SSH service status:")
    ssh_status = api.check_ssh_service_status(context)
    print(ssh_status)

    print("Checking Docker service status:")
    docker_status = api.check_docker_service_status(context)
    print(docker_status)

    container_id = '9523ad4c5b6a'

    print(f"Getting status of container {container_id}:")
    container_status = api.get_container_status(context, container_id)
    print(container_status)

    print(f"Restarting container {container_id}:")
    restart_result = api.restart_container(context, container_id)
    print(restart_result)


if __name__ == "__main__":
    run_client()
