"""A file operation demo using Oslo Logging"""

from oslo_config import cfg
from oslo_log import log as logging

# 配置日志
CONF = cfg.CONF
DOMAIN = 'file_operation_demo'

# 注册日志选项
logging.register_options(CONF)

# 设置默认日志级别
extra_log_level_defaults = [
    'dogpile=INFO',
    'routes=INFO',
    # 添加以下行，将默认日志级别设置为 DEBUG
    'root=DEBUG'
]
logging.set_defaults(
    default_log_levels=logging.get_default_log_levels() + extra_log_level_defaults
)

# 初始化日志
logging.setup(CONF, DOMAIN)

# 获取日志记录器
LOG = logging.getLogger(__name__)



def write_to_file(file_path, content):
    try:
        LOG.info(f"Attempting to write content to file: {file_path}")
        with open(file_path, 'w') as file:
            file.write(content)
        LOG.info(f"Successfully wrote content to file: {file_path}")
    except Exception as e:
        LOG.error(f"Error writing to file {file_path}: {e}")


def read_from_file(file_path):
    try:
        LOG.info(f"Attempting to read content from file: {file_path}")
        with open(file_path, 'r') as file:
            content = file.read()
        LOG.info(f"Successfully read content from file: {file_path}")
        return content
    except Exception as e:
        LOG.error(f"Error reading from file {file_path}: {e}")
        return None


if __name__ == '__main__':
    file_path = 'test_file.txt'
    content_to_write = "This is a test content for the file operation demo."

    # 写入文件
    write_to_file(file_path, content_to_write)

    # 读取文件
    read_content = read_from_file(file_path)
    if read_content:
        # 确保日志级别为 DEBUG
        LOG.setLevel(logging.logging.DEBUG)
        LOG.debug(f"Read content: {read_content}")
