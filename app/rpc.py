from hz import hz_cluster


class RPC(object):

	def __init__(self):
		self.lookup = {}

	def register_rpc(self, requestClass, func):
		hz_cluster.register_queue_listener(requestClass, func, None)
		self.lookup[requestClass] = func

	def request_rpc(self, key, request):
		hz_cluster.send_queue(key, request)


