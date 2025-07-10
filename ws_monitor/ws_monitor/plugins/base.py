# ws_monitor/plugins/base.py
import abc
import json
import logging

from ws_monitor import i18n

LOG = logging.getLogger(__name__)


class BaseMonitor(abc.ABC):
    """监控插件基类."""

    def __init__(self, conf):
        self.conf = conf

    @abc.abstractmethod
    def monitor(self):
        """监控方法，必须由子类实现."""
        pass

    def log_metric(self, metric_name, metric_value, unit=None):
        """记录监控指标."""
        plugin_name = self.__class__.__name__
        if isinstance(metric_value, dict):
            metric_value = json.dumps(metric_value, ensure_ascii=False, indent=2, sort_keys=True)
        # 构建日志消息，添加插件名称和更清晰的分隔符
        log_msg = "[Plugin: {plugin_name}] - {metric_name}: {metric_value}".format(
            plugin_name=plugin_name, metric_name=metric_name, metric_value=metric_value
        )
        if unit:
            log_msg += " {unit}".format(unit=unit)
        # 使用更美观的分隔线
        separator = "✦" * 80
        formatted_log = "{separator}\n{log_msg}\n{separator}".format(separator=separator, log_msg=log_msg)
        LOG.info(formatted_log)
