import consul
from application import app

consul_client = Consul(host=app.config.["CONSUL"])

