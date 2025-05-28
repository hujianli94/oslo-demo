from rpc import get_rpc_client

if __name__ == '__main__':
    client = get_rpc_client()
    ctx = {}

    hostname = client.call(ctx, 'get_hostname')
    print("Server hostname: {}".format(hostname))

    cpu_info = client.call(ctx, 'get_cpu_info')
    print("Server CPU usage: {}%".format(cpu_info))

    mem_info = client.call(ctx, 'get_mem_info')
    print("Server Memory usage: {}%".format(mem_info))

    disk_info = client.call(ctx, 'get_disk_info')
    print("Server Disk usage: {}%".format(disk_info))
