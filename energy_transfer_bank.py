from flask import Flask, escape, request
import threading, json, time
from spannungsteiler.util import broker_util
import socket

app = Flask(__name__)
energy_requested = {}
energy_provided = {}


def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("9.9.9.9", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip

def subscribe_to_topics():
    broker_util.send("subscribe", {
        "sender": "energy_bank",
        "address": "http://{}:5000/energy_bank".format(get_local_ip()),
        "interestedIn": ""
    })

def start_server():
    app = Flask(__name__)

    @app.route('/energy_bank', methods=["POST"])
    def endpoint():

        payload = request.json
        amount = payload["payload"]["amount"]
        sender_id = payload["id"]

        if amount < 0:
            energy_requested[sender_id] = amount
        elif amount > 0:
            energy_provided[sender_id] = amount

        return json.dumps({'success':True}), 200, {'ContentType':'application/json'}


        t = threading.Thread(target=app.run, kwargs={"host": "0.0.0.0"})
        t.daemon = False
        t.start()


if __name__ == "__main__":


    subscribe_to_topics()
    start_server()

    while True:

        provided_sum = 0
        requested_sum = 0

        for key in energy_provided.keys():
            provided_sum += energy_provided.get(key)

        for key in energy_requested.keys():
            requested_sum += energy_requested.get(key)

        for key in energy_provided.keys():
            amount = energy_provided.get(key)
            answere = 0

            if amount <= abs(requested_sum):
                answere -= amount

            else:
                answere = requested_sum

            broker_util.send_transaction_execution("energy_bank", answere, key)
            requested_sum -= answere


        for key in energy_requested.keys():
            amount = energy_requested.get(key)
            answere = 0

            if abs(amount) <= provided_sum:
                answere -= amount

            else:
                answere = provided_sum

            broker_util.send_transaction_execution("energy_bank", answere, key)
            provided_sum -= answere      
        

        time.sleep(0.3)

