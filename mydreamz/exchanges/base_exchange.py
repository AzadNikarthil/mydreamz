import time

from mydreamz.raft.raft_helper import RaftHelper
from mydreamz.raft.storage import Storage

class BaseExchange:
    """
    """

    def __init__(self, service_store):
        """
        """
        self.service_store = service_store
        self.exchange_obj = None
        self.name = None
        self.raft_helper = RaftHelper(self.service_store)
        self.exchange_mgr = self.service_store.get_exchange_mgr()

    def set_exchange_name(self, name):
        """
        """
        exchange_details = self.service_store.get_exchange_mgr().get_exchange_details()
        self.exchange_obj = exchange_details[name]
        self.name = name

    def get_coin_pair(self):
        """
        """
        return self.service_store.get_config_mgr().get_coin_pair()
    
    def run(self, ip_port):
        """
        """
        exchange_count = self.exchange_mgr.get_exchange_count()
        partner_address = self.raft_helper.get_partners_address(exchange_count, ip_port)
        self.storage = Storage(ip_port, partner_address)
        i = 0
        while True:
            try:
                ticker = self.exchange_obj.fetch_ticker(self.get_coin_pair()[0])
                if "last" in ticker:
                    #print("{} {}".format(self.name, ticker['last']))
                    self.storage.set(self.name, float(ticker['last']))
                elif "info" in ticker:
                    value_ticker = ticker['info']
                    if 'lastPrice' in value_ticker:
                        #print("{} {}".format(key, value_ticker['lastPrice']))
                        self.storage.set(self.name, float(value_ticker['last']))
                    elif 'last_price' in value_ticker:
                        #print("{} {}".format(key, value_ticker['last_price']))
                        self.storage.set(self.name, float(value_ticker['last_price']))
                    elif 'last' in value_ticker:
                        #print("{} {}".format(key, value_ticker['last']))
                        self.storage.set(self.name, float(value_ticker['last']))
            except Exception as ex:
                print("Exception : {} {}".format(self.name, str(ex)))
                time.sleep(1)
         
