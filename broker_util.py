import json
import requests

types = {'publish', 'subscribe', 'unsubscribe', 'subscribed', 'request'}


def send(send_type, payload):
    url = 'http://194.94.239.125:9000/'
    if send_type in types:
        url += send_type
    else:
        raise Exception('Give a valid send type.')

    json_payload = json.dumps(payload)

    headers = {
    'Content-Type': "application/json",
    'cache-control': "no-cache",
    }

    response = requests.request("POST", url, data=json_payload, headers=headers)
    return response


def send_demand(sender, timestamp, value):

    payload={
        "type": "spannungsteiler_demand_publish",
        "sender": sender,
        "payload": {
            "timestamp": timestamp,
            "demand": value
        }
    }

    send("publish", payload)

def send_fill_level(sender, timestamp, value):
    payload={
        "type": "spannungsteiler_fill_level_publish",
        "sender": sender,
        "payload": {
            "timestamp": timestamp,
            "fill_level": value
        }

    }

    send("publish", payload)


def send_offer(sender, timestamp, value):
    payload={
        "type": "spannungsteiler_offer_publish",
        "sender": sender,
        "payload": {
            "timestamp": timestamp,
            "offer": value,
        }
    }

    send("publish", payload)


def send_transaction_submit(sender, amount):
    payload={
        "type": "spannungsteiler_transaction_execution",
        "sender": sender,
        "payload": {
            "amount": amount
        }
    }

    send("publish", payload)


def send_transaction_execution(sender, amount, previous_id):
    payload={
        "type": "spannungsteiler_transaction_execution",
        "sender": sender,
        "payload": {
            "amount": amount
        },
        "causedBy": previous_id
    }

    send("publish", payload)
