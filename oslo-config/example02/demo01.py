# -*-coding:utf-8-*-
"""
$ python demo01.py
DEFAULT.enabled_apis: ec2
DEFAULT.enabled_apis: osapi_compute
DEFAULT.bind_host: 0.0.0.0
DEFAULT.bind_port: 9292
rabbit.use_ssl: False
rabbit.host: localhost
rabbit.port: 5672

$ python demo01.py --bind_host=1.1.1.1 --rabbit-host=1.1.1.1 --rabbit-port=2222 --rabbit-nouse_ssl
DEFAULT.enabled_apis: ec2
DEFAULT.enabled_apis: osapi_compute
DEFAULT.bind_host: 1.1.1.1
DEFAULT.bind_port: 9292
rabbit.use_ssl: False
rabbit.host: 1.1.1.1
rabbit.port: 2222

$ python demo01.py --config-file=my.conf
DEFAULT.enabled_apis: ec2
DEFAULT.enabled_apis: osapi_keystone
DEFAULT.enabled_apis: osapi_compute
DEFAULT.bind_host: 196.168.1.111
DEFAULT.bind_port: 9999
rabbit.use_ssl: True
rabbit.host: 127.0.0.1
rabbit.port: 12345
"""
import sys
from oslo_config import cfg

from oslo_config import types

PortType = types.Integer(1, 65535)
# 声明配置项模式
# 单个配置项模式
enabled_apis_opt = cfg.ListOpt('enabled_apis',
                               default=['ec2', 'osapi_compute'],
                               help='List of APIs to enable by default.')
# 多个配置项组成一个模式
common_opts = [
    cfg.StrOpt('bind_host',
               default='0.0.0.0',
               help='IP/hostname to listen on.'),
    cfg.Opt('bind_port',
            type=PortType,
            default=9292,
            help='Port number to listen on.')
]
# 配置组
rabbit_group = cfg.OptGroup(
    name='rabbit',
    title='RabbitMQ options'
)
# 配置组中的模式，通常以配置组的名称为前缀（非必须）
rabbit_ssl_opt = cfg.BoolOpt('use_ssl',
                             default=False,
                             help='use ssl for connection')
# 配置组中的多配置项模式
rabbit_Opts = [
    cfg.StrOpt('host',
               default='localhost',
               help='IP/hostname to listen on.'),
    cfg.Opt('port',
            type=PortType,
            default=5672,
            help='Port number to listen on.')
]

# 创建对象CONF，用来充当容器
CONF = cfg.CONF

# 注册单个配置项模式
CONF.register_opt(enabled_apis_opt)
# 注册含有多个配置项的模式
CONF.register_opts(common_opts)
# 配置组必须在其组件被注册前注册！
CONF.register_group(rabbit_group)
# 注册配置组中含有多个配置项的模式，必须指明配置组
CONF.register_opts(rabbit_Opts, rabbit_group)
# 注册配置组中的单配置项模式，指明配置组
CONF.register_opt(rabbit_ssl_opt, rabbit_group)

# 注册单个配置项模式
CONF.register_cli_opt(enabled_apis_opt)
# 注册含有多个配置项的模式
CONF.register_cli_opts(common_opts)
# 注册配置组中含有多个配置项的模式，必须指明配置组
CONF.register_cli_opts(rabbit_Opts, rabbit_group)
# 注册配置组中的单配置项模式，指明配置组
CONF.register_cli_opt(rabbit_ssl_opt, rabbit_group)

# 接下来打印使用配置项的值
if __name__ == "__main__":
    # 调用容器对象，传入要解析的文件（可以多个）
    # CONF(default_config_files=['my.conf'])
    CONF(sys.argv[1:], project='my', version='1.0')
    # CONF(sys.argv[1:], project='my', version='1.0', default_config_files=["./my.conf"])

    for i in CONF.enabled_apis:
        print("DEFAULT.enabled_apis: " + i)

    print("DEFAULT.bind_host: " + CONF.bind_host)
    print("DEFAULT.bind_port: " + str(CONF.bind_port))
    print("rabbit.use_ssl: " + str(CONF.rabbit.use_ssl))
    print("rabbit.host: " + CONF.rabbit.host)
    print("rabbit.port: " + str(CONF.rabbit.port))
