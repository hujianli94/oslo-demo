#!/usr/bin/env python3
# -*- coding:utf8 -*-
from oslo_serialization import jsonutils

# 定义一个简单的 Python 对象
data = {
    'name': 'OpenStack',
    'version': '2025.03',
    'active': True,
    'components': ['Nova', 'Neutron', 'Cinder']
}

# 将 Python 对象序列化为 JSON 字符串
json_data = jsonutils.dumps(data)
print("Serialized JSON Data:", json_data)

# 将 JSON 字符串反序列化回 Python 对象
deserialized_data = jsonutils.loads(json_data)
print("Deserialized Python Object:", deserialized_data)


# 从文件对象中加载 JSON 数据
jsontext = '{"a": "\u0442\u044d\u0441\u0442"}'
import io

fp = io.BytesIO(jsontext.encode('utf-8'))
result = jsonutils.load(fp, encoding='utf-8')
print(f"Loaded data from file: {result}")