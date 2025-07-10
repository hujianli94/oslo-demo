import os
import platform
import psutil

def import_module(module_name):
    """Dynamically import a module."""
    try:
        module = __import__(module_name, fromlist=['.'])
    except ImportError as e:
        raise ImportError("Unable to import module: %s, error: %s" %
                          (module_name, e))
    return module


def check_process_running(process_name):
    """Checks if a process is running."""
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] == process_name:
            return True
    return False

def get_os_type():
    """Gets the operating system type."""
    return platform.system()

def get_cpu_count():
    """Gets the number of CPUs."""
    return os.cpu_count()


