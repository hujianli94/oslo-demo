from webob.dec import wsgify
from webob import exc



# 过滤器方法
@wsgify.middleware
def auth_filter(request, app):
    if request.headers.get('X-Auth-Token') != 'open-sesame':    # 验证请求头中的X-Auth-Token是否为open-sesame
        return exc.HTTPForbidden()      # 如果验证失败，返回HTTPForbidden错误
    return app(request)             # 验证成功，将请求传递给下一个过滤器或者应用


# 过滤器工厂方法
def filter_factory(global_config, **local_config):
    return auth_filter