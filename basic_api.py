import json
import requests


def send(url, payload):


    json_payload = json.dumps(payload)

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