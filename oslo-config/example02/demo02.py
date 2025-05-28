#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
$ python demo02.py
volume: ['hda 100G', 'hdb 150G', 'hdc 200G']
cli_host: 119.119.119.119
cli_port: 9292

$ python demo02.py --volume "hda 200G,hdb 250G,hdc 300G"
volume: ['hda 200G', 'hdb 250G', 'hdc 300G']
cli_host: 119.119.119.119
cli_port: 9292

$ python demo02.py --host 192.168.1.100 --port 8080
volume: ['hda 100G', 'hdb 150G', 'hdc 200G']
cli_host: 192.168.1.100
"""
import sys
from oslo_config import cfg
from oslo_config import types

PortType = types.Integer(1, 65535)

disk_list = ['hda 100G', 'hdb 150G', 'hdc 200G']
disk_opts = [cfg.MultiStrOpt('volume', default=disk_list, help='disk volumes in GB')]

cli_opts = [
    cfg.StrOpt('host',
               default='119.119.119.119',
               help='IP address to listen on.'),
    cfg.Opt('port',
            type=PortType,
            default=9292,
            help='Port number to listen on.')
]
# oslo.config 默认维护了一个 ConfigOpts 类型的全局变量 CONF。
# 注册参数，以及后续获取参数，都是可以通过 CONF。
CONF = cfg.CONF
# disk_opts 不是命令行参数，所以假如要覆盖默认值，只能通过配置文件改变！
# 注册的选项必须是可迭代的！否则会发生错误
CONF.register_opts(disk_opts)
CONF.register_cli_opts(cli_opts)

if __name__ == '__main__':
    CONF(sys.argv[1:])

    print("volume:", CONF.volume)
    print("cli_host:", CONF.host)
    print("cli_port:", CONF.port)
