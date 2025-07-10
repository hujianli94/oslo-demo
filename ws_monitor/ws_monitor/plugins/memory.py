# ws_monitor/plugins/memory.py
import psutil
import logging

from ws_monitor.plugins import base
from ws_monitor import i18n

LOG = logging.getLogger(__name__)


class MemoryMonitor(base.BaseMonitor):
    """内存监控插件."""

    def monitor(self):
        """监控内存使用情况."""
        try:
            memory = psutil.virtual_memory()
            memory_usage_dict = {
                "total": "{:.2f} MB".format(memory.total / (1024 * 1024)),
                "available": "{:.2f} MB".format(memory.available / (1024 * 1024)),
                "used": "{:.2f} MB".format(memory.used / (1024 * 1024)),
                "percent": "{} %".format(memory.percent),
            }
            self.log_metric("memory_usage", memory_usage_dict)
        except Exception as e:
            LOG.error(i18n._("Failed to monitor memory usage: %s") % e)
            return None
