#!/usr/bin/env python3
# -*- coding:utf8 -*-
from oslo_cache import core as cache
from oslo_config import cfg
from oslo_log import log as logging
import functools

LOG = logging.getLogger(__name__)

CONF = cfg.CONF

# 注册配置选项
caching = cfg.BoolOpt('caching', default=True)
cache_time = cfg.IntOpt('cache_time', default=3600)
CONF.register_opts([caching, cache_time], "feature-name")

# 使用正确的组名访问配置项
_CACHE_TIME = CONF["feature-name"].cache_time

# 初始化 oslo.cache
cache.configure(CONF)
example_cache_region = cache.create_region()

# 加载配置文件
CONF(default_config_files=['settings.conf'])

WEEK = 60 * 60 * 24 * 7


class CacheClient(object):
    """
    封装了对数据的缓存操作。该类包含一个region属性保存CacheRegion对象，而对数据的缓存、获取、删除等操作具体是通过CacheRegion对象来实现的。
    """

    def __init__(self, region):
        self.region = region

    def get(self, key):
        value = self.region.get(key)
        if value == cache.NO_VALUE:
            return None
        return value

    def get_or_create(self, key, creator):
        return self.region.get_or_create(key, creator)

    def set(self, key, value):
        return self.region.set(key, value)

    def add(self, key, value):
        return self.region.get_or_create(key, lambda: value)

    def delete(self, key):
        return self.region.delete(key)

    def get_multi(self, keys):
        values = self.region.get_multi(keys)
        return [None if value is cache.NO_VALUE else value for value in values]

    def delete_multi(self, keys):
        return self.region.delete_multi(keys)


def _get_default_cache_region(expiration_time):
    """
    使用默认的后端缓存实现
    """
    region = cache.create_region()
    if expiration_time != 0:
        CONF.cache.expiration_time = expiration_time
    try:
        cache.configure_cache_region(CONF, region)
    except Exception as e:
        LOG.error(f"Failed to configure default cache region: {e}")
        raise
    return region


def _get_custom_cache_region(expiration_time=WEEK,
                             backend=None,
                             url=None):
    """
    可以自己指定后端缓存的实现
    """

    region = cache.create_region()
    region_params = {}
    if expiration_time != 0:
        region_params['expiration_time'] = expiration_time

    if backend == 'oslo_cache.dict':
        region_params['arguments'] = {'expiration_time': expiration_time}
    elif backend == 'dogpile.cache.memcached':
        if not url:
            raise ValueError("For 'dogpile.cache.memcached' backend, 'url' parameter must be specified.")
        region_params['arguments'] = {'url': url}
    else:
        raise RuntimeError('Old style configuration can use only dictionary or memcached backends')

    try:
        region.configure(backend, **region_params)
    except Exception as e:
        LOG.error(f"Failed to configure custom cache region: {e}")
        raise
    return region


def _warn_if_null_backend():
    """
    检查后端缓存backend是否为空
    """
    if CONF.cache.backend == 'dogpile.cache.null':
        LOG.warning("Cache enabled with backend dogpile.cache.null.")


def get_memcached_client(expiration_time=0):
    """
    创建了一个后端缓存为Memcache的CacheClient对象
    """
    # If the operator has [cache]/enabled flag on then we let oslo_cache
    # configure the region from the configuration settings
    if CONF.cache.enabled and CONF.cache.memcache_servers:
        _warn_if_null_backend()
        return CacheClient(
            _get_default_cache_region(expiration_time=expiration_time))
    return None


def get_client(expiration_time=0):
    """
    创建了一个后端缓存为dictionary的CacheClient对象。
    """
    # If the operator has [cache]/enabled flag on then we let oslo_cache
    # configure the region from configuration settings.
    if CONF.cache.enabled:
        _warn_if_null_backend()
        return CacheClient(
            _get_default_cache_region(expiration_time=expiration_time))
    # If [cache]/enabled flag is off, we use the dictionary backend
    return CacheClient(
        _get_custom_cache_region(expiration_time=expiration_time,
                                 backend='oslo_cache.dict'))


def memoize(func):
    """
    缓存装饰器，用于缓存函数的返回值
    """
    client = get_client()

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        key = f"{func.__name__}:{args}:{kwargs}"
        result = client.get(key)
        if result is None:
            result = func(*args, **kwargs)
            client.set(key, result)
        return result

    return wrapper


@memoize
def expensive_operation(x):
    print(f"Calculating result for {x}")
    return x * x


if __name__ == '__main__':
    # 测试
    print(expensive_operation(5))  # 第一次计算
    print(expensive_operation(5))  # 从缓存获取