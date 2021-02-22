from pandas_datareader import data
import math


def millify(n):
    millnames = ['', ' K', ' M', ' B', ' T']
    n = float(n)
    millidx = max(0,min(len(millnames)-1,
                        int(math.floor(0 if n == 0 else math.log10(abs(n))/3))))
    return '{:.2f}{}'.format(n / 10**(3 * millidx), millnames[millidx])

def cleanup_data(ticker):
        keys = ['shortName','price','regularMarketChangePercent','regularMarketOpen','regularMarketDayHigh','regularMarketDayLow',
                'regularMarketVolume','marketCap']
        ticker = ticker.upper()
        res={}
        ticker_data = data.get_quote_yahoo(ticker)
        for key in keys:
            if key in ticker_data:
                res[key] =' '.join(' '.join(ticker_data[key].to_string().split()).split(' ')[1:])
            else:
                res[key] = 0
        res['regularMarketChangePercent'] = str(round(float(res['regularMarketChangePercent']),2)) +'%'
        res['regularMarketVolume'] = "{:,}".format(int(res['regularMarketVolume']))
        res['marketCap']=millify(res['marketCap'])
        return res


print (cleanup_data('NQ=F'))
#print (data.get_quote_yahoo('cgc').to_string())