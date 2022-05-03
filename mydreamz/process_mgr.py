import multiprocessing

class Worker(multiprocessing.Process):
    """
    """
    def __init__(self, **kwargs):
        """
        """
        multiprocessing.Process.__init__(self)

    def run(self):
        """
        """
    

class ProcessMgr:
    """
    """
    def __init__(self, service_store):
        """
        """
        self.service_store = service_store

    def get_total_number_of_exchanges(self):
        """
        """
        return self.service_store.get_exchange_mgr().get_exchange_count()

    def get_starting_port():
        """
        """
        return self.service_store.get_raft_config_mgr().get_port_starting_address()

    def run():
        """
        """

