from flask import Flask, escape, request
import threading, json, time
import broker_util

app = Flask(__name__)



if __name__ == "__main__":

    energy_requested = {}
    energy_provided = {}


    
    app = Flask(__name__)

    @app.route('/energy_bank', methods=["POST"])
    def endpoint()


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

            broker_util.send_transaction_execution("enerrgy_bank", answere, key)
            provided_sum -= answere


        
        

        

        time.sleep(0.2)




    print("App is running")