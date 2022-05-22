import time
import requests

from mydreamz.raft.raft_helper import RaftHelper
from mydreamz.db.mongodb_util import DBUtil
from mydreamz.raft.storage import Storage

class BaseExchange:
    """
    """

    def __init__(self, service_store):
        """
        """
        self.service_store = service_store
        self.log = self.service_store.get_log_mgr().get_logger(__name__)
        self.db = DBUtil()
        self.exchange_obj = None
        self.name = None
        self.raft_helper = RaftHelper(self.service_store)
        self.exchange_mgr = self.service_store.get_exchange_mgr()
        self.currency_exchange_data = {}
        self.get_currency_exchange_data()
        self.loop = 0

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

    def get_all_coins(self):
        """
        """
        coin_pair = {}
        pairs = {}
        pairs["exchange"] = self.name
        pairs["pairs"] = coin_pair


        markets = self.exchange_obj.fetchMarkets()
        pair_list = []
        for market_data in markets:
            pair = market_data['symbol']
            if not self.pair_currently_listed(pair):
                continue

            print(pair)
            coin = format(pair.split('/')[0])
            if coin in coin_pair.keys():
                pair_list = coin_pair[coin]
                pair_list.append(pair)
                coin_pair[coin] = pair_list
            else:
                coin_pair[coin] = [pair]

        return pairs

    def pair_currently_listed(self, pair):
        """
        """
        try:
            ticker = self.exchange_obj.fetch_ticker(pair)
            return True
        except Exception as ex:
            return False


    def get_coin_pair_v2(self):
        """
        """
        coins = self.service_store.get_config_mgr().get_coins()
        coin_pair = {}
        pairs = {}
        pairs["exchange"] = self.name
        pairs["pairs"] = coin_pair


        markets = self.exchange_obj.fetchMarkets()
        for market_data in markets:
            pair = market_data['symbol']
            coin = format(pair.split('/')[0])
            if coin in coins:
                if coin in coin_pair.keys():
                    pair_list = coin_pair[coin]
                    pair_list.append(pair)
                    coin_pair[coin] = pair_list
                else:
                    coin_pair[coin] = [pair]

        return pairs

    def get_currency_exchange_data(self):
        """
        """
        url = "https://open.er-api.com/v6/latest/USD"
        try:
            self.currency_exchange_data = requests.get(url).json()
        except Exception as ex:
            print(ex)
            pass

    def convert_to_usd(self, cur_from, value):
        """
        if self.currency_exchange_data:
            try:
                if cur_from == None:
                    return value
                else:
                    if cur_from in self.currency_exchange_data['rates']:
                        rate = self.currency_exchange_data['rates'][cur_from]
                        return value/rate
            except:
                self.get_currency_exchange_data()
                return value

        else:
            return value
        """
        return value

        
    def get_fiat_currency_name(self, pair): 
        currency = pair.split("/")[1]
        """
        if currency == "USDC":
            return "USD"
        elif currency == "USDT":
            return "USD"
        elif currency == "UST":
            return "USD"
        elif currency == "BUSD":
            return "USD"
        elif currency == "DAI":
            return "USD"
        elif currency == "TUSD":
            return "USD"
        elif currency == "MIM":
            return "USD"
        elif currency == "NIS":
            return "ILS"
        else:
            return currency
        """
        return currency

    def handle_currency_convertion(self, pair, price, bid, ask):
        """
        """
        currency_name = self.get_fiat_currency_name(pair)
        new_price = self.convert_to_usd(currency_name, price)
        new_price_dict = {
                pair: {
                    "currency": currency_name,
                    "price": new_price,
                    "bid": bid,
                    "ask": ask
                    }
                }
        return new_price_dict

    def update_db(self, rate):
        """
        """
        pair = list(rate.keys())[0]
        currency = rate[pair]["currency"]
        price = rate[pair]["price"]
        bid = rate[pair].get("bid", 0)
        ask = rate[pair].get("ask", 0)
        data = {
                "exchange": self.name,
                "pair": pair,
                "currency": currency,
                "price": price,
                "bid": bid,
                "ask": ask
                }

        print(self.loop)
        if self.loop == 0:
            print("add {}".format(data))
            self.db.add_pair_price(data)
        else:
            print("update {}".format(data))
            self.db.update_pair_price(data)

    def update_storage(self, rate):
        """
        """
        old_rates = self.storage.get(self.name)
        if old_rates:
            old_rates.update(rate)
            self.storage.set(self.name, old_rates)
        else:
            self.storage.set(self.name, rate)

    def get_crypto_volume(self, ticker, pair):
        """
        """
        return {'volume':"surprise"}

    def get_crypto_rate(self, ticker, pair):
        """
        """
        value = 0
        bid = 0
        ask = 0
        if "last" in ticker:
            value = float(ticker['last'])
        elif "info" in ticker:
            value_ticker = ticker['info']
            if 'lastPrice' in value_ticker:
                value = float(value_ticker['lastPrice'])
            elif 'last_price' in value_ticker:
                value = float(value_ticker['last_price'])
            elif 'last' in value_ticker:
                value = float(value_ticker['last'])
        if "bid" in ticker:
            bid = ticker['bid']
        if "ask" in ticker:
            ask = ticker['ask']

        rate = self.handle_currency_convertion(pair, value, bid, ask)
        return rate
    
    def run(self, ip_port):
        """
        """
        exchange_count = self.exchange_mgr.get_exchange_count()
        partner_address = self.raft_helper.get_partners_address(exchange_count, ip_port)
        self.storage = Storage(ip_port, partner_address)
        pair_list = self.get_coin_pair()
        self.db.delete_all_pair_price(self.name)
        while True:
                for pair in pair_list:
                    try:
                        ticker = self.exchange_obj.fetch_ticker(pair)
                        kv_rate = self.get_crypto_rate(ticker, pair)
                        #self.update_storage(kv_rate)
                        self.update_db(kv_rate)
                        #kv_volume = self.get_crypto_volume(ticker, pair)
                        #self.update_storage(kv_volume)
                    except Exception as ex:
                        self.log.error("Exception : {} {}".format(self.name, pair))
                        self.log.error(ex)
                        time.sleep(1)
                self.loop = self.loop + 1
             
