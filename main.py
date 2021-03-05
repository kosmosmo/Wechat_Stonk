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
black_list = ['Flushing, Main Street Bets 🚀']

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
        keywords = ['#casino','h','hit','s','stand','skip','join','start']
        if stonk.lower() in keywords:
            casino(msg,msg.sender.name)
        else:
            stonk_flag = False
            msg_reply =  msg_stonk_quote(stonk,stonk_flag)
            if msg_reply:
                msg.reply(msg_reply)


@bot.register(Group,TEXT,except_self=False)
def auto_reply(msg):#listening wechat message
    stonk = str(msg.text).strip()#stripping white space both side
    keywords = ['#casino', 'h', 'hit', 's', 'stand', 'skip', 'join', 'start']
    if stonk.lower() in keywords:
        casino(msg,msg.member.name)
    else:
        stonk_flag = False
        if isinstance(msg.chat, Group):
            if "雪" in msg.chat.name in black_list: return
            return msg_stonk_quote(stonk,stonk_flag)

import time,blackjack_player,blackjack_bot



groups = {}
def casino(msg,player_name):
    global groups
    group_name = msg.chat.name
    command = str(msg.text).strip().lower()
    if command == '#casino':
        groups[group_name] =  blackjack_bot.game({})
        print ('created')
        res = '$$Main Street Bet Casino$$\n♣ ♦ ♥ ♠ ♣ ♦ ♥ ♠ ♣ ♦ ♥ ♠\n加入了balance和dealer\nEnter "join" to join the game\nEnter "start" to start\n游戏结束输入"start"继续游戏\nDuring game,"h" for hit\nDuring game,"s" for stand\n♣ ♦ ♥ ♠ ♣ ♦ ♥ ♠ ♣ ♦ ♥ ♠'
        msg.chat.send(res)
    elif command == 'join' and not groups[group_name].start:
        groups[group_name].players[player_name] = blackjack_player.player(player_name)
        res = player_name + ' joined the game'
        print (res)
    elif command == 'start' and not groups[group_name].start and len(groups[group_name].players) != 0:
        groups[msg.chat.name].start = True
        res ='\n----------------------------\n'.join (groups[group_name].deal())
        groups[group_name].check_winner()
        msg.chat.send('Dealer is: ' +  groups[msg.chat.name].orders[groups[msg.chat.name].dealer] + '\n----------------------------\n' + res)
    elif (command == 'hit' or command == 'h') and groups[group_name].start and player_name in groups[group_name].players and groups[group_name].move[player_name] != 's':
        groups[group_name].move[player_name] = 'h'
        print (groups[group_name].move)
        if groups[group_name].check_move() == len(groups[group_name].players):
            res =  '\n----------------------------\n'.join (groups[group_name].next())
            msg.chat.send('Dealer is: ' +  groups[msg.chat.name].orders[groups[msg.chat.name].dealer] + '\n----------------------------\n' +res)
            winner = groups[group_name].check_winner()
            temp = {}
            for key,val in groups[group_name].move.items():
                if groups[group_name].players[key].stand != True:
                    temp[key] = ''
                else:
                    temp[key] = val
            groups[group_name].move= temp
            if winner:
                balancing = ''
                for key,val in groups[group_name].balance.items():
                    if val == 1:val = '+1'
                    balancing += key + ':' + str(val)+', '
                msg.chat.send(balancing)
                groups[group_name].start = False
                groups[group_name].new_game()
    elif (command == 'stand' or command == 's') and groups[group_name].start and player_name in groups[group_name].players and  groups[group_name].move[player_name]  == '':
        groups[group_name].move[player_name] = 's'
        print (groups[group_name].move)
        if groups[group_name].check_move() == len(groups[group_name].players):
            res =  '\n----------------------------\n'.join (groups[group_name].next())
            msg.chat.send('Dealer is: ' +  groups[msg.chat.name].orders[groups[msg.chat.name].dealer] + '\n----------------------------\n' +res)
            winner = groups[group_name].check_winner()
            temp = {}
            for key, val in groups[group_name].move.items():
                if groups[group_name].players[key].stand != True:
                    temp[key] = ''
                else:
                    temp[key] = val
            groups[group_name].move = temp
            if winner:
                balancing = ''
                for key, val in groups[group_name].balance.items():
                    if val == 1: val = '+1'
                    balancing += key + ':' + str(val) + ', '
                msg.chat.send(balancing)
                groups[group_name].start = False
                groups[group_name].new_game()




"""
group = {}

@bot.register(Group,TEXT,except_self=False)
def auto_reply(msg):#listening wechat message
    if str(msg.text) == "#casino" and msg.chat.name not in group:
        group[msg.chat.name] = {}

def 
"""
embed()
bot.join()