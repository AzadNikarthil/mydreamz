"""
"""

import requests
import re
from lxml import html


def GetServiceStore():
    """
    """
    import mydreamz.mydream_store as _Store
    return _Store



def get_withdrawal_fees(exchange, trading_size=1000):
    '''
    function to get the withdrawal fees of each exchanges on website https://withdrawalfees.com/
    will also calculate the withdrawal fee percentage based on an approximate trading size
    '''

    withdrawal_fee = {}
    response = requests.get('https://withdrawalfees.com/exchanges/{}'.format(exchange))
    if response.ok:
        tree = html.fromstring(response.content)

        for ele in tree.xpath('//tbody//tr'):
            coin_name = ele.xpath('.//div[@class="symbol"]/text()')[0]
            usd_fee = ele.xpath('.//td[@class="withdrawalFee"]//div[@class="usd"]/text()')[0]
            coin_fee = ele.xpath('.//td[@class="withdrawalFee"]//div[@class="fee"]/text()')[
                0] if usd_fee != 'FREE' else 'FREE'

            usd_fee = 0 if usd_fee == 'FREE' else float(re.findall(r'[0-9\.]+', usd_fee)[0])
            coin_fee = 0 if coin_fee == 'FREE' else float(re.findall(r'[0-9\.]+', coin_fee)[0])

            withdrawal_fee[coin_name] = {
                'usd_fee': usd_fee,
                'usd_rate': usd_fee / trading_size,
                'coin_fee': coin_fee
            }
        return withdrawal_fee

    else:
        raise ValueError('{} is not an exchange supported by withdrawalfees.com'.format(exchange))

