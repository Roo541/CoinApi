import numpy as np
import pandas as pd
import pandas_datareader.data as web
import datetime as dt
import time
import math
import API
from binance.client import Client
import matplotlib.pyplot as plt
from matplotlib import style

style.use('ggplot')

client = Client(API.api_key, API.secret_key)
symbol = 'BTCUSDT'
high = 0.0 
low = 100000.0
buy_price = 0.0
buy_target = 1000000.0
sell_target = 10000000.0
bitcoin = 0.0
bank_account = 100000.0
networth = 0.0 
x = 'none'
twenty = 0.0
thirty = 0.0
fifty = 0.0
sixty = 0.0
y = 'none'
initital = 100000.0
order = True
date_low = 0
date_high = 0
percent_r = [(0)]*100000

while order:
	
	btc = client.get_historical_klines_generator(symbol, '30m',  '60 days ago UTC')
	i = 0
	t = 0
	for kline in btc:
		i = i + 1
		if i > 100:
			i = 0
			high = 0.0
			low = 1000000.0
		timestamp = dt.datetime.fromtimestamp(kline[0]/1000)
		dummy = timestamp
		current = float(kline[4])
		networth = bank_account + bitcoin*current
		#stop loss
		if current < (buy_price - .025*buy_price) and y == 'in trade':
			bank_account = bank_account + bitcoin*current -.00075*bitcoin*current
			bitcoin = 0
			networth = bank_account + bitcoin*current
			sell_target = 10000000.0
			y = 'none'
					
		print timestamp, 'price $', kline[4]
		print 'trigger at', x
		print 'Buy target', buy_target
		print 'Sell target', sell_target
		print 'Buy price', buy_price	
		print 'High:', high
		print 'Low:', low
		#finding high and low prices within window	
		if current > high:
			high = current
			date_high = timestamp
		if current < low:
			low = current
			date_low = timestamp
		#Making sure high price date is after low price date
		#Assigning targets
		if date_high > date_low and high != 0.0 and low != 100000.0:
			diff = (high - low)
			twenty = high - .236*diff
			thirty = high - .382*diff
			fifty = high - .50*diff
			sixty = high - .618*diff
		
		if current < twenty:
			buy_target = twenty + .0005*twenty
			x = 'twenty'
		if current < thirty:
			buy_target = thirty + .0005*thirty
			x = 'thirty'
		if current < fifty:
			buy_target = fifty + .0005*fifty
			x = 'fifty'
		if current < sixty:
			buy_target = sixty + .0005*sixty
			x = 'sixty'
		
		if current > buy_target and y !='in trade' and bank_account > current:
			bitcoin = float(bank_account/current)
			bank_account = bank_account - bitcoin*current - .00075*bank_account		
			networth = bank_account + bitcoin*current
			buy_price = current
			sell_target = high + 1.618*diff
			buy_target = 1000000.0
			y = 'in trade'

		if current > sell_target and bitcoin != 0:
			bank_account = bank_account + bitcoin*current -.00075*bitcoin*current
			bitcoin = 0
			networth = bank_account + bitcoin*current
			sell_target = 10000000.0
			y = 'none'
		
		print 'Bank account: ', bank_account
		print 'BTC:', bitcoin
		print 'Networth:', networth

		percent_r[t] = (networth/100000.0-1)*100
		print 'Return Percentage', percent_r[t],'%', '\n'
		t = t +1
		order = False
np.trim_zeros(percent_r)	
plt.plot(percent_r)
plt.show()
		
		
		# ~ time.sleep(1)
	# ~ timestamp = dt.datetime.fromtimestamp(btc[0][0]/1000)
	# ~ print btc[0][4]
	#print timestamp, '$', btc[0][4]
	
