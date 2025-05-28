from oslo_config import cfg
from oslo_log import log as logging
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

"""
需要先创建一个数据库
CREATE DATABASE users;
"""

# 初始化logger
LOG = logging.getLogger(__name__)
DOMAIN = "demo"
# 配置文件设置
CONF = cfg.CONF
logging.register_options(CONF)
logging.setup(CONF, DOMAIN)

# 使用 SQLAlchemy 的 declarative_base
Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    email = Column(String(255))


db_group = cfg.StrOpt('connection', default='sqlite:///example.db', help='Database connection string')
CONF.register_opt(db_group, group='database')
# 从配置文件加载配置
CONF(default_config_files=['config.ini'])


# 配置数据库连接
def configure_db():
    # 从 oslo_config 获取数据库连接字符串
    db_url = CONF.database.connection

    # 创建引擎
    engine = create_engine(db_url)

    # 创建 session 工厂
    Session = sessionmaker(bind=engine)

    return engine, Session


# 初始化数据库（创建表）
def initialize_db(engine):
    Base.metadata.create_all(engine)


# 在数据库中创建一个用户
def create_user(session, name, email):
    user = User(name=name, email=email)
    session.add(user)
    session.commit()
    return user


# 根据用户名查询用户
def get_user_by_name(session, name):
    return session.query(User).filter(User.name == name).first()


def get_user_by_email(session, email):
    return session.query(User).filter(User.email == email).first()


def get_all_users(session):
    return session.query(User).all()


def update_user(session, user_id, name=None, email=None):
    user = session.query(User).filter(User.id == user_id).first()
    if user:
        if name:
            user.name = name
        if email:
            user.email = email
        session.commit()
        return True
    else:
        return False


def delete_user(session, user_id):
    user = session.query(User).filter(User.id == user_id).first()
    if user:
        session.delete(user)
        session.commit()
        return True
    else:
        return False


def main():
    # 配置数据库
    engine, Session = configure_db()

    # 初始化数据库（创建表）
    initialize_db(engine)

    # 创建一个会话
    session = Session()

    # 创建一个新用户
    new_user = create_user(session, 'John Doe', 'johndoe@example.com')
    LOG.info(f'Created new user: {new_user.name}, {new_user.email}')

    # 根据用户名查询用户
    user = get_user_by_name(session, 'John Doe')
    if user:
        LOG.info(f'Found user: {user.name}, {user.email}')
    else:
        LOG.info('User not found.')

    # 删除用户
    if delete_user(session, new_user.id):
        LOG.info(f'Deleted user with ID: {new_user.id}')
    else:
        LOG.info('User not found.')

    # 关闭会话
    session.close()


if __name__ == '__main__':
    main()
