#!/usr/bin/env python
import ystockquote
from datetime import date
import pickle
import os
import csv
import time
from pprint import pprint

"""
where to save files
"""
def getsavename(stk,ext):
    return 'data/' + stk + ext

"""
get historical data from a stock ticker name
 - save in pickle format
 - update (and save) if already exists

"""
def getsavedata(stk):
    firstday = '2013-01-01'
    today    = date.today().strftime('%Y-%m-%d')

    savename=getsavename(stk,'.p')

    # TODO: make path for savename
    # mkdir(dirname(savename))

    # load (and update if needed)
    if os.path.exists(savename):
      quotes=pickle.load( open(savename, "rb") )
      lastquote = sorted(quotes.keys())[-1]

      # update with new values
      if lastquote != today:
         nextdate = datetime.datetime.strptime(lastquote,'%Y-%m-%d') + datetime.timedelta(days=1)
         quotes.update( ystockquote.get_historical_prices(stk,nextdate,today) )
         savestock(stk,quotes)

    # get all new
    else:
      quotes  = ystockquote.get_historical_prices(stk,firstday,today)
      savestock(stk,quotes)

    return quotes



"""
ystockquote format to csv ( for R)

"""
def ystocktoCSV(stk,quotes):
   savename=getsavename(stk,'.csv')
   # date, 'Close', 'High', 'Low', 'Open', 'Volume','Adj Close'
   twod = [  [k]+[vv for  kk,vv in v.items()] for k,v in quotes.items() ]
   with open(savename,'w',newline='') as csvfile:
     w = csv.writer(csvfile,quoting=csv.QUOTE_MINIMAL)
     w.writerow(['Date','Close','High','Low','Open','Volume','AdjClose'])
     for line in twod:
       w.writerow([stk]+line)

"""
save stocks in pickle and csv format
"""
def savestock(stk,quotes):
     pickle.dump(quotes, open( getsavename(stk,'.p') , "wb") )
     ystocktoCSV(stk,quotes)



"""
main
 for all stocks in stocks.txt
 get historical data from 2013 onward, save in data/stock.csv
"""

for l in open('stocks.txt','r'):
  stk=l.strip()
  pprint(stk)
  getsavedata(stk)
  time.sleep(5)




