
from neo4j import GraphDatabase

class Neo4jUtil:

    def __init__(self, service_store):
        """
        """
        self.service_store = service_store
        self.config = None

    def intialize(self):
        """
        """
        self.config = self.service_store.get_config_mgr().get_neo4j_config_mgr()
        self.driver = GraphDatabase.driver("bolt://localhost:{}".format(self.config.get_port()), auth=(self.config.get_username(), self.config.get_password()))
        self.session = self.driver.session(database=self.config.get_database())

    def create_graph(self, pair, exchange):
        self.session.write_transaction(self._create_node_and_relation, pair, exchange)

    def delete_graph(self):
        self.session.write_transaction(self._delete_graph)
    
    def is_pair(self, pair, exchange):
        return self.session.read_transaction(self._is_pair, pair, exchange)

    def fetch_all_pair(self, coin, exchange):
        return self.session.read_transaction(self._fetch_all_pair, coin, exchange)

    def _fetch_all_pair(self, tx,  coin, exchange):
        query = """
        MATCH (:COIN{name:$coin})-[r:PAIR]-(n:COIN) 
        return n
        """
        result = tx.run(query, coin=coin)
        value = []
        for res in result:
            value.append(res.value()['name'])
        return value


    def _delete_graph(self, tx):
        query = """
        MATCH (n)
        DETACH DELETE n
        """
        tx.run(query)

    def _is_pair(self, tx, pair, exchange):
        if "/" in pair:
            split_list = pair.split("/")
            c1 = split_list[0]
            c2 = split_list[1]
        else:
            c1 = pair[0]
            c2 = pair[1]

        query = """
        MATCH (:COIN{name:$c1})-[r:PAIR]-(n:COIN{name:$c2}) 
        return r
        """
        result = tx.run(query, c1=c1, c2=c2)
        for res in result:
            return True

        return False
     

    def _create_node_and_relation(self, tx, pair, exchange):
        split_list = pair.split("/")
        c1 = split_list[0]
        c2 = split_list[1]
        
        query = """
        MERGE (a:COIN{name: $coin})
        SET a.name = $coin

        """
        tx.run(query, coin=c1)
        tx.run(query, coin=c2)
        query = """
        MATCH
        (c1:COIN {name: $coin1}),
        (c2:COIN {name: $coin2})
        MERGE ((c1)-[p:PAIR{exchange: $exchange, pair: $pair}]-(c2))
        """
        tx.run(query, coin1=c1, coin2=c2, exchange=exchange, pair=pair)

    def close(self):
        self.driver = None
        self.session = None

