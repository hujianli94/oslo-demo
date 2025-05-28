#!/usr/bin/env python
# -*- coding:utf8 -*-
"""A syntax example of Python Logging"""

import logging

LOG = logging.getLogger(__name__)
formatter = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
level = logging.INFO
logging.basicConfig(level=level, format=formatter)

LOG.info("Python Standard Logging")
LOG.warning("Python Standard Logging")
LOG.error("Python Standard Logging")
