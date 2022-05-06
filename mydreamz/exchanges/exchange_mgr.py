
from mydreamz.exchanges.exchange import exchange
from mydreamz.exchanges.base_exchange import BaseExchange 

from mydreamz.exchanges.coinbase import CoinBase
from mydreamz.exchanges.bitstamp1 import BitStamp1
from mydreamz.exchanges.bit2c import Bit2c
from mydreamz.exchanges.bitflyer import BitFlyer
from mydreamz.exchanges.bl3p import Bl3p
from mydreamz.exchanges.btcalpha import Btcalpha
from mydreamz.exchanges.btcbox import BtcBox
from mydreamz.exchanges.bitbank import BitBank

class ExchangeMgr:
    """
    """

    def __init__(self, service_store):
        """
        """
        self.exchange = exchange
        self.exchange_count = len(self.exchange.keys())
        self.service_store = service_store

    def get_exchange_count(self):
        """
        """
        return self.exchange_count

    def get_exchange_details(self):
        """
        """
        return self.exchange

    def get_exchange_obj(self, exchange_name):
        """
        """
        exchange = None
        if exchange_name == "coinbase":
            exchange = CoinBase(self.service_store)
        elif exchange_name == "bitstamp1":
            exchange = BitStamp1(self.service_store)
        elif exchange_name == "bit2c":
            exchange = Bit2c(self.service_store)
        elif exchange_name == "bitflyer":
            exchange = BitFlyer(self.service_store)
        elif exchange_name == "bl3p":
            exchange = Bl3p(self.service_store)
        elif exchange_name == "btcalpha":
            exchange = Btcalpha(self.service_store)
        elif exchange_name == "btcbox":
            exchange = BtcBox(self.service_store)
        elif exchange_name == "bitbank":
            exchange = BitBank(self.service_store)
        else:
            exchange = BaseExchange(self.service_store)
        exchange.set_exchange_name(exchange_name)

        return exchange

