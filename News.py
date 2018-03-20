import requests
from datetime import *
from time import sleep

def NewsFilter(raw_data,count):
    news_list = []
    news_list.clear()
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
    return news_list,last_time

def GetHistoryNews():
    res = requests.get('https://kuaixun.cngold.org/getLastNews.html?versionType=new',headers={'authority':'kuaixun.cngold.org',
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
    'Accept': '*/*',
    'Referer': 'http://www.cngold.org/quote/',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',})

    return NewsFilter(res.json()['data']['data'],res.json()['data']['count'])

def GetLatestNews(timestamp):
    res = requests.get('https://kuaixun.cngold.org/getLastNews.html?versionType=new&lastTime=' + str(timestamp),headers={'authority':'kuaixun.cngold.org',
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
    'Accept': '*/*',
    'Referer': 'http://www.cngold.org/quote/',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',})
  
    if(res.json()['data']['count'] > 0):
        return NewsFilter(res.json()['data']['data'],res.json()['data']['count'])
    else:
        return None,timestamp

if __name__ == '__main__':
    news_list,ts = GetHistoryNews()
    if not news_list is None:
        news_list.reverse()
        for news in news_list:
            print(news)
    while True:
        sleep(20)
        news_list,ts = GetLatestNews(ts)
        if not news_list is None:
            for news in news_list:
                print(news)