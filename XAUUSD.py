import requests
import re

res = requests.get('https://api.jijinhao.com/sQuoteCenter/realTime.htm?code=JO_92233',headers={'Host': 'api.jijinhao.com',
'Connection': 'keep-alive',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
'Accept': '*/*',
'Referer': 'http://www.cngold.org/quote/',
'Accept-Encoding': 'gzip, deflate, br',
'Accept-Language': 'zh-CN,zh;q=0.9'})

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