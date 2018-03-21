#!/usr/bin/env python
# encoding: utf-8

import requests
from datetime import *
from time import sleep
import pyttsx3

# history url
history_url = 'https://kuaixun.cngold.org/getLastNews.html?versionType=new'

# lastest url
lastest_url = 'https://kuaixun.cngold.org/getLastNews.html?versionType=new&lastTime='

# header info
headers={'authority':'kuaixun.cngold.org',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
        'Accept': '*/*',
        'Referer': 'http://www.cngold.org/quote/',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
         }
# broadcast option,1:broadcast 0:don't broadcast
broadcast = 1

def Broadcast(news):
    '''
    broadcast the news
    :param news:
    :return:
    '''
    engine = pyttsx3.init()
    engine.say(news)
    engine.runAndWait()
    

def NewsFilter(raw_data,count):
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
        news_date = date(time_data['year'] + 1900,time_data['month'] + 1,time_data['date'])
        news_time = time(time_data['hours'],time_data['minutes'],time_data['seconds'])
        news_datetime = str(news_date) + ' ' + str(news_time)
        if(i == 0):
            last_time = time_data['time']
        news_title = raw_data[i]['title']
        news = news_datetime + ' ' + news_title
        news_list.append(news)
    news_list.reverse()
    ret = news_list,last_time
    del news_list
    return ret

def GetHistoryNews():
    '''
    to get the history news from jintou
    :return:
    '''
    res = requests.get(url=history_url, headers=headers)
    return NewsFilter(res.json()['data']['data'],res.json()['data']['count'])

def GetLatestNews(timestamp):
    '''
    to get the lastest new from jintou
    :param timestamp:
    :return:
    '''
    res = requests.get(url=lastest_url + str(timestamp),headers=headers)
    if(res.json()['data']['count'] > 0):
        if (broadcast == 1):
            Broadcast('有新消息')
        return NewsFilter(res.json()['data']['data'],res.json()['data']['count'])
    else:
        return None,timestamp

def main():
    '''
    main func
    :return:
    '''
    news_list,ts = GetHistoryNews()
    if not news_list is None:
        for news in news_list:
            print(news)
            if (broadcast == 1):
                Broadcast(news)
    while True:
        news_list,ts = GetLatestNews(ts)
        if not news_list is None:
            for news in news_list:
                print(news)
                if (broadcast == 1):
                    Broadcast(news)
            sleep(5)
        sleep(15)

if __name__ == '__main__':
    main()
