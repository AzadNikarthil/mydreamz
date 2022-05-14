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
        return pairs
    else:
        return [p1, p3, p2]

def split_pair(pairs):
    val = pairs.split("/")
    a = val[0]
    b = val[1]
    return a,b

def is_typeA_pair(p1, p2):
    """
    p1 -> A/B
    p2 -> B/C
    """
    c1_p1, c2_p1 = split_pair(p1)
    #print("{} {} {}".format(p1, c1_p1, c2_p1))
    c1_p2, c2_p2 = split_pair(p2)
    #print("{} {} {}".format(p2, c1_p2, c2_p2))
    if c2_p1 == c1_p2:
        return True
    else:
        return False

def check_arbitrage(pairs, data, db):
    p1 = pairs[0]
    p2 = pairs[1]
    p3 = pairs[2]

    x = requests.get("http://localhost:5000/?exchange={}&pair={}".format(EXCHANGE, p1))
    p1_price_details = json.loads(x.text)
    p1_price = p1_price_details.get('price', 0)
    if p1_price == 0 or p1_price == None:
        return

    x = requests.get("http://localhost:5000/?exchange={}&pair={}".format(EXCHANGE, p2))
    p2_price_details = json.loads(x.text)
    p2_price = p2_price_details.get('price', 0)
    if p2_price == 0 or p2_price == None:
        return

    x = requests.get("http://localhost:5000/?exchange={}&pair={}".format(EXCHANGE, p3))
    p3_price_details = json.loads(x.text)
    p3_price = p3_price_details.get('price', 0)
    if p3_price == 0 or p3_price == None:
        return
    """
    Type A
    A -> nB
    B -> mC
    A -> n*mC

    Type B
    A -> nB
    C -> mB
    B -> C/m
    A -> n*C/m
    """
    first_type = ""
    c1_p1_count = 1
    c2_p1_count = p1_price
    if is_typeA_pair(p1, p2):
        first_type = "Type A"
        c1_p2_count = c2_p1_count
        c2_p2_count = p2_price * c1_p2_count
        out_coin_count = c2_p2_count
    else: #c1_p2_count = c2_p2_count
        first_type = "Type B"
        c2_p2_count = c2_p1_count
        c1_p2_count = (1/p2_price) * c2_p2_count
        out_coin_count = c1_p2_count

    if is_typeA_pair(p2, p3):
        c1_p3_count = out_coin_count
        c2_p3_count = p3_price * c1_p3_count

        if c1_p1_count < c2_p3_count:
            print("First {}, second Type A".format(first_type))
            print("{}:{} ({}:{})".format(p1, p1_price, c1_p1_count, c2_p1_count))
            print("{}:{} ({}:{})".format(p2, p2_price, c1_p2_count, c2_p2_count))
            print("{}:{} ({}:{})".format(p3, p3_price, c1_p3_count, c2_p3_count))
            print("======================")
            db.sync_with_arbitrage_live(data)
    else:
        c2_p3_count = out_coin_count
        c1_p3_count = (1/p3_price) * c2_p3_count

        if c1_p1_count < c1_p3_count:
            print("First {}, second Type B".format(first_type))
            print("{}:{} ({}:{})".format(p1, p1_price, c1_p1_count, c2_p1_count))
            print("{}:{} ({}:{})".format(p2, p2_price, c1_p2_count, c2_p2_count))
            print("{}:{} ({}:{})".format(p3, p3_price, c1_p3_count, c2_p3_count))
            print("======================")
            db.sync_with_arbitrage_live(data)

 
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
    data = []
    while True:
        cursor = db.fetch_possible_arbitrage_list(EXCHANGE)
        for x in cursor:
            arbitrage = x
            pairs = change_order(arbitrage["pair"])


            #try:
            check_arbitrage(pairs, x, db)
            pairs.reverse()
            check_arbitrage(pairs, x, db)
            #except Exception as ex:
            #    pass


        
 
