# ws_monitor/app.py
import time
import multiprocessing
from queue import Queue
from oslo_service import service
from oslo_log import log as logging
from ws_monitor import i18n
from ws_monitor import utils
from ws_monitor.plugins import base
import signal

LOG = logging.getLogger(__name__)

# 定义一个全局的终止标志
terminate_event = multiprocessing.Event()


def signal_handler(signum, frame):
    """信号处理函数，设置终止标志"""
    LOG.info(i18n._("Received signal %s, setting termination event...") % signum)
    terminate_event.set()


class PluginWorker(multiprocessing.Process):
    """Plugin worker process."""

    def __init__(self, conf, plugin_name, result_queue):
        super().__init__()
        self.conf = conf
        self.plugin_name = plugin_name
        self.result_queue = result_queue

    def run(self):
        """Runs the plugin and puts the result in the queue."""
        # 在子进程中设置信号处理
        signal.signal(signal.SIGINT, signal_handler)
        try:
            while not terminate_event.is_set():
                plugin_module = utils.import_module(
                    'ws_monitor.plugins.%s' % self.plugin_name)
                class_name = self.plugin_name.capitalize() + 'Monitor'
                if hasattr(plugin_module, class_name):
                    plugin_class = getattr(plugin_module, class_name)
                    if issubclass(plugin_class, base.BaseMonitor):
                        plugin_instance = plugin_class(self.conf)
                        LOG.debug(i18n._("Running plugin: %s in worker process") % self.plugin_name)
                        plugin_instance.monitor()
                    else:
                        LOG.warning(i18n._("Plugin %s is not a subclass of BaseMonitor") % self.plugin_name)
                else:
                    LOG.warning(i18n._("Plugin %s has no '%s' class") % (self.plugin_name, class_name))
                if terminate_event.is_set():
                    break
                time.sleep(self.conf.monitoring_interval)
        except ImportError as e:
            LOG.error(i18n._("Failed to load plugin %s: %s") % (self.plugin_name, e))
        except Exception as e:
            LOG.error(i18n._("Error initializing plugin %s: %s") % (self.plugin_name, e))


class MonitorService(service.Service):  # 继承 oslo_service.service.Service
    """Monitoring service."""

    def __init__(self, conf):
        super().__init__()
        self.conf = conf
        self.plugin_workers = []
        self.result_queue = Queue()

        # 设置信号处理
        signal.signal(signal.SIGINT, signal_handler)

    def start(self):
        """Starts the monitoring loop."""
        super().start()
        LOG.info(i18n._("Starting monitoring service..."))

        enabled_plugins = self.conf.enabled_plugins
        LOG.debug(i18n._("Enabled plugins: %s") % enabled_plugins)

        self.periodic_monitoring()  # 启动监控

    def periodic_monitoring(self):
        """Periodic monitoring task."""
        while not terminate_event.is_set():
            try:
                # 创建插件工作进程
                num_workers = self.conf.plugin_workers
                LOG.debug(i18n._("Creating %s plugin worker processes") % num_workers)
                self.plugin_workers = []
                for plugin_name in self.conf.enabled_plugins:
                    worker = PluginWorker(self.conf, plugin_name, self.result_queue)
                    self.plugin_workers.append(worker)
                    worker.start()  # 启动进程

                # 等待所有工作进程完成
                for worker in self.plugin_workers:
                    worker.join()

                # 读取队列中的结果 (这里只是示例，实际情况可能需要处理结果)
                while not self.result_queue.empty():
                    result = self.result_queue.get()
                    LOG.debug(i18n._("Received result: %s") % result)

                time.sleep(self.conf.monitoring_interval)
            except Exception as e:
                LOG.error(i18n._("Error in periodic monitoring: %s") % e)
        self.stop()

    def stop(self):
        """Stops the monitoring service."""
        LOG.info(i18n._("Stopping monitoring service..."))
        # 关闭所有工作进程
        for worker in self.plugin_workers:
            if worker.is_alive():
                worker.terminate()
                worker.join()  # 等待进程结束
        super().stop()  # 调用父类的 stop 方法
        LOG.info(i18n._("Monitoring service stopped."))
