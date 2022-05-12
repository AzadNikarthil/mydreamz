import requests
import json

from mydreamz.utility import GetServiceStore
from mydreamz.config import ConfigMgr
from mydreamz.raft.storage import Storage
from mydreamz.exchanges.exchange import exchange
from mydreamz.exchanges.exchange_mgr import ExchangeMgr


EXCHANGE="binance"

def change_order(pairs):
    p1 = pairs[0]
    p2 = pairs[1]
    p3 = pairs[2]

    if p1.split("/")[1] in p2:
        return paris
    else:
        return [p1, p3, p2]

def check_arbitrage(pairs, price_details):
    p1 = pairs[0]
    p2 = pairs[1]
    p3 = pairs[2]

    p1_price = price_details[p1]['price']
    p2_price = price_details[p2]['price']
    p3_price = price_details[p3]['price']

    p1_count = 1
    p2_count = p1_price
    p3_count = p2_count/p2_price
    p1_count_end = p3_count/p1_price

    print("{}:{}".format(p1, p1_price))
    print("{}:{} {}".format(p2, p2_price, p3_count))
    print("{}:{} {}".format(p3, p3_price, p1_count_end))


 
if __name__ == "__main__":
    service_store_obj = GetServiceStore()
    service_store_obj.initialize()
    configMgr = ConfigMgr(service_store_obj)
    configMgr.init()
    configMgr.parse()
    exchangeMgr = ExchangeMgr(service_store_obj)
    service_store_obj.set_exchange_mgr(exchangeMgr)
    service_store_obj.set_config_mgr(configMgr)
    db = service_store_obj.get_db_util()
    cursor = db.fetch_possible_arbitrage_list(EXCHANGE)
    data = []
    for x in cursor:
        arbitrage = x
        pairs = change_order(arbitrage["pair"])

        print(pairs)

        x = requests.get("http://localhost:5000")
        content = json.loads(x.text)[EXCHANGE]
        try:
            check_arbitrage(pairs, content)
            pairs.reverse()
            check_arbitrage(pairs, content)
        except Exception as ex:
            pass


        
 
