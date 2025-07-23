#!/usr/bin/env python3
# -*- coding:utf8 -*-
from oslo_config import cfg
from oslo_log import log as logging

CONF = cfg.CONF
DOMAIN = 'demo'

logging.register_options(CONF)
logging.setup(CONF, DOMAIN)

for log_k_v in  CONF.items():
    print(log_k_v)


"""
('config_source', [])
('shell_completion', None)
('debug', False)
('log_config_append', None)
('log_date_format', '%Y-%m-%d %H:%M:%S')
('log_file', None)
('log_dir', None)
('watch_log_file', False)
('use_syslog', False)
('use_journal', False)
('syslog_log_facility', 'LOG_USER')
('use_json', False)
('use_stderr', False)
('use_eventlog', False)
('log_color', False)
('log_rotate_interval', 1)
('log_rotate_interval_type', 'days')
('max_logfile_count', 30)
('max_logfile_size_mb', 200)
('log_rotation_type', 'none')
('logging_context_format_string', '%(asctime)s.%(msecs)03d %(process)d %(levelname)s %(name)s [%(global_request_id)s %(request_id)s %(user_identity)s] %(instance)s%(message)s')
('logging_default_format_string', '%(asctime)s.%(msecs)03d %(process)d %(levelname)s %(name)s [-] %(instance)s%(message)s')
('logging_debug_format_suffix', '%(funcName)s %(pathname)s:%(lineno)d')
('logging_exception_prefix', '%(asctime)s.%(msecs)03d %(process)d ERROR %(name)s %(instance)s')
('logging_user_identity_format', '%(user)s %(project)s %(domain)s %(system_scope)s %(user_domain)s %(project_domain)s')
('default_log_levels', ['amqp=WARN', 'amqplib=WARN', 'boto=WARN', 'qpid=WARN', 'sqlalchemy=WARN', 'suds=INFO', 'oslo.messaging=INFO', 'oslo_messaging=INFO', 'iso8601=WARN', 'requests.packages.urllib3.connectionpool=WARN', 'urllib3.connectionpool=WARN', 'websocket=WARN', 'requests.packages.urllib3.util.retry=WARN', 'urllib3.util.retry=WARN', 'keystonemiddleware=WARN', 'routes.middleware=WARN', 'stevedore=WARN', 'taskflow=WARN', 'keystoneauth=WARN', 'oslo.cache=INFO', 'oslo_policy=INFO', 'dogpile.core.dogpile=INFO'])
('publish_errors', False)
('instance_format', '[instance: %(uuid)s] ')
('instance_uuid_format', '[instance: %(uuid)s] ')
('rate_limit_interval', 0)
('rate_limit_burst', 0)
('rate_limit_except_level', 'CRITICAL')
"""