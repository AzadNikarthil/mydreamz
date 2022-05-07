import time

from mydreamz.utility import GetServiceStore
from mydreamz.config import ConfigMgr
from mydreamz.raft.storage import Storage
from mydreamz.exchanges.exchange import exchange
from mydreamz.exchanges.exchange_mgr import ExchangeMgr
from mydreamz.raft.raft_helper import RaftHelper

partner_address = ['127.0.0.1:10001', '127.0.0.1:10002', '127.0.0.1:10003', '127.0.0.1:10004', '127.0.0.1:10005', '127.0.0.1:10006', '127.0.0.1:10007', '127.0.0.1:10008', '127.0.0.1:10009', '127.0.0.1:10010', '127.0.0.1:10011', '127.0.0.1:10012', '127.0.0.1:10013', '127.0.0.1:10014', '127.0.0.1:10015', '127.0.0.1:10016', '127.0.0.1:10017', '127.0.0.1:10018', '127.0.0.1:10019', '127.0.0.1:10020', '127.0.0.1:10021', '127.0.0.1:10022', '127.0.0.1:10023', '127.0.0.1:10024', '127.0.0.1:10025', '127.0.0.1:10026', '127.0.0.1:10027', '127.0.0.1:10028', '127.0.0.1:10029', '127.0.0.1:10030', '127.0.0.1:10031', '127.0.0.1:10032', '127.0.0.1:10033', '127.0.0.1:10034', '127.0.0.1:10035', '127.0.0.1:10036', '127.0.0.1:10037', '127.0.0.1:10038', '127.0.0.1:10039', '127.0.0.1:10040', '127.0.0.1:10041', '127.0.0.1:10042', '127.0.0.1:10043', '127.0.0.1:10044', '127.0.0.1:10045', '127.0.0.1:10046', '127.0.0.1:10047', '127.0.0.1:10048', '127.0.0.1:10049', '127.0.0.1:10050']


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
    print(ip_port)
    print(partner_address)

    storage = Storage(ip_port, partner_address)
   
    while True:
        for key, value in exchange.items():
            print("{}:{}".format(key, storage.get(key)))
        time.sleep(1)
        
