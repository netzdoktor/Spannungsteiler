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
from color_util import UserLightStatus

class SpannungsteilerApp(App):
    def build_graphs(self):
        layout = GridLayout(cols=1, row_force_default=True, row_default_height=150, size_hint_y=1)
        self.liveview1 = LiveView(xlabel='Time', ylabel='Supply [W]', ymax=3,y_ticks_major=1,)
        self.liveview_demand = LiveView(xlabel='Time', ylabel='Demand [W]', ymax=1050,y_ticks_major=500,)
        self.liveview3 = LiveView(xlabel='Time', ylabel='Fill [%]', ymax=1,y_ticks_major=1,)

        layout.add_widget(self.liveview1.graph)
        layout.add_widget(self.liveview_demand.graph)
        layout.add_widget(self.liveview3.graph)
        return layout

    def build_actions(self):
        actions = GridLayout(cols=3, size_hint_y=None, height=50)
        sell_button = Button(text="Sell")
        sell_button.bind(on_press=self.click())
        actions.add_widget(sell_button)
        buy_button = Button(text="Buy")
        buy_button.bind(on_press=self.click())
        actions.add_widget(buy_button)
        donate_button = Button(text="Donate")
        donate_button.bind(on_press=self.click())
        actions.add_widget(donate_button)
        return actions

    def build(self):
        self.demand = 0
        self.supply = 0
        self.fill = 0
        self.user_status_lights = UserLightStatus()

        layout = GridLayout(rows=3, row_default_height=30, row_force_default=False)
        layout.add_widget(Label(text='Overview', size_hint_y=None, height=20))
        layout.add_widget(self.build_graphs())
        layout.add_widget(self.build_actions())
        return layout

    def click(self):
        def callback(instance):
            print("click")
        return callback

    def update(self, json):
        if self.demand > self.supply:
            color = "red"
        else:
            color = "green"

        self.user_status_lights.update_user(0, color)
        if json["event"]["type"] == "spannungsteiler_demand_publish":
            self.liveview_demand.update(json)
        else:
            pass

if __name__ == '__main__':
    app = Flask(__name__)
    ui_app = SpannungsteilerApp()

    @app.route('/spannungsteiler', methods=["POST"])
    def endpoint():
        if request.json["event"]["sender"] != "spannungsteiler":
            ui_app.update(request.json)
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

    t = Thread(target=app.run, kwargs={"host": "0.0.0.0"});
    t.daemon = True
    t.start()

    broker_util.send("subscribe", {
        "sender": "spannungsteiler",
        "address": "http://194.94.239.78:5000/spannungsteiler",
        "interestedIn": "spannungsteiler_demand_publish"
    })
    ui_app.run()
