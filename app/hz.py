from time import sleep
import hazelcast
import logging
from consul import consul_client
from application import app
import sys


class Hz(object):


	def __init__(self)
		(index, services) = consul_client.services()

		wyre_ips = services[app.config["IP_SERVICE"]]

		config = hazelcast.ClientConfig()

		for ip in wyre_ips:
			config.network_config.addresses.append('{}:{}'.format(ip, 5701))
			config.network_config.addresses.append('{}:{}'.format(ip, 5702))

		self.hz = hazelcast.HazelcastClient(config)
		self.cluster = rc.clusterService(hz, config)
		self.member = rc.startMember(cluster.id)

		def member_added(event):
			print("member added", event)

		cluster.add_listener(member_added=member)


	def register_queue_listener(self, key, added, removed):
		self.hz.get_queue(key).add_listener(include_value=True, item_added_func=added, item_removed_func=removed)
 

	def send_queue(self, key, obj):
		self.hz.get_queue(key).add(obj)


	def remove_queue(self, key, obj):
		self.hz.get_queue(key).remove(obj)


	def take_queue(self, key):
		return hz.get_queue(key).take()


hz_cluster = Hz()