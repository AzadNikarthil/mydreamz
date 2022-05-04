import multiprocessing

class Worker(multiprocessing.Process):
    """
    """
    def __init__(self, **kwargs):
        """
        """
        multiprocessing.Process.__init__(self)
        self.exchange_name = kwargs['exchange_name']
        self.service_store = kwargs['store']
        self.ip_port = kwargs['ip_port']
        #print("Exchange name {}".format(self.exchange_name))

    def run(self):
        """
        """
        exchange = self.service_store.get_exchange_mgr().get_exchange_obj(self.exchange_name)
        exchange.run(self.ip_port)
    

class ProcessMgr:
    """
    """
    def __init__(self, service_store):
        """
        """
        self.service_store = service_store
        self.process = []

    def get_total_number_of_exchanges(self):
        """
        """
        return self.service_store.get_exchange_mgr().get_exchange_count()

    def get_starting_port(self):
        """
        """
        return self.service_store.get_config_mgr().get_raft_config_mgr().get_port_starting_address()

    def run(self):
        """
        """
        exchange_details = self.service_store.get_exchange_mgr().get_exchange_details()
        starting_port = int(self.get_starting_port())

        str_ip_port = "127.0.0.1:{}"

        for name, obj in exchange_details.items():
            ip_port = str_ip_port.format(starting_port)
            proc = Worker(exchange_name = name, store = self.service_store, ip_port = ip_port)
            self.process.append(proc)
            proc.start()
            starting_port = starting_port + 1

        for proc in self.process:
            proc.join()
