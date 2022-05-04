from mydreamz.exchanges.exchange import exchange
from mydreamz.exchanges.base_exchange import BaseExchange

class CoinBase(BaseExchange):
    """
    """

    def __init__(self, service_store):
        """
        """
        BaseExchange.__init__(self, service_store)

    def get_coin_pair(self):
        """
        """
        pairs = self.service_store.get_config_mgr().get_coin_pair()
