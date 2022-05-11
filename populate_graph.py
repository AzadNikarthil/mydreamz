import requests
import json

from mydreamz.utility import GetServiceStore
from mydreamz.config import ConfigMgr
from mydreamz.raft.storage import Storage
from mydreamz.exchanges.exchange import exchange
from mydreamz.exchanges.exchange_mgr import ExchangeMgr
from mydreamz.db.neo4j_util import Neo4jUtil

EXCHANGE="binance"

if __name__ == '__main__':
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
 
    x = requests.get("http://localhost:5000/pair?exchange={}".format(EXCHANGE))
    content = json.loads(x.text)[EXCHANGE]
    for key in content:
        for pair in content[key]:
            print(pair)
            service_store_obj.get_neo4j_util().create_graph(pair, EXCHANGE)

    service_store_obj.get_neo4j_util().close()
