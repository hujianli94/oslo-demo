import subprocess

class DemoManager(object):
    def check_ssh_service_status(self, ctx):
        status = subprocess.call(['systemctl', 'is-active', '--quiet', 'ssh'])
        return "Active" if status == 0 else "Inactive"

    def check_docker_service_status(self, ctx):
        status = subprocess.call(['systemctl', 'is-active', '--quiet', 'docker'])
        return "Active" if status == 0 else "Inactive"

    def get_container_status(self, ctx, container_id):
        result = subprocess.run(['docker', 'inspect', '--format', '{{.State.Status}}', container_id],
                                capture_output=True, text=True)
        return result.stdout.strip() if result.returncode == 0 else "Container not found"

    def restart_container(self, ctx, container_id):
        result = subprocess.run(['docker', 'restart', container_id],
                                capture_output=True, text=True)
        return result.stdout.strip() if result.returncode == 0 else "Failed to restart container"
