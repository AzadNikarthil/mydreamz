import json

import mydreamz.constant as CONSTANT

class ConfigMgr:
    """
    """

    def __init__(self, configFile=CONSTANT.CONFIG_FILE):
        """
        """
        self.file = configFile
        self.raft_config = RaftConfig()
        self.config = {}
        self.coin_pair = []

    def init(self):
        """
        """
        with open(self.file) as json_file:
            self.config = json.load(json_file)

    def parse(self):
        """
        """
        if "coin_pair" in self.config:
            self.coin_pair =  self.config["coin_pair"]

        raft_data = None
        if "raft" in self.config:
           raft_data = self.config["raft"] 

        self.raft_config.init(raft_data)
        self.raft_config.parse()

    def get_raft_config_mgr(self):
        return self.raft_config

    def get_coin_pair(self):
        """
        """
        return self.coin_pair


class RaftConfig:
    """
    """

    def __init__(self):
        """
        """
        self.config_data = None
        self.raft_starting_port = None

    def init(self, data):
        """
        """
        self.config_data = data

    def parse(self):
        """
        """
        if "port_start" in self.config_data:
            self.raft_starting_port = self.config_data["port_start"]

    def get_port_starting_address(self):
        """
        """
        return self.raft_starting_port
        


