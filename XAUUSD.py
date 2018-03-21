#!/usr/bin/env python
# encoding: utf-8

import requests
import re
import json
from time import sleep
# import threading
from yunpian_python_sdk.model import constant as YC
from yunpian_python_sdk.ypclient import YunpianClient

# The price of gold from jintou website. The header info.
headers = { 'Host': 'api.jijinhao.com',
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
            'Accept': '*/*',
            'Referer': 'http://www.cngold.org/quote/',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9'
            }

# the url of api from jintou website
url = 'https://api.jijinhao.com/sQuoteCenter/realTime.htm?code=JO_92233'

# the url of api sending email
apiurl="http://api.sendcloud.net/apiv2/mail/send"

# api params to send email
params = {"from" : "service@sendcloud.im" }

def getGoldPrice():
    '''
    to get the price of gold
    :return: dict include
    '''
    res = requests.get(url=url, headers=headers)
    raw_data = re.findall(r'"(.*),"',res.text)[0].split(',')
    data = {}
    data['Name'] = raw_data[0]
    data['Last Trade'] = raw_data[3]
    data['Bid'] = raw_data[36]
    data['Sell'] = raw_data[37]
    data['High Price'] = raw_data[4]
    data['Low Price'] = raw_data[5]
    data['Prev Close'] = raw_data[2]
    data['Open'] = raw_data[38]
    data['Change'] = raw_data[34]
    data['% Chg'] = raw_data[35]
    data['Last Updated'] = raw_data[40] + ' ' + raw_data[41]
    print(data)
    return data

def sendEmail(apiUser, apiKey, data, params, email):
    '''
    send email
    :param email: site
    :return: ojbk or not ojbk
    '''
    isSend = False
    # set the info of the email
    params[apiUser] = apiUser
    params[apiKey] = apiKey
    params["to"] = email
    # info need to send
    info = u"金价提醒" + data["Last Trade"]
    params["fromName"] = info
    params["subject"] = info
    params["html"] = info
    print params

    # send
    r = requests.post(apiurl, files={}, data=params)

    # get the result
    if r.status_code == 200:
        print "The email has been sent!"
        isSend = True
    elif r.status_code == 40005:
        print "Error, couldn't send the email!"
    return isSend

def sendSMS(apiKey, phone, data):
    '''
    to send SMS to phone
    :param ApiKey: apikey
    :param Phone: phone
    :return: ojbk or not ojbk
    '''
    isSend = False
    clnt = YunpianClient(apiKey)
    mess = "Now the price: " + data["Last Trade"]
    param = {YC.MOBILE: phone, YC.TEXT: mess}
    r = clnt.sms().single_send(param)
    r.code()

    return isSend

def main():
    '''
    main function
    :return:
    '''

    # for GitHub
    # apiUser = raw_input("Please input your apiUser:")
    # apiKey = raw_input("Please input your apiKey:")
    # smsApiKey = raw_input("Please input your smsApiKey:")
    # email = raw_input("Please input your email:")
    # phone = raw_input("Please input your phone:")
    while True:
        data = getGoldPrice()

        # sendEmail(apiUser, apiKey, data, params, email)
        # sendSMS(smsApiKey, phone, data)
        time.sleep(30)
        print "Sleep 30 sec!"

if __name__ == '__main__':
    main()