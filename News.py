#!/usr/bin/env python
# encoding: utf-8
'''
If using the weixin message feature, complete the wx info first
'''

import requests
from datetime import *
from time import sleep
import pyttsx3
import random
import json

# message url
message_url = 'https://wx2.qq.com/cgi-bin/mmwebwx-bin/webwxsendmsg'

# history url
history_url = 'https://kuaixun.cngold.org/getLastNews.html?versionType=new'

# lastest url
lastest_url = 'https://kuaixun.cngold.org/getLastNews.html?versionType=new&lastTime='

# header info
headers = {
    'authority':'kuaixun.cngold.org',
    'Connection':'keep-alive',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
    'Accept':'*/*',
    'Referer':'http://www.cngold.org/quote/',
    'Accept-Encoding':'gzip, deflate, br',
    'Accept-Language':'zh-CN,zh;q=0.9'
}

# wx header info
wx_headers = {
    'Host':'wx2.qq.com',
    'Content-Length':'383',
    'Content-Type':'application/json;charset=UTF-8',
    'Connection':'keep-alive',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
    'Accept':'application/json, text/plain, */*',
    'Origin':'https://wx2.qq.com',
    'Referer':'https://wx2.qq.com/',
    'Accept-Encoding':'gzip, deflate, br',
    'Accept-Language':'zh-CN,zh;q=0.9',
    'Cookie':''#need modify
}

# wx payload
'''
Values of 'BaseRequest' and 'Msg' should be updated as your account refering to the request of Weixin web client
'''
wx_msg_payload = {
    "BaseRequest": {
        "Uin": 0,#need modify
        "Sid": "",#need modify
        "Skey": "",#need modify
        "DeviceID": ""#need modify
    },
    "Msg": {
        "Type":1,
        "Content":"",
        "FromUserName":"",#need modify
        "ToUserName":"",
        "LocalID":"",#need modify
        "ClientMsgId":""
    },
    "Scene": 0
}

# wx accounts you want to send
wx_ToUserName_list = []#need add

# broadcast option,1:broadcast 0:don't broadcast
broadcast = 1

# send weixin message option,1:send 0:don't send
sendwx = 0

def SendWxMessage(ToUserName,Content,last_msgid):
    '''
    seng weixin message
    :param ToUserName:
    :param Content:
    :param last_msgid:
    :return:
    '''
    msgid = str(random.randint(1,10000))
    while msgid == last_msgid:
        msgid = str(random.randint(1,10000))
    wx_msg_payload['Msg']['Content'] = Content
    wx_msg_payload['Msg']['ClientMsgId'] = msgid
    wx_msg_payload['Msg']['ToUserName'] = ToUserName
    res = requests.post(url=message_url, headers=wx_headers, data=json.dumps(wx_msg_payload,ensure_ascii=False).encode('utf-8'))
    return msgid

def Broadcast(news):
    '''
    broadcast the news
    :param news:
    :return:
    '''
    engine = pyttsx3.init()
    engine.say(news)
    engine.runAndWait()


def NewsFilter(raw_data, count):
    '''
    get the main info from news
    :param raw_data:
    :param count:
    :return:
    '''
    news_list = []
    # bug: Python2 does not have func clear(), in this I use del to fix.
    # news_list.clear()
    last_time = 0
    for i in range(count):
        time_data = raw_data[i]['pubTime']
        news_date = date(time_data['year'] + 1900, time_data['month'] + 1,
                         time_data['date'])
        news_time = time(time_data['hours'], time_data['minutes'],
                         time_data['seconds'])
        news_datetime = str(news_date) + ' ' + str(news_time)
        if (i == 0):
            last_time = time_data['time']
        news_title = raw_data[i]['title']
        news = news_datetime + ' ' + news_title
        news_list.append(news)
    news_list.reverse()
    ret = news_list, last_time
    del news_list
    return ret


def GetHistoryNews():
    '''
    to get the history news from jintou
    :return:
    '''
    res = requests.get(url=history_url, headers=headers)
    return NewsFilter(res.json()['data']['data'], res.json()['data']['count'])


def GetLatestNews(timestamp):
    '''
    to get the lastest new from jintou
    :param timestamp:
    :return:
    '''
    res = requests.get(url=lastest_url + str(timestamp), headers=headers)
    if (res.json()['data']['count'] > 0):
        if (broadcast == 1):
            Broadcast('有新消息')
        return NewsFilter(res.json()['data']['data'],
                          res.json()['data']['count'])
    else:
        return None, timestamp


def main():
    '''
    main func
    :return:
    '''
    last_msgid = '1'
    news_list,ts = GetHistoryNews()
    if not news_list is None:
        for news in news_list:
            print(news)
            if (sendwx == 1):
                for username in wx_ToUserName_list:
                    last_msgid = SendWxMessage(username,news,last_msgid)
            if (broadcast == 1):
                Broadcast(news)
    while True:
        news_list,ts = GetLatestNews(ts)
        if not news_list is None:
            for news in news_list:
                print(news)
                if (sendwx == 1):
                    for username in wx_ToUserName_list:
                        last_msgid = SendWxMessage(username,news,last_msgid)
                if (broadcast == 1):
                    Broadcast(news)
            sleep(5)
        sleep(15)
    
if __name__ == '__main__':
    main()
