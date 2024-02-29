import ccxt
import pandas as pd
import time
import numpy as np
from pprint import pprint
from sklearn.linear_model import LinearRegression
import pygame
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk


pygame.init()

# Create Tkinter window
window = tk.Tk()
window.title("Crypto Status")
window.geometry("400x300")

# Add background image
# Open the JPEG image using Pillow
background_image = Image.open("background.png")
background_photo = ImageTk.PhotoImage(background_image)

# Create a Tkinter label with the background image
background_label = tk.Label(window, image=background_photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Initialize CCXT
hitbtc = ccxt.bitmex()

# Define variables
chosen_exchange_var = tk.StringVar()
req_interval_var = tk.IntVar()
number_of_loop_var = tk.IntVar()

# Function to fetch trading pairs
def fetch_trading_pairs():
    trading_pairs = []
    for trading_pair in hitbtc.load_markets():
        trading_pairs.append(trading_pair)
    return trading_pairs

def compare(last_val, predicted):
	if last_val > predicted:
		return "DROP"
	elif last_val < predicted:
		return "RISE"
	elif last_val == predicted:
		return "STATIC"

# Function to start fetching data
def start_fetching():
    chosen_exchange = chosen_exchange_var.get()
    req_interval = req_interval_var.get()
    df_rows_count = 3
    number_of_loop = number_of_loop_var.get()
    
    df = pd.DataFrame(columns=['id', 'bid', 'ask'])

    total_ask_prediction = 0
    correct_ask_prediction = 0

    total_bid_prediction = 0
    correct_bid_prediction = 0

    total_prediction = 0
    correct_prediction = 0

    prev_predask = ""
    prev_predbid = ""

    prev_pred = ""

    for i in range(number_of_loop):
        bitcoin_ticker = hitbtc.fetch_ticker(chosen_exchange)
        ask = float(bitcoin_ticker['ask'])
        bid = float(bitcoin_ticker['bid'])
        bitcoinPriceUSDT = (ask + bid) / 2

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
            actual_riseDrop_bid = compare([y[-2]], [y[-1]])

            if actual_riseDrop_ask == "DROP":
                print("DROP")
                pygame.mixer.music.load('audio.mp3')
                pygame.mixer.music.play()
            elif actual_riseDrop_ask == "RISE":
                print("RISE")
                pygame.mixer.music.load('heehee.mp3')
                pygame.mixer.music.play()
            else:
                print("STATIC")
            print("===========================================================================")
        time.sleep(req_interval)


# Create Tkinter widgets
trading_pairs_label = tk.Label(window, text="Trading Pairs:", highlightthickness=0)
trading_pairs_label.pack(pady=5)

trading_pairs_combobox = ttk.Combobox(window, values=fetch_trading_pairs(), textvariable=chosen_exchange_var, width=15)
trading_pairs_combobox.pack(pady=5)

req_interval_label = tk.Label(window, text="Interval (sec):", highlightthickness=0)
req_interval_label.pack(pady=5)

req_interval_entry = tk.Entry(window, textvariable=req_interval_var, width=5)
req_interval_entry.pack(pady=5)

number_of_loop_label = tk.Label(window, text="Number of Loops:", highlightthickness=0)
number_of_loop_label.pack(pady=5)

number_of_loop_entry = tk.Entry(window, textvariable=number_of_loop_var, width=5)
number_of_loop_entry.pack(pady=5)

# Customize the button color to green and round the corners
start_button = tk.Button(window, text="Start Fetching", command=start_fetching, bg="green", borderwidth=0, relief="solid", highlightthickness=0, width=15)
start_button.pack(pady=5)

# Run Tkinter event loop
window.mainloop()