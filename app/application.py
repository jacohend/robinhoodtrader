import logging, os
from flask import Flask
from celery import Celery
from redlock import Redlock

def make_celery(app):
	celery = Celery(app.import_name, backend=app.config['CELERY_RESULT_BACKEND'],
					broker=app.config['CELERY_BROKER_URL'])
	celery.conf.update(app.config)
	TaskBase = celery.Task
	class ContextTask(TaskBase):
		abstract = True
		def __call__(self, *args, **kwargs):
			with app.app_context():
				return TaskBase.__call__(self, *args, **kwargs)
	celery.Task = ContextTask
	return celery

logger = logging.getLogger('python')
logger.setLevel(logging.WARNING)
app = Flask(__name__)
app.config.from_object('config.{}Config'.format(os.environ.get('SERVER_ENV', 'Development')))
app.config['SQLALCHEMY_DATABASE_URI'] = app.config['SQLALCHEMY_DATABASE_URI'].format(
	os.environ.get('DB_USER'),
	os.environ.get('DB_PASS'),
	os.environ.get('DB_HOST'),
	os.environ.get('DB_NAME')
	)
app.config['APP_NAME'] = app.config['APP_NAME'].format("PyCore")
app.config['SECRET_KEY'] = app.config['SECRET_KEY'].format(os.environ.get('SECRET_KEY', 'SECRET'))
app.config['SECURITY_PASSWORD_SALT'] = app.config['SECURITY_PASSWORD_SALT'].format(os.environ.get('SECURITY_PASSWORD_SALT'))
app.config['CELERY_BROKER_URL'] =  'redis://redis:6379/0'
app.config['CELERY_RESULT_BACKEND'] = "db+{}".format(app.config['SQLALCHEMY_DATABASE_URI'])
celery = make_celery(app)
redlock = Redlock([{"host": app.config.REDIS}])