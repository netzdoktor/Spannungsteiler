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
            # if a user wants to provide energy, he will subtract from his energy pool, hence expects a negative return value
            energy_provided[sender_id] = -amount        

        return json.dumps({'success':True}), 200, {'ContentType':'application/json'}




    t = threading.Thread(target=app.run, kwargs={"host": "0.0.0.0"})
    t.daemon = False
    t.start()


    while True:

        provided_sum = 0
        requested_sum = 0

        #calculate total energy provided
        for key in energy_provided.keys():
            provided_sum += energy_provided.get(key)

        #calculate total energy requested
        for key in energy_requested.keys():
            requested_sum += energy_requested.get(key)

        
        for key in energy_provided.keys():
            amount = energy_provided.get(key)       #negative amount
            answer = 0

            if abs(amount) >= abs(requested_sum):   #both values are negative
                answer = amount

            else:
                answer = requested_sum              # if amount is smaller than the remaining sum, send the remainder instead

            broker_util.send_transaction_execution("energy_bank", answer, key) #sends a negative answer
            requested_sum -= answer


            

        for key in energy_requested.keys():
            amount = energy_requested.get(key)      #positive amount
            answer = 0

            if amount >= provided_sum:
                answer = amount

            else:
                answer = provided_sum               # if amount is smaller than the remaining sum, send the remainder instead

            broker_util.send_transaction_execution("enerrgy_bank", answer, key)
            provided_sum -= answer


        
        

        

        time.sleep(0.2)




    print("App is running")