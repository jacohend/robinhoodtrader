from exchange import RobinhoodExchange
import time
import requests
import json
import sys
import traceback
from datetime import datetime
import pandas as pd
from influxdb import DataFrameClient

class Trader(object):
	def __init__(self, config):
		self.exchange = RobinhoodExchange("", "", 1)

	def get_positions(self):
		try:
			self.owned = self.exchange.get_positions()
			self.owned_assets = {}
			for own in self.owned["results"]:
				print(own)
	 			asset = requests.get(own["instrument"]).json()["symbol"]
				amount = own["quantity"]
				price = own["average_buy_price"]
				self.owned_assets[asset] =  {"amount":amount, "price":price}
				time.sleep(5)
			print(self.owned_assets)
		except Exception as e:
			traceback.print_exc()

	def refresh_positions(self):
		try:
			for own in self.exchange.get_owned_securities():
				self.owned_assets[own]["current"] = self.exchange.get_quote(own)
				client = DataFrameClient("influx", 8086, "root", "root", "stock")
				client.create_database("stock")
				df = pd.DataFrame(data=list(self.owned_assets[own]["current"]["last_trade_price"]),
	                      index=pd.date_range(start=datetime.now().strftime("%Y-%m-%d"), periods=1, freq='D'))
				print(str(df))
				client.write_points(df, own)
				time.sleep(5)
		except Exception as e:
			traceback.print_exc()
