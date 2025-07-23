import os
import signal
from oslo_config import cfg
from oslo_log import log as logging
from oslo_service import service
from oslo_service import threadgroup

# 定义配置项
CONF = cfg.CONF
cli_opts = [
    cfg.StrOpt('host',
               default='localhost',
               help='Service host address'),
    cfg.IntOpt('port',
               default=9191,
               help='Service port'),
    cfg.BoolOpt("verbose",
                default=False,
                help="Enable verbose logging"),
]
CONF.register_cli_opts(cli_opts)
CONF.register_opts(cli_opts)

# 先注册 oslo_logging 的选项
logging.register_options(CONF)


class DemoService(service.Service):
    """示例服务类"""

    def __init__(self):
        super(DemoService, self).__init__()
        self.tg = threadgroup.ThreadGroup()
        self.running = False

        # 设置信号处理
        signal.signal(signal.SIGTERM, self.handle_signal)
        signal.signal(signal.SIGHUP, self.handle_signal)
        signal.signal(signal.SIGUSR1, self.handle_signal)

    def start(self):
        """启动服务"""
        self.running = True
        LOG.info("Starting demo service")
        self.tg.add_dynamic_timer(self._run_periodic,
                                  initial_delay=0,
                                  periodic_interval_max=5)

    def stop(self, graceful=True):
        """停止服务"""
        LOG.info("Stopping demo service")
        self.running = False
        self.tg.stop(graceful)
        super(DemoService, self).stop()

    def _run_periodic(self):
        """周期任务（每5秒执行一次）"""
        if self.running:
            LOG.info(f"Service running at {CONF.host}:{CONF.port}")
            LOG.debug("Debug mode enabled" if CONF.debug else "Debug mode disabled")
            return 5  # 返回下次执行间隔秒数

    def handle_signal(self, signum, frame):
        """信号处理器"""
        signame = {
            signal.SIGTERM: 'SIGTERM',
            signal.SIGHUP: 'SIGHUP',
            signal.SIGUSR1: 'SIGUSR1'
        }.get(signum, f'UNKNOWN({signum})')

        LOG.info(f"Received signal: {signame}")

        if signum == signal.SIGHUP:
            LOG.info("Reloading configuration")
            CONF.reload_config_files()
            LOG.info(f"New configuration: host={CONF.host}, port={CONF.port}, debug={CONF.debug}")
        elif signum == signal.SIGUSR1:
            LOG.info("Processing custom user signal")
        else:
            LOG.info("Shutting down")
            self.stop()


def prepare_service():
    """准备服务环境"""
    # 1. 现在 CONF 已经注册了所有选项，可以安全地解析配置
    CONF(default_config_files=['settings.conf'])
    DOMAIN = "demo_service"

    # 初始化 oslo_log
    logging.setup(CONF, DOMAIN)
    # Get the logger
    logger = logging.getLogger(__name__)
    # 根据配置动态设置日志级别
    if CONF.debug:
        logger.setLevel(logging.DEBUG)
    elif CONF.verbose:
        logger.setLevel(logging.INFO)
    else:
        logger.setLevel(logging.WARNING)
    return logger


def main():
    """启动服务"""
    global LOG
    LOG = prepare_service()

    launcher = service.launch(CONF, DemoService())
    LOG.info("Service started successfully. PID: %d", os.getpid())
    launcher.wait()


if __name__ == "__main__":
    main()
