from flask import Flask, escape, request
import json
from threading import Thread
import requests
from datetime import datetime
import sys
import socket
from spannungsteiler.util import broker_util
from spannungsteiler.app import SpannungsteilerApp
from spannungsteiler.user import User, USERS


def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("9.9.9.9", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip

def subscribe_to_topics():
    topics = [ "spannungsteiler_demand_publish",
               "spannungsteiler_fill_level_publish",
               "spannungsteiler_offer_publish" ]


    for topic in topics:
        broker_util.send("subscribe", {
            "sender": "spannungsteiler",
            "address": "http://{}:5000/spannungsteiler".format(get_local_ip()),
            "interestedIn": topic
        })

def start_server(ui_app):
    app = Flask(__name__)
    @app.route('/spannungsteiler', methods=["POST"])
    def endpoint():
        if request.json["event"]["sender"] != "spannungsteiler":
            ui_app.update(request.json)
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

    t = Thread(target=app.run, kwargs={"host": "0.0.0.0"});
    t.daemon = True
    t.start()

if __name__ == '__main__':
    user = USERS[int(sys.argv[1])]
    ui_app = SpannungsteilerApp(user)
    start_server(ui_app)

    subscribe_to_topics()

    ui_app.run()
