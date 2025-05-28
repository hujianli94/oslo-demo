#!/usr/bin/env python3
# -*- coding:utf8 -*-
from oslo_utils import uuidutils


## 测试 UUID
valid_uuid = '550e8400-e29b-41d4-a716-446655440000'
is_valid_uuid = uuidutils.is_uuid_like(valid_uuid)
print(f"Is {valid_uuid} a valid UUID? {is_valid_uuid}")

# 测试无效的 UUID
invalid_uuid = 'not_a_uuid'
is_invalid_uuid = uuidutils.is_uuid_like(invalid_uuid)
print(f"Is {invalid_uuid} a valid UUID? {is_invalid_uuid}")



## 测试文件是否为 JSON 类型
import os
from oslo_utils import fileutils

# 创建一个临时 JSON 文件
test_json_content = '{"key": "value"}'
test_json_file = 'test.json'
with open(test_json_file, 'w') as f:
    f.write(test_json_content)

# 检查文件是否为 JSON 类型
is_json_result = fileutils.is_json(test_json_file)
print(f"Is {test_json_file} a JSON file? {is_json_result}")

# 删除临时文件
os.remove(test_json_file)

