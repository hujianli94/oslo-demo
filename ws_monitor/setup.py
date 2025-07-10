import os
from setuptools import setup, find_packages

NAME = 'ws_monitor'


# 读取 version.py 文件以获取版本信息
def get_version():
    version_file = os.path.join(NAME, 'version.py')
    with open(version_file) as f:
        exec(f.read())
    return locals()['__version__']


# 提取版本信息
VERSION = get_version()


def strip_comments(l):
    # strip comments and empty lines
    return l.split("#", 1)[0].strip()


def reqs(*f):
    # read requirements from file
    return list(
        filter(None, [strip_comments(l) for l in open(os.path.join(os.path.dirname(__file__), *f)).readlines()]))


README = os.path.join(os.path.dirname(__file__), "README.md")

setup(
    name=NAME,
    version=VERSION,
    description='A simple and extensible monitoring tool',
    long_description=open(README).read(),
    long_description_content_type='text/markdown',
    author='hu jianli',
    author_email='jianli.email@example.com',
    license='Apache License, Version 2.0',
    url='https://github.com/hujianli94/ws_monitor',
    packages=find_packages(),
    install_requires=[
        'oslo.config',
        'oslo.log',
        'oslo.context',
        'oslo.i18n',
        'oslo.service',
        'psutil',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    python_requires='>=3.8',
    entry_points={
        'console_scripts': [
            'ws_monitor= ws_monitor.cli:main',
        ],
    },
    data_files=[
        ('/etc/ws_monitor', ['etc/ws_monitor.conf']),
        ('/etc/systemd/system', ['etc/ws_monitor.service']),
    ],
)
