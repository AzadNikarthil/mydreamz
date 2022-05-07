import pymongo

class DBUtil:

    def __init__(self):
        """
        """
        self.mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.mydreamz_db = self.mongo_client["mydreamz"]

        self.pair = self.mydreamz_db["pair"]

    def add_pair(self, data):
        """
        """
        self.pair.insert_one(data)

    def get_pair(self):
        """
        """
        val = self.pair.find()
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

