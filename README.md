# XAUUSD-Price-Realtime
- Allows us to watch the price of XAUUSD in real time.
- Datas come from [金投网](https://www.cngold.org/).

---

# News
- Allws us to watch the real finacail news all over the world.
- News comes from [金投网](https://www.cngold.org/).

---

# RMBGOLD_ICBC_PRICE
- Allws us to watch the real RMB_GOLD from ICBC.
- Precious Metals Price datas come from [Precious Metals Price](http://m.icbc.com.cn/WapDynamicSite/TouchPage/GoldMarket/Default.aspx).
- Gold Price datas come from [Gold Price](http://m.icbc.com.cn/WapDynamicSite/TouchPage/GoldMarket/AccInfo.aspx?ID=901001).

---

# Logs
### 2018-3-20
- Update `XAUUSD.py` function send email and send sms.
### 2018-3-21
- Update `News.py` fix the bug: python2 list doesn't have func:clear().
### 2018-3-22
- Finish send sms func
- Create `SMsEmailKey.py` Func save and load API_KEY

### 2018-3-28
- Create `RMBGOLD_ICBC_PRICE.py` to get the real-time RMB GOLD price from ICBC website.
- Have the middle price, purchase price and sell price.

### 2018-3-29
- Update `RMBGOLD_ICBC_PRICE.py` change `getGoldPrice()` into `getAllPrice`, which to catch all price about Precious Metals.
- Create `RMBGOLD_ICBC_PRICE.py` func `getGoldPrice()` to catch all price about RMB GOLD.
