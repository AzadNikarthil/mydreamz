import requests
import json
import collections

from itertools import combinations

from mydreamz.utility import GetServiceStore
from mydreamz.config import ConfigMgr
from mydreamz.raft.storage import Storage
from mydreamz.exchanges.exchange import exchange
from mydreamz.exchanges.exchange_mgr import ExchangeMgr
from mydreamz.db.neo4j_util import Neo4jUtil

EXCHANGE="binance"

def add_pair_to_set(pair, coin_list):
    split_list = pair.split("/")
    c1 = split_list[0]
    c2 = split_list[1]
    coin_list.add(c1)
    coin_list.add(c2)

    return coin_list

def get_all_pairs(coins):
    perm = combinations(coins, 2)
    return perm

def all_triangle_combination(permut):
    perm = combinations(permut, 3)
    return perm


def is_traingle_arbitrash(combi):
    d1 = collections.Counter(k[0] for k in combi)
    d2 = collections.Counter(k[1] for k in combi)
    d3 = d1 + d2
    l = d3.values()
    for i in l:
        if i != 2:
            return False
    return True

def covert_tuple_pair(combi, exchange):
    """
    """
    doc = {}
    pair_list = []
    for tuple_pair in combi:
        pair = "{}/{}".format(tuple_pair[0], tuple_pair[1])
        pair_list.append(pair)

    doc['pair'] = pair_list
    doc['exchange'] = exchange
    return doc




if __name__ == "__main__":
    service_store_obj = GetServiceStore()
    service_store_obj.initialize()
    configMgr = ConfigMgr(service_store_obj)
    configMgr.init()
    configMgr.parse()
    exchangeMgr = ExchangeMgr(service_store_obj)
    neo4j = Neo4jUtil(service_store_obj)
    service_store_obj.set_exchange_mgr(exchangeMgr)
    service_store_obj.set_config_mgr(configMgr)
    service_store_obj.set_neo4j_util(neo4j)
    neo4j.intialize()
 
    def check_all_pair_valid(combi):
        for pair in combi:
            if not service_store_obj.get_neo4j_util().is_pair(pair, EXCHANGE):
                return False
        return True


    x = requests.get("http://localhost:5000/pair?exchange={}".format(EXCHANGE))
    content = json.loads(x.text)[EXCHANGE]

    total_key = len(content.keys())
    key_count = 0
    for key in content:
        key_count = key_count + 1
        total_pair = len(content[key])
        if total_pair <= 6:
            continue
        pair_count = 0

        arbitrage_data = []
        for pair in content[key]:
            pair_count = pair_count + 1
            print("Keys {}/{}, Pair {}/{} {}".format(total_key, key_count, total_pair, pair_count, pair))
            if service_store_obj.get_neo4j_util().is_pair(pair, EXCHANGE):

                split_list = pair.split("/")
                c1 = split_list[0]
                c2 = split_list[1]

                result_c1 = service_store_obj.get_neo4j_util().fetch_all_pair(c1, EXCHANGE)
                set_c1 = set(result_c1)
                result_c2 = service_store_obj.get_neo4j_util().fetch_all_pair(c2, EXCHANGE)
                set_c2 = set(result_c2)

                common = set_c1.intersection(set_c2)
                coins = add_pair_to_set(pair, common)
                if len(coins) < 3:
                    continue

                all_pair = get_all_pairs(coins)
                possible_arbitrage_list = all_triangle_combination(all_pair)


                for combi in possible_arbitrage_list:
                    if is_traingle_arbitrash(combi):
                        if check_all_pair_valid(combi):
                            doc = covert_tuple_pair(combi, EXCHANGE)
                            arbitrage_data.append(doc)

        if len(arbitrage_data) > 0:
            service_store_obj.get_db_util().insert_arbitrage(arbitrage_data)


    service_store_obj.get_neo4j_util().close()
    
                

