
import airtable_talker
from datetime import datetime
from collections import defaultdict
import datetime as dt
from pandas_datareader import data
import math

def isNowInTimePeriod(startTime, endTime, nowTime):
    #print (startTime,endTime,nowTime)
    if startTime < endTime:
        return nowTime >= startTime and nowTime <= endTime
    else:
        #Over midnight:
        return nowTime >= startTime or nowTime <= endTime

def millify(n):
    millnames = ['', ' K', ' M', ' B', ' T']
    n = float(n)
    millidx = max(0,min(len(millnames)-1,
                        int(math.floor(0 if n == 0 else math.log10(abs(n))/3))))
    return '{:.2f}{}'.format(n / 10**(3 * millidx), millnames[millidx])

def is_alpha(word):
    # check sif str are all alpha letter
    try:
        return word.encode('ascii').isalpha()
    except:
        return False

def convert_week(time):
    date = str(datetime.fromtimestamp(int(time)))[5:-3]
    week = str(datetime.fromtimestamp(int(time)).strftime('%A'))
    return date + ', ' + week


def convert_er(times):
    if times[0] == '0':
        return 'NA'
    if times[0] == times[1]:
        return convert_week(times[0])
    else:
        return "\n" + convert_week(times[0]) + ' -\n' +convert_week(times[1])


def cleanup_data(ticker):
    keys = ['shortName', 'price', 'regularMarketChangePercent', 'regularMarketOpen', 'regularMarketDayHigh',
            'regularMarketDayLow',
            'regularMarketVolume',
            'marketCap',
            'earningsTimestampStart',
            'earningsTimestampEnd',
            'postMarketPrice',
            'postMarketChangePercent',
            'preMarketPrice',
            'preMarketChangePercent'
            ]
    ticker = ticker.upper()
    res = {}
    ticker_data = data.get_quote_yahoo(ticker)
    for key in keys:
        if key in ticker_data:
            res[key] = ' '.join(' '.join(ticker_data[key].to_string().split()).split(' ')[1:])
        else:
            res[key] = '0'
    res['regularMarketChangePercent'] = str(round(float(res['regularMarketChangePercent']), 2)) + '%'
    res['regularMarketVolume'] = "{:,}".format(int(res['regularMarketVolume']))
    res['marketCap'] = millify(res['marketCap'])
    res['postMarketChangePercent'] = str(round(float(res['postMarketChangePercent']), 2)) + '%'
    res['preMarketChangePercent'] = str(round(float(res['preMarketChangePercent']), 2)) + '%'
    res['earning'] = convert_er([res['earningsTimestampStart'],res['earningsTimestampEnd']])
    #print (res['preMarketPrice'],res['postMarketPrice'])
    return res

#print (isNowInTimePeriod(dt.time(16,00), dt.time(4,00), dt.datetime.now().time()))
class stonk(object):
    def __init__(self,ticker):
        self.ticker = ticker.upper()
        try:
            self.quotes = cleanup_data(ticker)
            self.flag = True
        except:
            self.flag = False


    def get_market_time(self):
        if isNowInTimePeriod(dt.time(4,00), dt.time(9,30), dt.datetime.now().time()) and self.quotes['preMarketPrice'] != '0':
            return 'pre'
        elif isNowInTimePeriod(dt.time(16,00), dt.time(4,00), dt.datetime.now().time())  and self.quotes['postMarketPrice'] != '0' :
            return 'post'
        else:
            return 'open'

    def simple_quote(self):
        if self.get_market_time() == 'pre':
            return str(self.ticker) + ', pre $' + str(self.quotes['preMarketPrice']) + ', ' + str(
                        self.quotes['preMarketChangePercent'])
        elif self.get_market_time() == 'post':
            return str(self.ticker) + ', after $' + str(self.quotes['postMarketPrice']) + ', ' + str(
                        self.quotes['postMarketChangePercent'])
        else:
            return str(self.ticker) + ', $' + str(self.quotes['price']) + ', ' + str(
                        self.quotes['regularMarketChangePercent'])

    def earning_date(self):
        return self.ticker + ', ' + self.quotes['earning']

    def detail_quote(self):
        res = "{}\n${}\nChange:       {}\nOpen:           {}\nH1gh:           {}\nLow:             {}\nvo1ume:       {}\nmarket cap: {}".format(
            self.quotes['shortName'],
            self.quotes['price'],
            self.quotes['regularMarketChangePercent'],
            self.quotes['regularMarketOpen'],
            self.quotes['regularMarketDayHigh'],
            self.quotes['regularMarketDayLow'],
            self.quotes['regularMarketVolume'],
            self.quotes['marketCap'])
        if self.get_market_time() == 'pre':
            res += "\n\n${}\nPreChange  {}".format(
                self.quotes['preMarketPrice'],
                self.quotes['preMarketChangePercent']
            )
        elif self.get_market_time() == 'post':
            res += "\n\n${}\nPostChange {}".format(
                self.quotes['postMarketPrice'],
                self.quotes['postMarketChangePercent']
            )
        return res

a = stonk('bad')
print (a.flag)

