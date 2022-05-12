import pymongo

class DBUtil:

    def __init__(self):
        """
        """
        self.mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.mydreamz_db = self.mongo_client["mydreamz"]

        self.pair = self.mydreamz_db["pair"]
        self.arbitrage = self.mydreamz_db["arbitrage"]

    def add_pair(self, data):
        """
        """
        self.pair.insert_one(data)

    def fetch_possible_arbitrage_list(self, exch):
        """
        """
        val = self.arbitrage.find({'exchange':exch}, {'exchange': 1, 'pair':1, '_id': False})
        return val

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

    def insert_arbitrage(self, data):
        """
        """
        self.arbitrage.insert_many(data)
