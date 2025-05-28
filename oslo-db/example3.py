from oslo_config import cfg
from oslo_log import log
from oslo_db import options as db_options
from oslo_db.sqlalchemy import enginefacade
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

"""
需要先创建一个数据库
CREATE DATABASE users;
使用上下文管理器形式
使用 SQLAlchemy 的 declarative_base
使用 oslo_config 配置
使用 oslo_log 日志
"""

# 初始化logger
LOG = log.getLogger(__name__)

# 配置数据库选项
db_options.set_defaults(cfg.CONF)
CONF = cfg.CONF

# 注册日志选项
log.register_options(CONF)

# 使用 SQLAlchemy 的 declarative_base
Base = declarative_base()

# 从配置文件加载配置，这一步会解析命令行参数
CONF(default_config_files=['config.ini'])

# 设置日志
log.setup(CONF, __name__)


# 使用 enginefacade 上下文管理器形式
class MyContext(object):
    "User-defined context class."


context = MyContext()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    email = Column(String(255))


# 创建数据库引擎
engine = enginefacade.writer.get_engine()


# 初始化数据库（创建表）
def initialize_db():
    Base.metadata.create_all(engine)


# 在数据库中创建一个用户
def create_user(context, name, email):
    with enginefacade.writer.using(context) as session:
        session.add(User(name=name, email=email))


# 根据用户名查询用户
def get_user_by_name(context, name):
    with enginefacade.reader.using(context) as session:
        return session.query(User).filter(User.name == name).first()


def main():
    # 初始化数据库（创建表）
    initialize_db()

    # 创建一个新用户
    create_user(context, 'John Doe', 'johndoe@example.com')
    LOG.info(f'Created new user successfully.')

    # 根据用户名查询用户
    user = get_user_by_name(context, 'John Doe')
    if user:
        LOG.info(f'Found user: {user.name}, {user.email}')
    else:
        LOG.info('User not found.')


if __name__ == '__main__':
    main()
