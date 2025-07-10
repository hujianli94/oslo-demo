import psutil
import logging

from ws_monitor.plugins import base
from ws_monitor import i18n

LOG = logging.getLogger(__name__)


class CpuMonitor(base.BaseMonitor):
    """CPU 监控插件."""

    def monitor(self):
        """监控 CPU 使用率."""
        try:
            # 只调用一次 psutil.cpu_percent(interval=1)
            cpu_percentage = psutil.cpu_percent(interval=1)
            cpu_freq = psutil.cpu_freq()
            cpu_times = psutil.cpu_times()
            cpu_stats = psutil.cpu_stats()

            cpu_usage_dict = {
                "cpu_usage": cpu_percentage,
                "cpu_count": psutil.cpu_count(),
                "cpu_freq_current": cpu_freq.current if cpu_freq else None,
                "cpu_freq_min": cpu_freq.min if cpu_freq else None,
                "cpu_freq_max": cpu_freq.max if cpu_freq else None,
                "cpu_times_user": cpu_times.user,
                "cpu_times_system": cpu_times.system,
                "cpu_times_idle": cpu_times.idle,
                "cpu_stats_ctx_switches": cpu_stats.ctx_switches,
                "cpu_stats_interrupts": cpu_stats.interrupts,
                "cpu_stats_soft_interrupts": cpu_stats.soft_interrupts,
                "cpu_stats_syscalls": cpu_stats.syscalls
            }
            self.log_metric("cpu_usage", cpu_usage_dict)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess) as e:
            LOG.error(i18n._("Failed to monitor CPU usage due to process error: %s") % e)
        except Exception as e:
            LOG.error(i18n._("Failed to monitor CPU usage: %s") % e)
        return None
