from exchange import RobinhoodExchange
import time
import requests
import json
import sys
from datetime import datetime
import pandas as pd
from influxdb import DataFrameClient

class Trader(object):
	def __init__(self, config):
		self.exchange = RobinhoodExchange(config["ROBINHOOD_USER"], config["ROBINHOOD_PASS"], 1)

	def get_positions(self):
		self.owned = self.exchange.get_positions()
		self.owned_assets = {}
		for own in self.owned:
			asset = requests.get(own["instrument"]).json()["symbol"]
			amount = own["quantity"]
			price = own["average_buy_price"]
			self.owned_assets[asset] =  {"amount":amount, "price":price}
			time.sleep(2)

	def refresh_positions(self):
		for own in self.exchange.get_owned_securities():
			self.owned_assets[own]["current"] = self.exchange.get_quote(own)
			sys.stdout.write(self.owned_assets[own]["current"])
			client = DataFrameClient("influx", 8086, "root", "root", "stock")
			client.create_database("stock")
			df = pd.DataFrame(data=list(self.owned_assets[own]["current"]["last_trade_price"]),
                      index=pd.date_range(start=datetime.now().strftime("%Y-%m-%d"), periods=1, freq='D'))
			client.write_points(df, own)
			time.sleep(2)
