# ws_monitor/cli.py
import logging
from oslo_config import cfg
from oslo_log import log as logging
from oslo_service import service
from oslo_service import systemd
from ws_monitor.conf import monitor as conf_monitor
from ws_monitor import context
from ws_monitor import i18n
from ws_monitor import app
from ws_monitor import version

CONF = cfg.CONF


def main(args=None, config_files=None):
    # 1. 注册配置选项 (合并注册)
    conf_monitor.register_opts(CONF)
    logging.register_options(CONF)

    # 2. 加载配置
    CONF(args=args, project='ws_monitor', default_config_files=config_files)

    # 3. 初始化日志
    logging.setup(CONF, 'ws_monitor')
    LOG = logging.getLogger(__name__)

    # 4. 启用国际化
    i18n.enable()

    LOG.info(i18n._("Starting ws-monitor..."))
    LOG.debug(i18n._("Configuration loaded: %s") % CONF.monitored_host)

    # 5. 创建上下文
    ctx = context.create_context()

    # 6. 打印版本信息
    LOG.info(i18n._("Version: ws-monitor %s") % version.version_string())  # 从version.py 中获取

    # 7. 启动服务
    try:
        # 创建 Service 对象
        monitor_service = app.MonitorService(CONF)
        # 启动服务
        launcher = service.launch(CONF, monitor_service, restart_method='mutate')
        # 等待服务停止
        launcher.wait()
        # 通知 systemd 服务已停止
        systemd.notify_once()
    except KeyboardInterrupt:
        LOG.info(i18n._("Monitor tool stopped."))
        systemd.notify_once()
    except Exception as e:
        LOG.exception(e)  # 记录异常
        raise  # 抛出异常


if __name__ == '__main__':
    main()
