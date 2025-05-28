#!/usr/bin/env python3
# -*- coding:utf8 -*-
import sys
from oslo_config import cfg
from oslo_config import types

"""
$ python demo02.py
Config file used: ['settings.conf']
bind_host: 192.168.1.111, bind_port: 9999

$ python demo02.py --config-file=settings.conf
Config file used: ['settings.conf']
bind_host: 192.168.1.111, bind_port: 9999

$ python demo02.py --bind_host=11.1.1.1 --bind_port=222
Config file used: ['settings.conf']
bind_host: 11.1.1.1, bind_port: 222
"""

# 定义端口类型的验证器
PortType = types.Integer(1, 65535)

# 定义参数
common_opts = [
    cfg.StrOpt('bind_host',
               default='0.0.0.0',
               help='IP address to listen on.'),
    cfg.Opt('bind_port',
            type=PortType,
            default=9292,
            help='Port number to listen on.')
]


def main():
    # 定义configOpts实例还可以通过  conf = cfg.ConfigOpts()
    conf = cfg.CONF
    # 注册 命令和配置项
    conf.register_cli_opts(common_opts)
    conf.register_opts(common_opts)

    # 获取参数，默认配置也可以通过--config-file来指定
    conf(args=sys.argv[1:], default_config_files=['settings.conf'])
    # 打印配置文件路径以确认是否正确读取
    print("Config file used:", conf.config_file)
    print('bind_host: {}, bind_port: {}'.format(conf.bind_host, conf.bind_port))


if __name__ == '__main__':
    main()
