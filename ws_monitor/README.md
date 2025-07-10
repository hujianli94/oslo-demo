# ws-monitor

一个简单且可扩展的监控工具。

## 介绍

“ws-monitor”是专为监控系统资源而设计的命令行工具。

它提供了一个基于插件的架构，可以轻松扩展其功能并添加对监控不同指标的支持。

它利用“oslo.config”、“oslo.log”、“oslo.context”、“oslo.i18n”、"oslo.service"和“psutil”来提供强大而灵活的监控解决方案。

## 功能

* **基于插件的架构：** 通过创建新的插件轻松扩展功能。
* **可配置：** 通过配置文件配置监控行为。
* **国际化 （i18n）:** 支持多种语言。
* **日志记录：** 用于调试和审计的全面日志记录。
* **资源监控：** 监控 CPU、内存、磁盘和作系统信息（可通过插件扩展）。

## 安装

### 依赖

* Python 3.6 or higher
* pip (Python package installer)

### 步骤

```bash
git clone <repository_url>  # Replace <repository_url> with the actual URL
cd ws-monitor

python3 -m venv .venv
source .venv/bin/activate  # On Linux/macOS
# .venv\Scripts\activate  # On Windows

#pip install -r requirements.txt  # If a requirements.txt file exists
#pip install .  # Install the ws-monitor package

pip install oslo.config oslo.log oslo.context oslo.i18n psutil
python setup.py install  # If using setup.py
```

## 使用

```shell
# 使用默认配置
ws_monitor

# 使用配置文件
ws_monitor --config-file etc/ws_monitor.conf
```

## Plugin 扩展

创建新插件

在 `ws_monitor/plugins/` 目录中创建一个新的插件文件（例如，`ws_monitor/plugins/my_plugin.py`）。
创建一个继承自 `ws_monitor.plugins.base.BaseMonitor` 的类。
实现 `monitor()` 方法。此方法应包含用于监视所需资源的逻辑。
使用 `self.log_metric()` 方法 记录监控结果。

Example:

```python
import logging
import psutil  # Example: If you need psutil

from ws_monitor.plugins import base
from ws_monitor import i18n

LOG = logging.getLogger(__name__)


class MyPluginMonitor(base.BaseMonitor):
    """My custom monitoring plugin."""

    def monitor(self):
        """Monitors a custom metric."""
        try:
            # Add your monitoring logic here
            process_count = len(psutil.pids())
            self.log_metric(i18n._("Number of Processes"), process_count)
        except Exception as e:
            LOG.error(i18n._("Failed to monitor my metric: %s") % e)
```

## 贡献代码

1. Fork 这个仓库。
2. 创建一个新的分支。
3. 实现你的功能。
4. 编写测试用例。
5. 提交你的代码。
6. 向本仓库提交一个 Pull Request。
7. 等待审核。
8. 完成。
