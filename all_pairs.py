"""
fetch all the pair from the exchanges configured
"""

from mydreamz.utility import GetServiceStore
from mydreamz.config import ConfigMgr
from mydreamz.raft.storage import Storage
from mydreamz.exchanges.exchange import exchange
from mydreamz.exchanges.exchange_mgr import ExchangeMgr



if __name__ == '__main__':
    service_store_obj = GetServiceStore()
    service_store_obj.initialize()
    configMgr = ConfigMgr(service_store_obj)
    configMgr.init()
    configMgr.parse()
    exchangeMgr = ExchangeMgr(service_store_obj)
    service_store_obj.set_exchange_mgr(exchangeMgr)
    service_store_obj.set_config_mgr(configMgr)


    exchange_details = service_store_obj.get_exchange_mgr().get_exchange_details()
    for key, value in exchange_details.items():
        if key == "binance":
            print("skipped binance")
            continue
        elif key == "coinbase":
            print("skipped coinbase")
            continue
        elif key == "wazirx":
            print("skipped coinbase")
            continue
        try:
            exchange = service_store_obj.get_exchange_mgr().get_exchange_obj(key)
            value = exchange.get_all_coins()
            service_store_obj.get_db_util().update_pair(value)
            #val = service_store_obj.get_db_util().get_pair()
            #for x in val:
            #    print(x)
            print("{}".format(value))
        except Exception as ex:
            print(ex)
            pass

