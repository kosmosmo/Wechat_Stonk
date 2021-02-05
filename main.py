from wxpy import *
import stockquotes,airtable_talker
from collections import defaultdict
at = airtable_talker.airtable_talk()
bot = Bot(cache_path=True)

ticker_map = defaultdict(int)
counter = [0]
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

@bot.register(Group,TEXT)
def auto_reply(msg):
    #listening wechat message
    stonk = str(msg.text).strip()
    #stripping white space both side
    if isinstance(msg.chat, Group) and is_alpha(stonk) and len(stonk) <=5: #vertifying ticker format, letter and length
        try:
            ticker_map[stonk] += 1 #add to ticker map buffer
            counter[0] += 1#add to ticker counter
            print (ticker_map)
            st = stockquotes.Stock(stonk)
            if counter[0]>=5:#counter reach 5, bulk update to airtable
                airtable_bulk_update(ticker_map)
                ticker_map.clear()
                counter[0] = 0
            return  str(st.name)+ ', ' + str(st.current_price) + ', ' + str(st.increase_percent)+'%'
        except:
            pass
    elif isinstance(msg.chat, Group) and stonk == "#top":
        print(counter[0])
        airtable_bulk_update(ticker_map)
        ticker_map.clear()
        counter[0] = 0
        return '\n'.join(at.top_ten())
    elif isinstance(msg.chat, Group) and stonk == "#link":
        print(counter[0])
        airtable_bulk_update(ticker_map)
        ticker_map.clear()
        counter[0] = 0
        return "https://airtable.com/shrLdYMX4LrW6cUpb"
    else:
        pass





embed()
#bot.join()