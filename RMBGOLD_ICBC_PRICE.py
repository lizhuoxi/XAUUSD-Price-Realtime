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

icbc_all_url = "http://m.icbc.com.cn/WapDynamicSite/Windroid/GoldMarket/AccResponse.aspx?datapara="

icbc_gold_price = "http://m.icbc.com.cn/WapDynamicSite/TouchPage/GoldMarket/AccInfo.aspx?ID=901001"

re_rmb_gold = r"\d{3}\.\d{2}"

def getAllPrice():
    '''
    get the real time price of rmb gold
    :return: return middle_price, purchase_price, sell_price
    '''
    res = requests.get(url=icbc_all_url, headers=headers)
    # get the middle price of rmb gold price
    price_data = re.findall(re_rmb_gold, res.text)
    middle_rmb_gold_price = float(price_data[0])
    purchase_price = middle_rmb_gold_price + 0.20
    sell_price = middle_rmb_gold_price - 0.20
    return middle_rmb_gold_price, purchase_price, sell_price

def getGoldPrice():
    '''
    get the real time price of rmb gold
    :return: return purchase_price, sell_price, high_price, low_price, middle_price
    '''
    res = requests.get(url=icbc_gold_price, headers=headers)
    # get all price about rmb gold
    price_data = re.findall(re_rmb_gold, res.text)
    return price_data

def printAllPrice():
    '''
    print all gold prices
    :return: none
    '''
    while True:
        middle_price, purchase_price, sell_price = getAllPrice()
        print "Time: " + asctime()
        print "MiddlePrice: %s PurchasePrice: %s SellPrice: %s" % (middle_price, purchase_price, sell_price)
        sleep(3)

def printGoldPrice():
    '''
    print rmb gold price
    :return:
    '''
    while True:
        purchase_price, sell_price, high_price, low_price, middle_price = getGoldPrice()
        print "Time: " + asctime()
        print "PurchasePrice: %s SellPrice: %s HighPrice: %s LowPrice: %s MiddlePrice: %s " % (purchase_price, sell_price, high_price, low_price, middle_price)
        sleep(3)

def main():
    '''
    main func
    :return:
    '''
    printGoldPrice()

if __name__ == '__main__':
    main()
