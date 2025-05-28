from oslo_serialization import jsonutils

"""
oslo_serialization.jsonutils 提供了 JSON 序列化和反序列化的功能。
"""

# 序列化字典为 JSON 字符串
data = {'a': 'b'}
json_str = jsonutils.dumps(data)
print(f"Serialized JSON string: {json_str}")

# 反序列化 JSON 字符串为字典
deserialized_data = jsonutils.loads(json_str)
print(f"Deserialized data: {deserialized_data}")

# 从文件对象中加载 JSON 数据
jsontext = '{"a": "\u0442\u044d\u0441\u0442"}'
import io

fp = io.BytesIO(jsontext.encode('utf-8'))
result = jsonutils.load(fp, encoding='utf-8')
print(f"Loaded data from file: {result}")
