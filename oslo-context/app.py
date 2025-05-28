#!/usr/bin/env python3
# -*- coding:utf8 -*-
from oslo_context import context
from oslo_log import log as logging
from flask import Flask, request, jsonify, g
import uuid

# 配置日志
LOG = logging.getLogger(__name__)
logging.set_defaults()


# 定义自定义的上下文类
class MyContext(context.RequestContext):
    def __init__(self, user_id, tenant_id, request_id, *args, **kwargs):
        super(MyContext, self).__init__(*args, **kwargs)
        self.user_id = user_id
        self.tenant_id = tenant_id
        self.request_id = request_id


# 请求ID生成函数
def generate_request_id():
    return str(uuid.uuid4())


# 日志记录函数
def log_context_info(ctxt):
    """根据上下文记录当前的用户、租户信息以及请求ID"""
    LOG.info(f"Request ID: {ctxt.request_id} | User ID: {ctxt.user_id} | Tenant ID: {ctxt.tenant_id}")


# Flask应用实例
app = Flask(__name__)


@app.before_request
def before_request():
    """在每个请求之前创建上下文"""
    try:
        # 假设从请求的 header 或其他来源获取用户和租户信息
        user_id = request.headers.get('X-User-Id', 'unknown_user')
        tenant_id = request.headers.get('X-Tenant-Id', 'unknown_tenant')

        # 创建唯一的请求ID
        request_id = generate_request_id()

        # 创建请求上下文实例
        ctxt = MyContext(user_id=user_id, tenant_id=tenant_id, request_id=request_id, is_admin=False)

        # 将上下文存储在 Flask 的 g 对象中，便于后续获取
        g.ctxt = ctxt

        # 在日志中记录上下文信息
        log_context_info(ctxt)
    except Exception as e:
        LOG.error(f"Failed to create context: {e}")
        return jsonify({'message': 'Internal server error'}), 500


@app.after_request
def after_request(response):
    """在每个请求之后记录上下文信息"""
    try:
        ctxt = g.ctxt
        LOG.info(f"Request ID: {ctxt.request_id} completed with status: {response.status_code}")
    except AttributeError as e:
        LOG.error(f"Context not found: {e}")
    return response


@app.route('/')
def index():
    """一个简单的示例接口"""
    try:
        ctxt = g.ctxt
        return jsonify({
            'message': f'Hello, User {ctxt.user_id} from Tenant {ctxt.tenant_id}',
            'request_id': ctxt.request_id
        })
    except Exception as e:
        LOG.error(f"Error in index: {e}")
        return jsonify({'message': 'Internal server error'}), 500


@app.route('/error')
def error():
    """模拟一个错误接口，用于测试异常日志"""
    try:
        ctxt = g.ctxt
        LOG.error(f"Request ID: {ctxt.request_id} encountered an error.")
        return jsonify({'message': 'Something went wrong!'}), 500
    except Exception as e:
        LOG.error(f"Failed to log error context: {e}")
        return jsonify({'message': 'Internal server error'}), 500


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
