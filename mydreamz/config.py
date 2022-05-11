import json

import mydreamz.constant as CONSTANT

class ConfigMgr:
    """
    """

    def __init__(self, service_store, configFile=CONSTANT.CONFIG_FILE):
        """
        """
        self.service_store = service_store
        self.log = self.service_store.get_log_mgr().get_logger(__name__)
        self.file = configFile
        self.raft_config = RaftConfig()
        self.neo4j_config = Neo4jConfig()
        self.config = {}
        self.coin_pair = []
        self.coins = []

    def init(self):
        """
        """
        self.log.debug(">")
        with open(self.file) as json_file:
            self.config = json.load(json_file)
        self.log.debug("<")

    def parse(self):
        """
        """
        self.log.debug(">")
        if "coin_pair" in self.config:
            self.coin_pair =  self.config["coin_pair"]

        if "coins" in self.config:
            self.coins = self.config["coins"]

        raft_data = None
        if "raft" in self.config:
           raft_data = self.config["raft"] 

        neo4j_data = None
        if "neo4j" in self.config:
           neo4j_data = self.config["neo4j"] 


        self.raft_config.init(raft_data)
        self.raft_config.parse()
        self.neo4j_config.init(neo4j_data)
        self.neo4j_config.parse()
        self.log.debug("<")

    def get_neo4j_config_mgr(self):
        return self.neo4j_config

    def get_raft_config_mgr(self):
        return self.raft_config

    def get_coin_pair(self):
        """
        """
        return self.coin_pair

    def get_coins(self):
        """
        """
        return self.coins

class Neo4jConfig:
    """
    """

    def __init__(self):
        """
        """
        self.port = None
        self.username = None
        self.password = None
        self.database = None

    def init(self, data):
        """
        """
        self.config_data = data

    def parse(self):
        """
        """
        if "port" in self.config_data:
            self.port = self.config_data["port"]
        if "username" in self.config_data:
            self.username = self.config_data["username"]
        if "password" in self.config_data:
            self.password = self.config_data["password"]
        if "database" in self.config_data:
            self.database = self.config_data["database"]

    def get_database(self):
        """
        """
        return self.database

    def get_port(self):
        """
        """
        return self.port

    def get_username(self):
        """
        """
        return self.username

    def get_password(self):
        """
        """
        return self.password


class RaftConfig:
    """
    """

    def __init__(self):
        """
        """
        self.config_data = None
        self.raft_starting_port = None
        self.collector_port = None

    def init(self, data):
        """
        """
        self.config_data = data

    def parse(self):
        """
        """
        if "port_start" in self.config_data:
            self.raft_starting_port = self.config_data["port_start"]

        if "collector_port" in self.config_data:
            self.collector_port = self.config_data["collector_port"]


    def get_port_starting_address(self):
        """
        """
        return self.raft_starting_port
        

    def get_collector_port(self):
        """
        """
        return self.collector_port
        


