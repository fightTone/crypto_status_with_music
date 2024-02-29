import ccxt
import pandas as pd
import time
import numpy as np
from pprint import pprint
from sklearn.linear_model import LinearRegression
# from playsound import playsound
import pygame

pygame.init()

hitbtc = ccxt.bitmex()
df = pd.DataFrame(columns = ['id', 'bid', 'ask']) 
for trading_pair in hitbtc.load_markets():
	print(trading_pair)

choosen_exchange = input("enter market exchange  from above: ")

req_interval  =  int(input("request time interval: "))
dfRows_count = int(input("number of dataframe  rows: "))
number_of_loop = int(input("number of loop: "))

total_ask_prediction = 0
correct_ask_prediction = 0

total_bid_prediction = 0
correct_bid_prediction = 0

total_prediction = 0
correct_prediction = 0

prev_predask = ""
prev_predbid = ""

prev_pred = ""

def compare(last_val, predicted):
	if last_val > predicted:
		return "DROP"
	elif last_val < predicted:
		return "RISE"
	elif last_val == predicted:
		return "STATIC"

for i in range(number_of_loop):
	bitcoin_ticker = hitbtc.fetch_ticker(choosen_exchange)
	ask=float(bitcoin_ticker['ask'])
	bid = float(bitcoin_ticker['bid'])
	bitcoinPriceUSDT = ( ask + bid ) / 2

	if len(df.index) == int(dfRows_count):
		df = df.iloc[1:]
	
	# df = df.append({"id": i, "ask" : ask, "bid": bid}, ignore_index=True)
	df.loc[len(df)] = {"id": i, "ask": ask, "bid": bid}
	print("########### LATEST VALUE RESPONSE ###########")
	pprint(df[-1:])
	print("#############################################")
	model = LinearRegression()
	x = np.array(df['ask']).reshape((-1, 1))
	y = np.array(df['bid']).reshape((-1, 1))

	if len(df.index) > 2:
		model.fit(x, y)
		r_sq = model.score(x, y)

		actual_riseDrop_ask = compare([x[-2]], [x[-1]])
		actual_riseDrop_bid = compare([y[-2]],  [y[-1]])
		
		if actual_riseDrop_ask ==  "DROP":
			# playsound('audio.mp3')
			print("DROP")
			pygame.mixer.music.load('audio.mp3')
			pygame.mixer.music.play()
		elif actual_riseDrop_ask == "RISE":
			# playsound('heehee.mp3')
			print("RISE")
			pygame.mixer.music.load('heehee.mp3')
			pygame.mixer.music.play()
		else:
			print("static")
		print("===========================================================================")
	time.sleep(req_interval)
