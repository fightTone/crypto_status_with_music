import ccxt
import pandas as pd
import time
import numpy as np
from pprint import pprint
from sklearn.linear_model import LinearRegression
from playsound import playsound

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
	# fetch the BTC/USDT ticker for use in converting assets to price in USDT
	bitcoin_ticker = hitbtc.fetch_ticker(choosen_exchange)
	ask=float(bitcoin_ticker['ask'])
	bid = float(bitcoin_ticker['bid'])
	# ask=float(bitcoin_ticker['info']['ask'])
	# bid = float(bitcoin_ticker['info']['bid'])
	bitcoinPriceUSDT = ( ask + bid ) / 2

	# print("ask: "+str(float(bitcoin_ticker['info']['ask'])))
	# print("bid: "+str(float(bitcoin_ticker['info']['bid'])))
	# print(bitcoinPriceUSDT)
	if len(df.index) == int(dfRows_count):
		df = df.iloc[1:]
	
	df = df.append({"id": i, "ask" : ask, "bid": bid}, ignore_index=True)
	print("########### LATEST VALUE RESPONSE ###########")
	pprint(df[-1:])
	print("#############################################")
	model = LinearRegression()
	x = np.array(df['ask']).reshape((-1, 1))
	y = np.array(df['bid']).reshape((-1, 1))

	if len(df.index) > 2:
		model.fit(x, y)
		r_sq = model.score(x, y)
		# print('coefficient of determination:', r_sq)
		# print('intercept:', model.intercept_)
		# print('slope:', model.coef_)

		actual_riseDrop_ask = compare([x[-2]], [x[-1]])
		actual_riseDrop_bid = compare([y[-2]],  [y[-1]])
		
		prev_value = ([x[-2]][0][0] + [y[-2]][0][0])/2
		current_value = ([x[-1]][0][0] + [y[-1]][0][0])/2
		
		actual_riseDrop = compare(prev_value,  current_value)
		if actual_riseDrop ==  "DROP":
			playsound('audio.mp3')
		elif actual_riseDrop == "RISE":
			playsound('heehee.mp3')

		if prev_pred != "":
			print("------------------------------------")
			print("prev value: "+str(prev_value))
			print("current value: "+str(current_value))
			if prev_pred == actual_riseDrop:
				print("previous prediction is CORRECT that it will "+prev_pred)
				correct_prediction+=1
			else:
				print("previous prediction is WRONG that it will "+prev_pred)
			print("------------------------------------")

			total_prediction+=1
			# print("------------------------------------")
			# print("prev_ask result: "+str([x[-2]][0][0]))
			# print("current_ask result: "+str([x[-1]][0][0]))
			# if prev_predask == actual_riseDrop_ask:
			# 	print("previous ask prediction is CORRECT that it will "+prev_predask)
			# 	correct_ask_prediction+=1
			# else:
			# 	print("previous ask prediction is WRONG that it will "+prev_predask)
			# print("------------------------------------")

			# print("------------------------------------")
			# print("prev_bid result: "+str([y[-2]][0][0]))
			# print("current_bid result: "+str([y[-1][0]][0]))
			# if prev_predbid == actual_riseDrop_bid:
			# 	print("previous bid prediction is CORRECT that it will "+prev_predbid)
			# 	correct_bid_prediction+=1
			# else:
			# 	print("previous bid prediction is WRONG that it will "+prev_predbid)
			# print("------------------------------------")
			# total_ask_prediction+=1
			# total_bid_prediction+=1

		x_pred = model.predict([y[-1]])
		y_pred = model.predict([x[-1]])
		pred = (x_pred[0][0] + y_pred[0][0])/2

		riseDrop_ask  = compare([x[-1]][0][0],x_pred[0][0])
		riseDrop_bid = compare([y[-1]][0][0],y_pred[0][0])
		riseDrop = compare(current_value, pred)

		print("*************************************")
		print('prediction base on previous result: ', pred)
		# print("current value:  ",  current_value)
		print("Prediction: value will "+ riseDrop +" by approx. "+str(abs(current_value - pred))+" for the next "+str(req_interval)+" sec")
		print("*************************************")

		# print("*************************************")
		# # print('predicted ASK response: ', x_pred)
		# print("ask will "+ riseDrop_ask +" by approx. "+str(abs([x[-1]][0][0]-x_pred[0][0]))+"for the next "+str(req_interval)+" sec")
		
		# # print('predicted BID response: ', y_pred)
		# print("bid will "+ riseDrop_bid +" by approx. "+str(abs([y[-1]][0][0]-y_pred[0][0]))+"for the next "+str(req_interval)+" sec")
		# print("*************************************")

		prev_predask = riseDrop_ask
		prev_predbid = riseDrop_bid
		prev_pred = riseDrop
		if total_prediction!=0:
			if correct_prediction == 0:
				print("prediction accuracy: 0.0%")
			else:
				print("prediction accuracy: "+str((correct_prediction/total_prediction)*100)+"%")
			# if correct_ask_prediction == 0:
			# 	print("ask prediction accuracy: 0.0%")
			# else:
			# 	print("ask prediction accuracy: "+str((correct_ask_prediction/total_ask_prediction)*100)+"%")
			# if correct_bid_prediction == 0:
			# 	print("bid prediction accuracy: 0.0%")
			# else:
			# 	print("bid prediction accuracy: "+str((correct_bid_prediction/total_bid_prediction)*100)+"%")
		print("===========================================================================")
	time.sleep(req_interval)
