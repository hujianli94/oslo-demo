import platform
import logging

from ws_monitor.plugins import base
from ws_monitor import i18n

LOG = logging.getLogger(__name__)


class OsMonitor(base.BaseMonitor):
    """操作系统信息插件."""

    def monitor(self):
        """获取并记录操作系统信息."""
        try:
            os_info_dict = {
                "system": platform.system(),
                "node": platform.node(),
                "release": platform.release(),
                "version": platform.version(),
                "machine": platform.machine(),
                "processor": platform.processor()
            }
            self.log_metric("os_info", os_info_dict)
        except Exception as e:
            LOG.error(i18n._("Failed to get OS info: %s") % e)
            return None
