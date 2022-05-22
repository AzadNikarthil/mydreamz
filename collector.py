"""
rate fetched by the main process will be synced to this process through raft

it also has rest api server to communicate to the outside 
"""
import time

import logging
from flask import Flask, request

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

    #storage = Storage(ip_port, partner_address)
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
       
    @app.route('/')
    def exchange_rate():
        """
        """
        exch = None
        pair = None
        try:
            exch = request.args.get('exchange')
        except Exception as ex:
            print(ex)
        try:
            pair = request.args.get('pair')
        except Exception as ex:
            print(ex)

        if exch == None and pair == None:
            return {"Info": "Pass exchange name"}

        data = service_store_obj.get_db_util().get_exchange_rate(exch, pair)
        return data

    @app.route('/possible_arbitrage')
    def get_arbitrage():
        """
        """
        result = {}
        try:
            exch = request.args.get('exchange')
        except Exception as ex:
            print(ex)

        cursor = service_store_obj.get_db_util().fetch_possible_arbitrage_list(exch)
        data = []
        for x in cursor:
            data.append(x)

        result['arbitrage'] = data

        return result



    @app.route('/pair')
    def get_pair():
        """
        """
        data = {}
        try:
            exch = request.args.get('exchange')
        except Exception as ex:
            print(ex)

        cursor = service_store_obj.get_db_util().get_pair(exch)
        for x in cursor:
            data[x['exchange']] = x['pairs']
        return data


    app.run()
      
