from oslo_config import cfg

common_opts = [
    cfg.StrOpt('monitored_host',
               default='localhost',
               help='Host to be monitored'),
    cfg.IntOpt('monitoring_interval',
               default=60,
               help='Monitoring interval in seconds'),
    cfg.ListOpt('enabled_plugins',
                default=['cpu', 'memory', 'disk', 'os'],
                help='List of enabled monitoring plugins'),
    cfg.IntOpt('plugin_workers',
               default=4,
               help='Number of worker processes for plugins'),  # 添加插件工作进程数
]

i18n_opts = [
    cfg.StrOpt('language',
               default='en_US',
               help='Language for internationalization (e.g., en_US, zh_CN)')
]


def register_opts(conf):
    conf.register_opts(common_opts)
    conf.register_opts(i18n_opts)


def list_opts():
    return {
        None: common_opts,
        'i18n': i18n_opts
    }
