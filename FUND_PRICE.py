# #!/usr/bin/env python
# # encoding: utf-8

'''
Some notes should be listed first.
The fund gets the fund price, and will return the dict.
The details are as follows:
dic[name]: the name of fund
dic[fundcode]: the code of fund
dic[dwjz]: the price of yesterday
dic[gsz]: the price of real time
dic[gztime]: the time of real time price
dic[gszzl]: the rate of real time
All above are encoded to unicode.
'''

import re
import requests
from time import sleep
import json

# headers info
headers={'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
        'Accept': '*/*',
        'Referer': 'http://http://m.icbc.com.cn/WapDynamicSite/Windroid/GoldMarket/',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
         }

url_template = r"http://fundgz.1234567.com.cn/js/"

def savaFundCode(path, data):
    '''
    save json in local place
    :param path: the json path
    :param data: the json data
    :return: None
    '''
    with open(path, 'wb') as f:
        json.dump(data, f)

def loadFundCode(path):
    '''
    to load the fundcode saved in local
    :param path: the json path
    :return: return dic
    '''
    with open(path, 'rb') as f:
        return json.load(f)


def getFUNDPrice(fundCode):
    '''
    to get the price of fund, whose code is funcode
    :param fundCode: fund code
    :return: return dic about this fund
    '''
    url_std = url_template + str(fundCode) + ".js"
    res = requests.get(url=url_std, headers=headers)
    data = re.findall("\{.*\}", res.text)
    jsonDic = json.loads(data[0])
    return jsonDic

def main():
    '''
    main func
    :return:
    '''
    while True:
        fund_data = getFUNDPrice(161725)
        print "Time: %s" %(fund_data["gztime"])
        print "Price: %s Rate: %s" %(fund_data["gsz"], fund_data["gszzl"])
        sleep(60)


if __name__ == '__main__':
    main()