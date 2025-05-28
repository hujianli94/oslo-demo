#!/usr/bin/env python3
# server.py
"""
RPC Server implementation
"""
import time
import eventlet

eventlet.monkey_patch()
import rpcapi
import config
import sys
import threading
from oslo_log import log
from oslo_service import service

LOG = log.getLogger(__name__)

from oslo_config import cfg

CONF = cfg.CONF


class DemoRPCService(rpcapi.GenericRPCServer):
    """Demo RPC Service following Ironic's BaseRPCService pattern"""

    def __init__(self, topic='demo-service', config_file='settings.cfg'):
        # 加载配置
        self.conf = config.load_config(config_file)
        self.transport = config.get_transport()

        # 创建端点
        self.endpoint = DemoEndpoint()

        # 初始化父类
        super().__init__(
            topic=topic,
            endpoints=[self.endpoint],
            host=self.conf.host,
            transport=self.transport
        )

        self._started = False
        self._failure = None

    def wait_for_start(self):
        """Wait for service to start, following Ironic's pattern"""
        while not self._started and not self._failure:
            time.sleep(0.1)
        if self._failure:
            LOG.critical(self._failure)
            sys.exit(self._failure)

    def start(self):
        """Start RPC server with error handling"""
        self._failure = None
        self._started = False

        try:
            super().start()
            self._started = True
            # LOG.info('Demo RPC service started successfully on topic: %s', self.topic)
        except Exception as exc:
            self._failure = f"{exc.__class__.__name__}: {exc}"
            LOG.error('Failed to start RPC service: %s', self._failure)
            raise

    def stop(self):
        """Stop RPC server gracefully"""
        try:
            super().stop()
            LOG.info('Demo RPC service stopped successfully')
        except Exception as e:
            LOG.exception('Error occurred when stopping RPC service: %s', e)


class DemoEndpoint(object):
    """Demo RPC endpoint for server"""

    def __init__(self):
        self.version = '1.0'

    def hello(self, context, name):
        """Hello method"""
        print(f'Received hello call with name: {name}')
        return f"Hello, {name}!"

    def calculate(self, context, a, b, operation='add'):
        """Calculate method"""
        if operation == 'add':
            result = a + b
        elif operation == 'multiply':
            result = a * b
        else:
            raise ValueError(f"Unsupported operation: {operation}")

        print(f'Calculation: {a} {operation} {b} = {result}')
        return result

    # 耗时操作
    def backup_database(self, context, database_name, backup_path):
        """异步数据库备份操作 - 可能需要几小时"""
        def do_backup():
            # 模拟长时间的备份操作
            LOG.info(f'Starting backup of {database_name} to {backup_path}')
            time.sleep(300)  # 模拟5分钟的备份时间
            LOG.info(f'Backup completed for {database_name}')

            # 在后台线程中执行备份

        backup_thread = threading.Thread(target=do_backup)
        backup_thread.start()

        return f"Backup started for {database_name}"


    def system_health_check(self, context, check_type='full'):
        """异步系统健康检查 - 可能需要几十分钟"""
        def run_health_check():
            checks = ['cpu', 'memory', 'disk', 'network', 'services']
            for check in checks:
                LOG.info(f'Running {check} health check')
                time.sleep(120)  # 每项检查2分钟  
                LOG.info(f'{check} check completed')
            LOG.info('Full system health check completed')
    
        threading.Thread(target=run_health_check).start()
        return f"Health check started with type: {check_type}"
def main():
    """Main entry point following Ironic's conductor main pattern"""
    # 配置文件路径和主题名称
    config_file = 'settings.cfg'
    topic = 'demo-service'

    # LOG.info('Starting RPC server for topic: %s', topic)

    # 创建 RPC 服务
    rpc_service = DemoRPCService(topic=topic, config_file=config_file)

    try:
        # 启动服务
        launcher = service.launch(CONF, rpc_service, restart_method='mutate')

        # 等待服务启动完成
        rpc_service.wait_for_start()
        print(f'RPC server started successfully on topic: {topic}')
        print('Press Ctrl+C to stop the server...')
        # 等待服务结束
        sys.exit(launcher.wait())
    except KeyboardInterrupt:
        launcher.stop()
    except Exception as e:
        LOG.error('Failed to start RPC server: %s', e)
        sys.exit(1)


if __name__ == '__main__':
    main()
