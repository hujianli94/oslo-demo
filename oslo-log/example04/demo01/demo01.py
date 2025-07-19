# -*- coding: utf-8 -*-

import os
from oslo_config import cfg
from oslo_log import log as logging


# Initialize the configuration object
CONF = cfg.ConfigOpts()


def register_cli_opts():
    CONF.register_cli_opt(
        cfg.BoolOpt("verbose", default=False, help="Enable verbose logging")
    )


register_cli_opts()


# Let oslo_log register its default configuration options
logging.register_options(CONF)


# Parse the configuration file
def parse_config():
    # Get the directory of the current script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    config_file_path = os.path.join(current_dir, "settings.conf")
    if os.path.exists(config_file_path):
        # Ensure the correct configuration file is loaded
        CONF(default_config_files=[config_file_path])
    else:
        raise FileNotFoundError("{} not found".format(config_file_path))


# Main program
if __name__ == "__main__":
    # Read the configuration file
    parse_config()
    DOMAIN = "demo"

    # Print configuration items to confirm if the configuration file is loaded correctly
    print("debug: {}".format(CONF.debug))
    print("verbose: {}".format(CONF.verbose))
    print("log_file: {}".format(CONF.log_file))
    print("log_dir: {}".format(CONF.log_dir))
    print("log_date_format: {}".format(CONF.log_date_format))
    print(
        "logging_context_format_string: {}".format(CONF.logging_context_format_string)
    )
    print("use_stderr: {}".format(CONF.use_stderr))
    print("default_log_levels: {}".format(CONF.default_log_levels))
    print("instance_format: {}".format(CONF.instance_format))

    # Configure logging
    logging.setup(CONF, DOMAIN)

    # Get the logger
    logger = logging.getLogger(__name__)
    # 根据配置动态设置日志级别
    if CONF.debug:
        logger.setLevel(logging.DEBUG)
    elif CONF.verbose:
        logger.setLevel(logging.INFO)
    else:
        logger.setLevel(logging.WARNING)

    # Use the logger
    logger.debug("This is a debug message.")
    logger.info("This is an info message.")
    logger.warning("This is a warning message.")
    logger.error("This is an error message.")
