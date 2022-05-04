from mydreamz.exchanges.exchange import exchange
from mydreamz.exchanges.base_exchange import BaseExchange

class Bl3p(BaseExchange):
    """
    """

    def __init__(self, service_store):
        """
        """
        BaseExchange.__init__(self, service_store)

    def get_coin_pair(self):
        """
        """
        new_pair = ['BTC/EUR']
        pairs = self.service_store.get_config_mgr().get_coin_pair()
        return new_pair



