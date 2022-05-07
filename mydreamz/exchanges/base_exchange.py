import time
import requests

from mydreamz.raft.raft_helper import RaftHelper
from mydreamz.raft.storage import Storage

class BaseExchange:
    """
    """

    def __init__(self, service_store):
        """
        """
        self.service_store = service_store
        self.log = self.service_store.get_log_mgr().get_logger(__name__)
        self.exchange_obj = None
        self.name = None
        self.raft_helper = RaftHelper(self.service_store)
        self.exchange_mgr = self.service_store.get_exchange_mgr()
        self.currency_exchange_data = {}
        self.get_currency_exchange_data()

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

        
    def get_fiat_currency_name(self, pair): 
        currency = pair.split("/")[1]
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

    def handle_currency_convertion(self, price, pair):
        """
        """
        currency_name = self.get_fiat_currency_name(pair)
        new_price = self.convert_to_usd(currency_name, price)
        new_price_dict = {
                "currency": currency_name,
                "price": new_price
                }
        return new_price_dict

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

        rate = self.handle_currency_convertion(value, pair)
        return rate
    
    def run(self, ip_port):
        """
        """
        exchange_count = self.exchange_mgr.get_exchange_count()
        partner_address = self.raft_helper.get_partners_address(exchange_count, ip_port)
        self.storage = Storage(ip_port, partner_address)
        pair_list = self.get_coin_pair()
        while True:
                for pair in pair_list:
                    try:
                        ticker = self.exchange_obj.fetch_ticker(pair)
                        kv_rate = self.get_crypto_rate(ticker, pair)
                        self.update_storage(kv_rate)
                        #kv_volume = self.get_crypto_volume(ticker, pair)
                        #self.update_storage(kv_volume)
                    except Exception as ex:
                        self.log.error("Exception : {} {}".format(self.name, pair))
                        self.log.error(ex)
                        time.sleep(1)
             
