#!/usr/bin/env python3
""" PIYOT - otp handler """
from os import environ as env
from prometheus_client import multiprocess, generate_latest, Summary, CollectorRegistry
from flask import Flask, request, make_response, send_file, jsonify
from flask_sqlalchemy import SQLAlchemy
import pyotp
from models import piyot as piyot_model

application = Flask(__name__, template_folder="templates")
application.config["SQLALCHEMY_DATABASE_URI"] = env.get("PIYOT_DB_URI", "sqlite:///application.db")
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(application)

REQUEST_TIME = Summary("piyot_request_processing_time", "Time spent processing request")

def child_exit(server, worker):
    """ multiprocess function for prometheus to track gunicorn """
    return multiprocess.mark_process_dead(worker.pid)

@application.route("/healthz", methods=["GET"])
def default_healthz():
    """ healthcheck route """
    return make_response("", 200)

@application.route("/metrics", methods=["GET"])
def metrics():
    """  metrics route """
    registry = CollectorRegistry()
    multiprocess.MultiProcessCollector(registry)
    return generate_latest(registry)

def validate_otp(user, otp):
    """ validate one time password """
    obj = pyotp.TOTP(user.secret_otp)
    return obj.verify(otp)

def get_user(user_name):
    """ query db for user secret key """
    user = piyot_model.query.filter(piyot_model.user_name == user_name).first()
    return user

def json_resp(result):
    """ prepare response """
    return (
        jsonify(result),
        200,
        {"Content-Type": "application/json; Charset=UTF-8", "Server": "Snooki"}
    )

@application.route("/<path:path>", methods=["GET", "PUT"])
@application.route("/<path:path>")
@REQUEST_TIME.time()
def req_handler(path):
    """ request handler function """
    try:
        if request.method == "GET":
            user_name = request.args.get("username")
            one_time_code = request.args.get("otp")
            return_type = request.args.get("type")
            user = get_user(user_name)
            if user and one_time_code:
                return make_response(json_resp(validate_otp(user, one_time_code)))
            if user and return_type == 'image':
                return send_file(user.get_qr_code(), mimetype='image/png')
            if user is not None:
                return make_response(json_resp(user))
            return make_response('403 Forbidden', 403)
        return make_response('405 Method Not Allowed', 405)
    except (AttributeError, ValueError, IOError, RuntimeError, SyntaxError) as exp:
        print("Error in req_handler() " + str(exp))
        return make_response('400 Bad Request', 400)

if __name__ == "__main__":
    application.run(debug=False,threaded=False)
    db.init_app(application)
