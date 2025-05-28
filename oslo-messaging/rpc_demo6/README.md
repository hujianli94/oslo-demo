# rabbitmq docker

## 安装

docker run
```shell
docker run -d --hostname rabbitmq --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management
```

docker-compose.yaml

```yml
version: '3'

services:
  rabbitmq:
    image: rabbitmq:management-alpine
    ports:
      - 5672:5672
      - 15672:15672
    volumes:
      - ./data:/var/lib/rabbitmq
    environment:
      RABBITMQ_DEFAULT_VHOST: myRabbit
      RABBITMQ_DEFAULT_USER: admin
      RABBITMQ_DEFAULT_PASS: admin
```


## rabbitmq 创建 guest 用户
```shell

# 创建用户
rabbitmqctl add_user guest guest
rabbitmqctl set_user_tags guest administrator
# 创建虚拟主机
rabbitmqctl add_vhost /
rabbitmqctl add_vhost myRabbit
# 设置用户权限
rabbitmqctl set_permissions -p / guest ".*" ".*" ".*"
rabbitmqctl set_permissions -p myRabbit guest ".*" ".*" ".*"

# 移除权限
rabbitmqctl delete_user guest # 删除用户
rabbitmqctl delete_vhost /
rabbitmqctl delete_vhost myRabbit
rabbitmqctl clear_permissions -p / guest # 清除权限

# 查看用户
rabbitmqctl list_users
# 查看虚拟主机
rabbitmqctl list_vhosts
# 查看权限
rabbitmqctl list_permissions -p /
```



## 说明
一个简单的 RPC 服务端和客户端示例，使用 RabbitMQ 作为消息队列。客户端发送计算请求，服务端接收请求并计算结果，然后将结果返回给客户端。

### 目录结构

```shell
.rpc_demo6/
├── rpc_utils.py         # 公共工具函数（get_rpc_transport 等）
├── rpc_service.py       # 新增：RpcService 类定义
├── rpc-server.py        # 使用 RpcService 启动服务
├── rpc-client.py        # 已重构：使用 rpc_utils
├── log.py               # 日志配置
└── settings.cfg         # 配置文件
```