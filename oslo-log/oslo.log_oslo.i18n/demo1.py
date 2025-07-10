#!/usr/bin/env python3
# -*- coding:utf8 -*-
"""
A usage example of Oslo Logging with Oslo i18n.
This example requires the following package to be installed.
$ pip install oslo.log
$ pip install oslo.i18n
"""

from oslo_config import cfg
from oslo_log import log as logging
import i18n as u

LOG = logging.getLogger(__name__)
CONF = cfg.CONF
DOMAIN = 'demo'


def prepare():
    logging.register_options(CONF)
    extra_log_level_defaults = [
        'dogpile=INFO',
        'routes=INFO'
    ]
    logging.set_defaults(
        default_log_levels=logging.get_default_log_levels() +
                           extra_log_level_defaults)

    logging.setup(CONF, DOMAIN)


if __name__ == '__main__':
    prepare()
    LOG.info(u._LI("Welcome to Oslo Logging"))
    LOG.debug("A debugging message")  # Debug messages are not translated
    LOG.warning(u._LW("A warning occurred"))
    LOG.error(u._LE("An error occurred"))
    try:
        raise Exception(u._("This is exceptional"))
    except Exception:
        LOG.exception(u._LE("An Exception occurred"))
