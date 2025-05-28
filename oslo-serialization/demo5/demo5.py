#!/usr/bin/env python
from oslo_serialization.serializer.base_serializer import BaseSerializer
from oslo_serialization import jsonutils
import datetime


class CustomMultiTypeSerializer(BaseSerializer):
    def __init__(self, default=jsonutils.to_primitive, encoding='utf-8'):
        self._default = default
        self._encoding = encoding

    def _custom_default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        # 可以根据需要添加更多的数据类型处理逻辑
        return self._default(obj)

    def dump(self, obj, fp):
        return jsonutils.dump(obj, fp, default=self._custom_default)

    def dump_as_bytes(self, obj):
        return jsonutils.dump_as_bytes(obj, default=self._custom_default,
                                       encoding=self._encoding)

    def load(self, fp):
        return jsonutils.load(fp, encoding=self._encoding)

    def load_from_bytes(self, s):
        return jsonutils.loads(s, encoding=self._encoding)


# 使用示例
if __name__ == "__main__":
    serializer = CustomMultiTypeSerializer()

    # 不同数据类型的对象
    data = {
        'name': 'Alice',
        'age': 25,
        'birth_date': datetime.datetime(1998, 5, 15)
    }

    # 序列化对象为字节字符串
    serialized_bytes = serializer.dump_as_bytes(data)
    print(f"Serialized bytes: {serialized_bytes}")

    # 从字节字符串中反序列化对象
    deserialized_data = serializer.load_from_bytes(serialized_bytes)
    print(f"Deserialized data: {deserialized_data}")
