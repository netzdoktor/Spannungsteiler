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

def subscribe_to_topics(port=5000):
    topics = [ "spannungsteiler_demand_publish",
               "spannungsteiler_fill_level_publish",
               "spannungsteiler_offer_publish" ]


    for topic in topics:
        broker_util.send("subscribe", {
            "sender": "spannungsteiler",
            "address": "http://{}:{}/spannungsteiler".format(get_local_ip(), port),
            "interestedIn": topic
        })

def start_server(ui_app, port):
    app = Flask(__name__)
    @app.route('/spannungsteiler', methods=["POST"])
    def endpoint():
        if request.json["event"]["sender"] != "spannungsteiler":
            ui_app.update(request.json)
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

    t = Thread(target=app.run, kwargs={"host": "0.0.0.0", "port": port});
    t.daemon = True
    t.start()

if __name__ == '__main__':
    user = USERS[int(sys.argv[1])]
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 5000
    ui_app = SpannungsteilerApp(user)
    start_server(ui_app, port)

    subscribe_to_topics(port)

    ui_app.run()
