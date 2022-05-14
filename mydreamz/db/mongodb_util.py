import pymongo

class DBUtil:

    def __init__(self):
        """
        """
        self.mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.mydreamz_db = self.mongo_client["mydreamz"]

        self.pair = self.mydreamz_db["pair"]
        self.arbitrage = self.mydreamz_db["arbitrage"]
        self.exchange_rate = self.mydreamz_db["exchange_rate"]

    def add_pair(self, data):
        """
        """
        self.pair.insert_one(data)

    def fetch_possible_arbitrage_list(self, exch):
        """
        """
        val = self.arbitrage.find({'exchange':exch}, {'exchange': 1, 'pair':1, '_id': False})
        return val

    def get_exchange_rate(self, exchange, pair):
        """
        """
        value = {}
        if pair == None:
            cursor = self.exchange_rate.find({'exchange': exchange}, {'_id': False})
            data = []
            for x in cursor:
                data.append(x)
            value[exchange] = data
            return value
        else:
            cursor = self.exchange_rate.find({'exchange': exchange, 'pair': pair}, {'_id': False})
            for x in cursor:
                return x


    def get_pair(self, exch):
        """
        """
        if exch == None:
            val = self.pair.find()
        else:
            val = self.pair.find({'exchange':exch})
        return val

    def update_pair(self, data):
        """
        """
        exchange = data['exchange']
        pairs = data['pairs']
        query = {"exchange":exchange}

        value = {"$set": data}

        result = self.pair.update_one(query, value)

        if result.modified_count < 1:
            self.add_pair(data)

    def check_arbitrage_key_present(self, doc):
        """
        """
        cursor = self.arbitrage.find({'key':doc['key']})
        for x in cursor:
            return True

        return False

    def update_pair_price(self, data):
        """
        """
        exchange = data["exchange"]
        pair = data["pair"]

        value = {"$set": data}

        query = {"exchange": exchange, "pair": pair}
        result = self.exchange_rate.update_one(query, value)

    def delete_all_pair_price(self, exchange):
        """
        """
        try:
            self.exchange_rate.delete_many({'exchange': exchange})
        except Exception as ex:
            print(ex)
            pass
            

    def add_pair_price(self, data):
        """
        """
        self.exchange_rate.insert_one(data)

    def insert_arbitrage(self, data):
        """
        """
        self.arbitrage.insert_many(data)
