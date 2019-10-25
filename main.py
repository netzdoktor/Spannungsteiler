from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from liveview import LiveView
from flask import Flask, escape, request
import json
from threading import Thread
import broker_util
import requests

class SpannungsteilerApp(App):
    def build(self):
        full = GridLayout(rows=3, row_default_height=30, row_force_default=False)
        full.add_widget(Label(text='Overview', size_hint_y=None, height=20))

        layout = GridLayout(cols=1, row_force_default=True, row_default_height=150, size_hint_y=1)

        self.liveview1 = LiveView(xlabel='Time', ylabel='Supply [W]', ymax=3)
        self.liveview2 = LiveView(xlabel='Time', ylabel='Demand [W]', ymax=2)
        self.liveview3 = LiveView(xlabel='Time', ylabel='Fill [%]', ymax=1)

        layout.add_widget(self.liveview1.graph)
        layout.add_widget(self.liveview2.graph)
        layout.add_widget(self.liveview3.graph)


        full.add_widget(layout)

        actions = GridLayout(cols=3, size_hint_y=None, height=50)
        actions.add_widget(Button(text="Sell"))
        actions.add_widget(Button(text="Buy"))
        actions.add_widget(Button(text="Donate"))
        full.add_widget(actions)

        return full

    def update(self, json):
        self.liveview1.update(json)

if __name__ == '__main__':
    app = Flask(__name__)
    ui_app = SpannungsteilerApp()

    @app.route('/spannungsteiler', methods=["POST"])
    def endpoint():
        ui_app.update(request.json)
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

    t = Thread(target=app.run, kwargs={"host": "0.0.0.0"});
    t.daemon = True
    t.start()

    broker_util.send("subscribe", {
        "sender": "spannungsteiler",
        "address": "http://194.94.239.78:5000/spannungsteiler",
        "interestedIn": "lightcontrol"
    })
    ui_app.run()
