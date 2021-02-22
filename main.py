from wxpy import *
import airtable_talker
from collections import defaultdict
at = airtable_talker.airtable_talk()
bot = Bot(cache_path=True)

ticker_map = defaultdict(int)
counter = [0]

from pandas_datareader import data
import math


def millify(n):
    millnames = ['', ' K', ' M', ' B', ' T']
    n = float(n)
    millidx = max(0,min(len(millnames)-1,
                        int(math.floor(0 if n == 0 else math.log10(abs(n))/3))))
    return '{:.2f}{}'.format(n / 10**(3 * millidx), millnames[millidx])


def cleanup_data(ticker):
    keys = ['shortName', 'price', 'regularMarketChangePercent', 'regularMarketOpen', 'regularMarketDayHigh',
            'regularMarketDayLow',
            'regularMarketVolume', 'marketCap']
    ticker = ticker.upper()
    res = {}
    ticker_data = data.get_quote_yahoo(ticker)
    for key in keys:
        if key in ticker_data:
            res[key] = ' '.join(' '.join(ticker_data[key].to_string().split()).split(' ')[1:])
        else:
            res[key] = 0
    res['regularMarketChangePercent'] = str(round(float(res['regularMarketChangePercent']), 2)) + '%'
    res['regularMarketVolume'] = "{:,}".format(int(res['regularMarketVolume']))
    res['marketCap'] = millify(res['marketCap'])
    return res


def is_alpha(word):
    # check sif str are all alpha letter
    try:
        return word.encode('ascii').isalpha()
    except:
        return False

def airtable_bulk_update(ticker_map):
    # bulk update the ticker map to airtable
    for key,val in ticker_map.items():
        at.push_count(key,val)

def msg_stonk_quote(stonk,stonk_flag):
    if stonk.startswith('$'):
        stonk_flag = True
        stonk = stonk[1:]
    elif stonk.startswith('#'):
        stonk = stonk[1:]
        if stonk == "top":
            airtable_bulk_update(ticker_map)
            ticker_map.clear()
            counter[0] = 0
            return '\n'.join(at.top_ten())
        elif stonk == "link":
            return "https://airtable.com/shrcxCuzzyfbwEOTB"
        elif stonk == "future":
            res = 'Future:\n'
            stonk_data = cleanup_data("ES=F")
            res += "S&P" + ', $' + str(stonk_data['price']) + ', ' + str(
                    stonk_data['regularMarketChangePercent']) +'\n'
            stonk_data = cleanup_data("NQ=F")
            res += "NAS" + ', $' + str(stonk_data['price']) + ', ' + str(
                stonk_data['regularMarketChangePercent'])+'\n'
            stonk_data = cleanup_data("YM=F")
            res += "DOW" + ', $' + str(stonk_data['price']) + ', ' + str(
                stonk_data['regularMarketChangePercent'])
            return res

    if is_alpha(stonk) and len(stonk) <= 5:  # vertifying ticker format, letter and length
        try:
            print (stonk)

            stonk = stonk.upper()
            if stonk == "BTC":
                stonk_data = cleanup_data("BTC-USD")
            elif stonk == "ETH":
                stonk_data = cleanup_data("ETH-USD")
            else:
                stonk_data = cleanup_data(stonk)
            if not stonk_data: return
            ticker_map[stonk] += 1  # add to ticker map buffer
            counter[0] += 1  # add to ticker counter
            print(ticker_map)
            if counter[0] >= 5:  # counter reach 5, bulk update to airtable
                airtable_bulk_update(ticker_map)
                ticker_map.clear()
                counter[0] = 0
            if not stonk_flag:

                return str(stonk) + ', $' + str(stonk_data['price']) + ', ' + str(
                    stonk_data['regularMarketChangePercent'])
            else:
                res = "{}\n${}\nChange:       {}\nOpen:           {}\nH1gh:           {}\nLow:             {}\nvo1ume:       {}\nmarket cap: {}".format(
                    stonk_data['shortName'],
                    stonk_data['price'],
                    stonk_data['regularMarketChangePercent'],
                    stonk_data['regularMarketOpen'],
                    stonk_data['regularMarketDayHigh'],
                    stonk_data['regularMarketDayLow'],
                    stonk_data['regularMarketVolume'],
                    stonk_data['marketCap'])
                return res
        except:
            return None
    return None

@bot.register(except_self=False)
def reply_msg(msg):
    if (bot.self == msg.sender):
        stonk = str(msg.text).strip()  # stripping white space both side
        stonk_flag = False
        msg_reply =  msg_stonk_quote(stonk,stonk_flag)
        if msg_reply:
            msg.reply(msg_reply)


@bot.register(Group,TEXT,except_self=False)
def auto_reply(msg):#listening wechat message
    stonk = str(msg.text).strip()#stripping white space both side
    stonk_flag = False
    if isinstance(msg.chat, Group):
        return msg_stonk_quote(stonk,stonk_flag)



embed()
#bot.join()