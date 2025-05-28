#!/usr/bin/env python3
# -*- coding:utf8 -*-
from oslo_cache import core as cache
from oslo_config import cfg

# 1. 注册配置选项
CONF = cfg.CONF
CONF.register_opts([
    cfg.BoolOpt('caching', default=True),
    cfg.IntOpt('cache_time', default=3600),
], "feature-name")

# 2. 初始化oslo.cache
cache.configure(CONF)

# 3. 创建缓存区域
example_cache_region = cache.create_region()

# 4. 获取缓存装饰器
MEMOIZE = cache.get_memoization_decorator(
    CONF, example_cache_region, "feature-name")

# 5. 加载配置文件（这里可以替换为实际的配置文件路径）
CONF(['--config-file', 'settings.conf'])

# 6. 配置缓存区域（必须在加载配置文件后调用）
cache.configure_cache_region(CONF, example_cache_region)


# 7. 使用装饰器
@MEMOIZE
def expensive_operation(x):
    print(f"Calculating result for {x}")
    return x * x


if __name__ == '__main__':
    # 测试
    print(expensive_operation(5))  # 第一次计算
    print(expensive_operation(5))  # 从缓存获取
