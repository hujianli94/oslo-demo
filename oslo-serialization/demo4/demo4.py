#!/usr/bin/env python3
# -*- coding:utf8 -*-
"""
Base64 编码与解码
oslo_serialization.base64 提供了 Base64 编码和解码的功能。
"""

from oslo_serialization import base64

# Base64 编码为字节
encoded_bytes = base64.encode_as_bytes('text')
print(f"Base64 encoded bytes: {encoded_bytes}")

# Base64 编码为文本
encoded_text = base64.encode_as_text('text')
print(f"Base64 encoded text: {encoded_text}")

# Base64 解码为字节
decoded_bytes = base64.decode_as_bytes(encoded_bytes)
print(f"Base64 decoded bytes: {decoded_bytes}")

# Base64 解码为文本
decoded_text = base64.decode_as_text(encoded_text)
print(f"Base64 decoded text: {decoded_text}")