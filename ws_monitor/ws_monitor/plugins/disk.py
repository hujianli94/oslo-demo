# ws_monitor/plugins/disk.py
import psutil
import logging

from ws_monitor.plugins import base
from ws_monitor import i18n

LOG = logging.getLogger(__name__)


class DiskMonitor(base.BaseMonitor):
    """磁盘监控插件."""

    def monitor(self):
        """监控磁盘使用情况."""
        try:
            disk = psutil.disk_usage('/')  # 监控根目录
            disk_usage_dict = {
                "total": "{:.2f} GB".format(disk.total / (1024 * 1024 * 1024)),
                "used": "{:.2f} GB".format(disk.used / (1024 * 1024 * 1024)),
                "free": "{:.2f} GB".format(disk.free / (1024 * 1024 * 1024)),
                "percent": "{} %".format(disk.percent),
            }
            self.log_metric("disk_usage", disk_usage_dict)
        except Exception as e:
            LOG.error(i18n._("Failed to monitor disk usage: %s") % e)
            return None
