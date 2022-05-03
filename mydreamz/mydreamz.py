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
        self.configMgr = ConfigMgr()
        self.processMgr = None

    def initialize(self):
        """
        """
        try:
            self.service_store_obj.initialize()
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
        pass