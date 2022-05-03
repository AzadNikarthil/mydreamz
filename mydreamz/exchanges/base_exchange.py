
from mydreamz.exchanges.exchange import exchange

class BaseExchange:
    """
    """

    def __init__(self, service_store):
        """
        """
        self.service_store = service_store

    def get_coin_pair(self):
        """
        """
        self.service_store.get_config_mgr().get_coin_pair()

