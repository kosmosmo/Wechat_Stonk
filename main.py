from wxpy import *
import airtable_talker
from datetime import datetime
from collections import defaultdict
at = airtable_talker.airtable_talk()
bot = Bot(cache_path=True)

ticker_map = defaultdict(int)
counter = [0]

from pandas_datareader import data
import math
import stonk_quoter

import datetime as dt


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
    elif stonk.startswith('!'):
        stonk = stonk[1:]
        stonk = stonk.upper()
        stonk_data = stonk_quoter.stonk(stonk)
        if not stonk_data.flag: return
        if is_alpha(stonk) and len(stonk) <= 5:  # vertifying ticker format, letter and length
            return stonk_data.earning_date()
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
            stonk_data = stonk_quoter.stonk("ES=F")
            res += "S&P" + ', $' + str(stonk_data.quotes['price']) + ', ' + str(
                    stonk_data.quotes['regularMarketChangePercent']) +'\n'
            stonk_data = stonk_quoter.stonk("NQ=F")
            res += "NAS" + ', $' + str(stonk_data.quotes['price']) + ', ' + str(
                stonk_data.quotes['regularMarketChangePercent'])+'\n'
            stonk_data = stonk_quoter.stonk("YM=F")
            res += "DOW" + ', $' + str(stonk_data.quotes['price']) + ', ' + str(
                stonk_data.quotes['regularMarketChangePercent'])
            return res

    if is_alpha(stonk) and len(stonk) <= 5:  # vertifying ticker format, letter and length

            stonk = stonk.upper()
            if stonk == "BTC":
                stonk_data = stonk_quoter.stonk("BTC-USD")
            elif stonk == "ETH":
                stonk_data = stonk_quoter.stonk("ETH-USD")
            else:
                stonk_data = stonk_quoter.stonk(stonk)
            if not stonk_data.flag: return
            ticker_map[stonk] += 1  # add to ticker map buffer
            counter[0] += 1  # add to ticker counter
            print(ticker_map)
            if counter[0] >= 5:  # counter reach 5, bulk update to airtable
                airtable_bulk_update(ticker_map)
                ticker_map.clear()
                counter[0] = 0
            if not stonk_flag:
                return stonk_data.simple_quote()
            else:
                return stonk_data.detail_quote()

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