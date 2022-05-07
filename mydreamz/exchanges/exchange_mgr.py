
from mydreamz.exchanges.exchange import exchange
from mydreamz.exchanges.base_exchange import BaseExchange 

from mydreamz.exchanges.coinbase import CoinBase
from mydreamz.exchanges.bitstamp1 import BitStamp1
from mydreamz.exchanges.bit2c import Bit2c
from mydreamz.exchanges.bitflyer import BitFlyer
from mydreamz.exchanges.bl3p import Bl3p
from mydreamz.exchanges.btcbox import BtcBox
from mydreamz.exchanges.bitbank import BitBank
from mydreamz.exchanges.binancecoinm import BinanceCoinm
from mydreamz.exchanges.bitmex import BitMex
from mydreamz.exchanges.bitpanda import BitPanda
from mydreamz.exchanges.bitvavo import BitVavo
from mydreamz.exchanges.btcalpha import BtcAlpha
from mydreamz.exchanges.btcmarkets import BtcMarkets
from mydreamz.exchanges.btctradeua import BtcTradeUA
from mydreamz.exchanges.bybit import ByBit
from mydreamz.exchanges.coincheck import CoinCheck

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
        elif exchange_name == "btcbox":
            exchange = BtcBox(self.service_store)
        elif exchange_name == "bitbank":
            exchange = BitBank(self.service_store)
        elif exchange_name == "binancecoinm":
            exchange = BinanceCoinm(self.service_store)
        elif exchange_name == "bitmex":
            exchange = BitMex(self.service_store)
        elif exchange_name == "bitpanda":
            exchange = BitPanda(self.service_store)
        elif exchange_name == "bitvavo":
            exchange = BitVavo(self.service_store)
        elif exchange_name == "btcalpha":
            exchange = BtcAlpha(self.service_store)
        elif exchange_name == "btcmarkets":
            exchange = BtcMarkets(self.service_store)
        elif exchange_name == "btctradeua":
            exchange = BtcTradeUA(self.service_store)
        elif exchange_name == "bybit":
            exchange = ByBit(self.service_store)
        elif exchange_name == "coincheck":
            exchange = CoinCheck(self.service_store)
        else:
            exchange = BaseExchange(self.service_store)
        exchange.set_exchange_name(exchange_name)

        return exchange

