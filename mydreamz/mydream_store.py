from mydreamz.log_mgr import LogMgr
from mydreamz.db.mongodb_util import DBUtil

class _ServiceStore:
    """
    """

    class __ServiceStore:
        """
        """
        def __init__(self):
            """ """
            pass

        def initialize(self):
            """ """
            self.config_mgr = None
            self.ip_port = None
            self.exchangeMgr = None
            self.db = DBUtil()
            self.neo4j = None
            self.log_mgr = LogMgr()

        def __str__(self):
            return "<__ServiceStore obj>"

    instance = None

    def __init__(self):
        if not _ServiceStore.instance:
            _ServiceStore.instance = _ServiceStore.__ServiceStore()

    def __getattr__(self, name):
        return getattr(_ServiceStore.instance, name)

ServiceStore = _ServiceStore()

def initialize():
    """
    """
    ServiceStore.initialize()

def set_ip_port(ip_port):
    """
    """
    ServiceStore.ip_port = ip_port
 
def set_config_mgr(config):
    """
    """
    ServiceStore.config_mgr = config
 
def set_db_util(db):
    """
    """
    ServiceStore.db = db

def set_neo4j_util(db):
    """
    """
    ServiceStore.neo4j = db


def set_exchange_mgr(exchange_mgr):
    """
    """
    ServiceStore.exchangeMgr = exchange_mgr
     
def get_db_util():
    """
    """
    return ServiceStore.db

def get_neo4j_util():
    """
    """
    return ServiceStore.neo4j


def get_config_mgr():
    """
    """
    return ServiceStore.config_mgr

def get_ip_port():
    """
    """
    return ServiceStore.ip_port


def get_log_mgr():
    """
    """
    return ServiceStore.log_mgr

def get_exchange_mgr():
    """
    """
    return ServiceStore.exchangeMgr
