# #!/usr/bin/env python
# # encoding: utf-8

import re
import requests
from time import sleep, asctime

# headers info
headers={'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
        'Accept': '*/*',
        'Referer': 'http://http://m.icbc.com.cn/WapDynamicSite/Windroid/GoldMarket/',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
         }

icbc_url = "http://m.icbc.com.cn/WapDynamicSite/Windroid/GoldMarket/AccResponse.aspx?datapara="

re_rmb_gold = r"\d{3}\.\d{2}"

def getGoldPrice():
    '''
    get the real time price of rmb gold
    :return:
    '''
    res = requests.get(url=icbc_url, headers=headers)
    # get the middle price of rmb gold price
    price_data = re.findall(re_rmb_gold, res.text)
    rmb_gold_price = price_data[0]
    return rmb_gold_price

def main():
    '''
    main func
    :return:
    '''
    getGoldPrice()
    while True:
        middle_price = float(getGoldPrice())
        purchase_price = middle_price + 0.20
        sell_price = middle_price - 0.20
        print "Time: " + asctime()
        print "MiddlePrice: %.2f PurchasePrice: %.2f SellPrice: %.2f" % (middle_price, purchase_price, sell_price)
        sleep(3)

if __name__ == '__main__':
    main()
