#!/usr/bin/env python
# -*- coding: utf-8 -*-
from oslo_config import cfg
from oslo_log import log
from oslo_db import options as db_options
from oslo_db.sqlalchemy import enginefacade
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.exc import SQLAlchemyError

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


# 使用 enginefacade 装饰器形式
@enginefacade.transaction_context_provider
class MyContext(object):
    """User-defined context class."""


# 使用引擎和会话管理
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
    """初始化数据库，创建表格"""
    Base.metadata.create_all(engine)
    LOG.info("Database initialized successfully.")


# 在数据库中创建一个用户
@enginefacade.writer
def create_user(context, name, email):
    """创建新用户"""
    try:
        user = User(name=name, email=email)
        context.session.add(user)
        LOG.info(f'User {name} created successfully.')
    except SQLAlchemyError as e:
        LOG.error(f"Failed to create user: {e}")
        raise


# 根据用户名查询用户
@enginefacade.reader
def get_user_by_name(context, name):
    """根据用户名查询用户"""
    try:
        return context.session.query(User).filter(User.name == name).first()
    except SQLAlchemyError as e:
        LOG.error(f"Failed to get user by name: {e}")
        raise


# 根据邮箱查询用户
@enginefacade.reader
def get_user_by_email(context, email):
    """根据邮箱查询用户"""
    try:
        return context.session.query(User).filter(User.email == email).first()
    except SQLAlchemyError as e:
        LOG.error(f"Failed to get user by email: {e}")
        raise


# 获取所有用户
@enginefacade.reader
def get_all_users(context):
    """获取所有用户"""
    try:
        return context.session.query(User).all()
    except SQLAlchemyError as e:
        LOG.error(f"Failed to get all users: {e}")
        raise


# 更新用户信息
@enginefacade.writer
def update_user(context, user_id, name=None, email=None):
    """更新用户信息"""
    try:
        user = context.session.query(User).filter(User.id == user_id).first()
        if user:
            if name:
                user.name = name
            if email:
                user.email = email
            context.session.commit()
            LOG.info(f'User {user_id} updated successfully.')
            return True
        else:
            LOG.info(f'User with ID {user_id} not found.')
            return False
    except SQLAlchemyError as e:
        LOG.error(f"Failed to update user {user_id}: {e}")
        raise


# 删除用户
@enginefacade.writer
def delete_user(context, user_id):
    """删除用户"""
    try:
        user = context.session.query(User).filter(User.id == user_id).first()
        if user:
            context.session.delete(user)
            LOG.info(f'User {user_id} deleted successfully.')
            return True
        else:
            LOG.info(f'User with ID {user_id} not found.')
            return False
    except SQLAlchemyError as e:
        LOG.error(f"Failed to delete user {user_id}: {e}")
        raise


def main():
    """主程序"""
    # 初始化数据库（创建表）
    initialize_db()

    # 创建一个新用户
    create_user(context, 'hujl', 'hujl@example.com')

    # 根据用户名查询用户
    user = get_user_by_name(context, 'hujl')
    if user:
        LOG.info(f'Found user: {user.name}, {user.email}')
    else:
        LOG.info('User not found.')

    # 更新用户信息
    if update_user(context, user.id, name='hujl_updated', email='hujl_updated@example.com'):
        LOG.info('User updated successfully.')

    # # 删除用户
    # if delete_user(context, user.id):
    #     LOG.info('User deleted successfully.')


if __name__ == "__main__":
    main()
