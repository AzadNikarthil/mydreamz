import traceback

from mydreamz.utility import GetServiceStore
from mydreamz.config import ConfigMgr
from mydreamz.process_mgr import ProcessMgr

class MyDreamz:
    """
    """

    def __init__(self):
        """
        """
        self.service_store_obj = GetServiceStore()
        self.configMgr = None
        self.processMgr = None
        self.log = None

    def initialize(self, ip_port):
        """
        """
        try:
            self.service_store_obj.initialize()
            self.configMgr = ConfigMgr(self.service_store_obj)
            self.log = self.service_store_obj.get_log_mgr().get_logger(__name__)
            self.log.debug("Hello world")
            self.log.error("Hello world")
            self.service_store_obj.set_ip_port(ip_port)
            self.configMgr.init()
            self.configMgr.parse()
            self.service_store_obj.set_config_mgr(self.configMgr)
            self.processMgr = ProcessMgr(self.service_store_obj)

        except Exception as ex:
            trace_back = traceback.format_exc()
            print("{}".format(trace_back))
            print("Exception {}".format(ex))

    def run(self):
        """
        """
        print("ip port {}".format(self.service_store_obj.get_ip_port()))
