from Robinhood.Robinhood import Robinhood

class RobinhoodExchange(object):	
	def __init__(self, user, passw, page_depth):
		self.robin = Robinhood()
		self.robin.login(username=user, password=passw)
		self.page_depth = page_depth

	def get_orders(self):
		return self.robin.order_history()

	def place_order(self, instrument, ACTION, price, amount):
		if ACTION == "buy":
			return self.robin.place_buy_order(instrument, amount, price)
		elif ACTION == "sell":
			return self.robin.place_sell_order(instrument, amount, price)

	def get_instrument(self, id):
		return self.robin.instruments(stock=id)

	def get_instruments(self):
		return self.robin.instruments()

	def get_owned_securities(self, id):
		return self.robin.securities_owned()

	def get_positions(self):
		return self.robin.positions()


	def get_quote(self, instrument):
		return quote_data(instrument)
