# api.py
"""
Public API interface for generic RPC system
"""
import threading
import time
import config
import manager

# Global RPC manager instance
_rpc_manager = None
_lock = threading.Lock()


def get_rpc_manager(config_file=None):
    """Get global RPC manager instance"""
    global _rpc_manager
    with _lock:
        if _rpc_manager is None:
            conf = config.load_config(config_file)
            transport = config.get_transport()
            _rpc_manager = manager.RPCManager(
                transport=transport,
                host=conf.host
            )
        return _rpc_manager


def init_rpc(config_file=None):
    """Initialize RPC system"""
    return get_rpc_manager(config_file)


# Convenient functions
def rpc_call(topic, method, context=None, version='1.0', **kwargs):
    """Global RPC synchronous call function"""
    rpc_manager = get_rpc_manager()
    return rpc_manager.call(topic, method, context, version, **kwargs)


def rpc_cast(topic, method, context=None, version='1.0', **kwargs):
    """Global RPC asynchronous call function"""
    rpc_manager = get_rpc_manager()
    return rpc_manager.cast(topic, method, context, version, **kwargs)
