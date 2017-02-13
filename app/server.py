import json, inspect, traceback, time, sys
from flask import render_template, request, redirect, make_response
from celery import Celery
import logging


from database import db
from application import *
import models
from models import *
from functools import wraps


# Views  ======================================================================
@app.route('/status')
def home():
    return make_response(json.dumps({"status":"ok"}),200)


@celery.task(bind=True)
def long_task(self):
    sys.stderr.write("starting long-running task")
    while(True):
        try:
        except Exception as e:
            traceback.print_exc()
        time.sleep(1)


@app.before_first_request
def bootstrap_app():
    db.init_app(app)
    long_task.delay()
    return


@app.teardown_request
def teardown(self):
    try:
        db.session.commit()
        db.session.remove()
    except Exception as e:
        traceback.print_exc()


def wrap_teardown_func(teardown_func):
    @wraps(teardown_func)
    def log_teardown_error(*args, **kwargs):
        try:
            teardown_func(*args, **kwargs)
        except Exception as exc:
            app.logger.exception(exc)
    return log_teardown_error


def main(app):
    if app.teardown_request_funcs:
        for bp, func_list in app.teardown_request_funcs.items():
            for i, func in enumerate(func_list):
                app.teardown_request_funcs[bp][i] = wrap_teardown_func(func)
    if app.teardown_appcontext_funcs:
        for i, func in enumerate(app.teardown_appcontext_funcs):
            app.teardown_appcontext_funcs[i] = wrap_teardown_func(func)

    try:
        db.init_app(app)
        with app.app_context():
            db.create_all()
    except Exception as e:
        print(e)
    try:
        app.run()
    except Exception as e:
        traceback.print_exc()

    # Start server  ===============================================================
if __name__ == '__main__':
    main(app)


