import json
import requests

types = {'publish', 'subscribe', 'unsubscribe', 'subscribed', 'request'}

def send(send_type, json_payload):

    url = 'http://194.94.239.125:9000/'
    if send_type in types:
        url += send_type
    else:
        raise Exception('Give a valid send type.')

    headers = {
    'Content-Type': "application/json",
    'cache-control': "no-cache",
    }

    response = requests.request("POST", url, data=json_payload, headers=headers)
    print(response)


def main():

    payload = {
    "type": "addFilterToInspectorService",
    "sender": "Spannungsteiler",
    "payload": {
        "keyword": "Gasverbrauch",
        }
}

    

    send("http://194.94.239.125:9000/request", payload)
   

if __name__ == "__main__":
    main()