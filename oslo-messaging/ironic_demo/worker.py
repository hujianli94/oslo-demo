#!/usr/bin/env python3
# client.py
"""
RPC Client implementation
"""
import api


def main():
    # 配置文件路径和主题名称
    config_file = 'settings.cfg'
    topic = 'demo-service'

    # print(f"Connecting to RPC service: {topic}")

    # 初始化 RPC 系统
    api.init_rpc(config_file)

    # 同步调用示例
    print("\n1. Testing hello method:")
    result = api.rpc_call(topic, 'hello', name='World')
    print(f'   Result: {result}')

    # 计算示例
    print("\n2. Testing calculate method (addition):")
    calc_result = api.rpc_call(topic, 'calculate', a=10, b=5, operation='add')
    print(f'   Result: 10 + 5 = {calc_result}')

    print("\n3. Testing calculate method (multiplication):")
    calc_result = api.rpc_call(topic, 'calculate', a=10, b=5, operation='multiply')
    print(f'   Result: 10 * 5 = {calc_result}')

    # 异步调用示例
    print("\n4. Testing async call backup_database method:")
    api.rpc_cast('demo-service', 'backup_database',
                 database_name='production_db',
                 backup_path='/backup/prod_20250528.sql')

    # 异步调用示例
    print("\n5. Testing async call system_health_check method:")
    api.rpc_cast('demo-service', 'system_health_check', check_type='full')


if __name__ == '__main__':
    import sys

    sys.exit(main())
