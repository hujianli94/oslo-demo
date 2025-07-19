#!/usr/bin/env python3
# -*- coding:utf8 -*-
import logging


def setup_logger(
    name,
    log_level="INFO",
    log_format=None,
    datefmt=None,
):
    """
    设置并返回一个日志记录器，适用于所有服务类模块。

    :param name: 日志记录器的名称（通常使用 __name__)
    :param log_level: 日志级别（默认为 'INFO')
    :param log_format: 日志格式
    :param datefmt: 时间格式
    :return: 配置好的日志记录器对象
    """
    # 创建日志记录器
    logger = logging.getLogger(name)

    # 设置日志级别
    logger.setLevel(log_level)
    log_format = log_format or "%(asctime)s %(levelname)8s: %(message)s"
    datefmt = datefmt or "%Y-%m-%d %H:%M:%S"

    # 创建日志格式化器
    formatter = logging.Formatter(log_format, datefmt=datefmt)

    # 创建一个控制台日志处理器
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # 添加处理器到日志记录器
    if not logger.hasHandlers():  # 防止重复添加处理器
        logger.addHandler(console_handler)

    return logger


if __name__ == "__main__":
    logger = setup_logger(__name__)
    logger.debug("This is a debug message.")
    logger.info("This is a info message.")
    logger.warning("This is a warning message.")
    logger.error("This is an error message.")
