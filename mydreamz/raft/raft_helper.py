

class RaftHelper:
    """
    """
    def __init__(self, service_store):
        """
        """
        self.service_store = service_store
        self.ip_port = self.service_store.get_ip_port()

    def get_partners_address(self, number_of_exchange, ip_port):
        """
        """
        starting_port = int(self.service_store.get_config_mgr().get_raft_config_mgr().get_port_starting_address())
        collector_port = int(self.service_store.get_config_mgr().get_raft_config_mgr().get_collector_port())

        partner_address = []
        ip_address = "127.0.0.1"
        next_port = starting_port

        for i in range(0, number_of_exchange):
           ip_address_port = "{}:{}".format(ip_address, next_port) 
           if ip_address_port == ip_port:
               continue
           partner_address.append(ip_address_port)
           next_port = next_port + 1

        partner_address.append("{}:{}".format(ip_address, collector_port))

        return partner_address


