import requests
import json

class TriangleArbitrage:
    def __init__(self, exchange, pairs, trade_price=None, fees=None, min_cut_off=None):
        """
        """
        self.exchange = exchange
        self.pairs = pairs
        self.trade_price = trade_price
        self.fees = fees
        self.pair_price = {}

        self.p1 = pairs[0]
        self.p2 = pairs[1]
        self.p3 = pairs[2]
        self.p1_count = {}
        self.p3_count = {}

        self.start_coin = self.find_coin_to_arbitrage(pairs)

    def analyze(self):
        """
        """
        c1_p1_count, c2_p1_count, self.p1_count = self.find_count_with_start_coin(self.p1, self.start_coin)
        if c1_p1_count == None and c2_p1_count == None:
            return None
        
        com_coin_set1, _ = self.find_common_coin(self.p1, self.p2)
        multiplier = self.p1_count[com_coin_set1]
        c1_p2_count, c2_p2_count, p2_count = self.find_count_with_common_coin(self.p2, com_coin_set1)
        if c1_p2_count == None and c2_p2_count == None:
            return None

        c1_p2_count = c1_p2_count * multiplier
        c1_p2_count = c2_p2_count * multiplier

        com_coin_set2, _ = self.find_common_coin(self.p2, self.p3)
        multiplier_1 = p2_count[com_coin_set2]
        c1_p3_count, c2_p3_count, self.p3_count = self.find_count_with_common_coin(self.p3, com_coin_set2)
        if c1_p3_count == None and c2_p3_count == None:
            return None


        c1_p3_count = c1_p3_count * multiplier_1 * multiplier
        c2_p3_count = c2_p3_count * multiplier_1 * multiplier
        self.p3_count[com_coin_set2] = self.p3_count[com_coin_set2] * multiplier * multiplier_1
        self.p3_count[self.start_coin] = self.p3_count[self.start_coin] * multiplier * multiplier_1

        if self.p3_count[self.start_coin] > self.p1_count[self.start_coin]:
            print("{} {} {}:{}".format(self.p1, self.pair_price[self.p1], c1_p1_count, c2_p1_count))
            print("{} {} {}:{}".format(self.p2, self.pair_price[self.p2], c1_p2_count, c2_p2_count))
            print("{} {} {}:{}".format(self.p3, self.pair_price[self.p3], c1_p3_count, c2_p3_count))
            print("{} {}->{}".format(self.start_coin, self.p1_count[self.start_coin], self.p3_count[self.start_coin]))
            print("=======================")
            return True
        return False

    def calculate_min_cut_off(self, start_coin, start_coin_count, end_coin_count):
        pass

    def get_arbitrage_value(self):
        """
        """
        return {
                    "coin": self.start_coin, 
                    "s_c": self.p1_count[self.start_coin], 
                    "e_c": self.p3_count[self.start_coin],
                    "p": self.pair_price
                }

    def find_count_with_common_coin(self, pair, common_coin):
        c1_count = 0
        c2_count = 0
        c1_count, c2_count, count = self.find_count_with_start_coin(pair, common_coin)
        return c1_count, c2_count, count
        

    def find_count_with_start_coin(self, pair, start_coin):
        c1_count = 0
        c2_count = 0
        count = {}
        pair_value = self.get_pair_price(pair)
        price = pair_value['price']
        ask = pair_value['ask']
        bid = pair_value['bid']

        if price == 0 or price == None:
            return None, None, {}
        if ask == 0 or ask == None:
            return None, None, {}
        if bid == 0 or bid == None:
            return None, None, {}


        #A/B B/C
        #SELL A get B ask -> check bid/buy price
        #BUY A with B bid -> check ask/sell price

        c1, c2 = self.split_pair(pair)
        if start_coin == c1:
            c1_count = 1
            c2_count = bid
            self.pair_price[pair] = pair_value['bid']

        elif start_coin == c2:
            c2_count = 1
            c1_count = 1/ask
            self.pair_price[pair] = pair_value['ask']

        count[c1] = c1_count
        count[c2] = c2_count

        return c1_count, c2_count, count


    def get_pair_price(self, pair):
        """
        """
        x = requests.get("http://localhost:5000/?exchange={}&pair={}".format(self.exchange, pair))
        price_details = json.loads(x.text)
        price = price_details.get('price', 0)
        bid = price_details.get('bid', 0)
        ask = price_details.get('ask', 0)
        if price == None:
            price = 0
        if bid == None:
            bid = 0
        if ask == None:
            ask = 0
        return {
                "price": price,
                "bid": bid,
                "ask": ask
                }

    def find_coin_to_arbitrage(self, pairs):
        """
        """
        p1 = self.p1
        p2 = self.p2
        p3 = self.p3

        c1_com_1, c2_com_1 = self.find_common_coin(p1, p2)
        if c1_com_1 == None:
            return  None
        c1_com_2, c2_com_2 = self.find_common_coin(p2, p3)
        if c1_com_2 == None:
            return  None
        c1_com_3, c2_com_3 = self.find_common_coin(p1, p3)
        if c1_com_3 == None:
            return  None

        return c1_com_3


    def find_common_coin(self, p1, p2):
        """
        """
        c1_p1, c2_p1 = self.split_pair(p1)
        c1_p2, c2_p2 = self.split_pair(p2)
        if c1_p1 == c1_p2:
            return c1_p1, c1_p2
        if c2_p1 == c2_p2:
            return c2_p1, c2_p2
        if c1_p1 == c2_p2:
            return c1_p1, c2_p2
        if c2_p1 == c1_p2:
            return c2_p1, c1_p2
        return None, None

    def split_pair(self, pairs):
        """
        """
        val = pairs.split("/")
        a = val[0]
        b = val[1]
        return a,b

