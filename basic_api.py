import broker_util

def main():

    payload = {
    "type": "addFilterToInspectorService",
    "sender": "Spannungsteiler",
    "payload": {
        "keyword": "Gasverbrauch",
        }
    }
    print(broker_util.send("request", payload))


if __name__ == "__main__":
    main()
