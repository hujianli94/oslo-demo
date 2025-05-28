from oslo_serialization import jsonutils

"""
将对象转换为基本类型
jsonutils.to_primitive 方法可以将复杂对象转换为基本类型，便于 JSON 序列化。
"""

class MappingClass:
    def __init__(self):
        self.data = dict(a=1, b=2, c=3)

    def __getitem__(self, val):
        return self.data[val]

    def __iter__(self):
        return iter(self.data)

    def __len__(self):
        return len(self.data)


x = MappingClass()
p = jsonutils.to_primitive(x)
print(f"Primitive representation: {p}")
