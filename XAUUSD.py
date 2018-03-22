#!/usr/bin/env python
# encoding: utf-8

import re
import requests
import json
from time import sleep
from SmsEmailKey import loadKey
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
    # split price int and float
    data['int'] = raw_data[3][0:4]
    data['float'] = raw_data[3][5:7]
    data['Bid'] = raw_data[36]
    data['Sell'] = raw_data[37]
    data['High Price'] = raw_data[4]
    data['Low Price'] = raw_data[5]
    data['Prev Close'] = raw_data[2]
    data['Open'] = raw_data[38]
    data['Change'] = raw_data[34]
    data['% Chg'] = raw_data[35]
    data['Last Updated'] = raw_data[40] + ' ' + raw_data[41]
    data['time'] = raw_data[41]
    # split time
    data['hour'] = raw_data[41][0:2]
    data['minute'] = raw_data[41][3:5]
    data['second'] = raw_data[41][6:8]
    return data

def sendEmail(apiUser, apiKey, data, params, email):
    '''
    send email
    :param email: site
    :return: ojbk or not ojbk
    '''
    isSend = False
    # set the info of the email
    params['apiUser'] = apiUser
    params['apiKey'] = apiKey
    params["to"] = email
    # info need to send
    info = u"金价提醒" + data["Last Trade"]
    params["fromName"] = info
    params["subject"] = info
    params["html"] = info

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
    mess = u"【晶透水果店】您关注的水果已经在" + \
            data['hour'] + \
            ':' + \
            data['minute'] + \
            u"补货，目前价格为" + \
            data['int'] + \
            '.' + \
            data['float'] + \
            u"，祝您生活愉快！"
    param = {YC.MOBILE: phone, YC.TEXT: mess}
    r = clnt.sms().single_send(param)
    if r.code() == 0:
        isSend = False

    return isSend

def main():
    '''
    main function
    :return:
    '''

    # for GitHub, the real info can get from
    # email from https://www.sendcloud.net
    # sms from https://www.yunpian.com
    # apiUser = raw_input("Please input your apiUser:")
    # apiKey = raw_input("Please input your apiKey:")
    # smsApiKey = raw_input("Please input your smsApiKey:")
    # email = raw_input("Please input your email:")
    # phone = raw_input("Please input your phone:")

    # for myself, my key is saved in ..\
    key = loadKey(r'..\key.pkl')
    apiUser = key['apiUser']
    apiKey = key['apiKey']
    smsApiKey = key['smsApiKey']
    email = key['email']
    phone = key['phone']
    while True:
        data = getGoldPrice()

        while True:
            print "Sending email."
            if sendEmail(apiUser, apiKey, data, params, email):
                print "Sent."
                break
            print "Sent Error."
            sleep(5)

        # while True:
        #     print "Sending sms."
        #     if sendSMS(smsApiKey, phone, data):
        #         print "Sent."
        #         break
        #     print "Sent Error."
        #     sleep(5)
        sleep(30)
        print "Sleep 30 sec!"

if __name__ == '__main__':
    main()