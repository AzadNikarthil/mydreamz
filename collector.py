import time

from flask import Flask

from mydreamz.utility import GetServiceStore
from mydreamz.config import ConfigMgr
from mydreamz.raft.storage import Storage
from mydreamz.exchanges.exchange import exchange
from mydreamz.exchanges.exchange_mgr import ExchangeMgr
from mydreamz.raft.raft_helper import RaftHelper

app = Flask(__name__)

if __name__ == '__main__':
    service_store_obj = GetServiceStore()
    service_store_obj.initialize()
    configMgr = ConfigMgr(service_store_obj)
    configMgr.init()
    configMgr.parse()
    exchangeMgr = ExchangeMgr(service_store_obj)
    rafthelper = RaftHelper(service_store_obj)
    service_store_obj.set_exchange_mgr(exchangeMgr)
    service_store_obj.set_config_mgr(configMgr)
    exchange_count = exchangeMgr.get_exchange_count()
    raft_helper = RaftHelper(service_store_obj)
    collector_port = int(service_store_obj.get_config_mgr().get_raft_config_mgr().get_collector_port())
    ip_port = "127.0.0.1:{}".format(collector_port)
    partner_address = raft_helper.get_partners_address(exchange_count, ip_port)

    storage = Storage(ip_port, partner_address)
       
    @app.route('/')
    def exchange_rate():
        """
        """
        data = {}
        print("request received")
        try:
            for key, value in exchange.items():
                data[key] = storage.get(key)
        except Exception as ex:
            print(ex)
        return data


    app.run()
      
