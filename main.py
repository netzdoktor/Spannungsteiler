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
from math import ceil
from datetime import datetime


def str_to_quarter_no(s):
    FMT = '%H:%M:%S'
    tdelta = (datetime.strptime(s, FMT) - datetime.strptime("00:00:00", FMT)).total_seconds()
    return ceil(tdelta / (60*16))


class SpannungsteilerApp(App):
    def build_graphs(self):
        layout = GridLayout(cols=1, row_force_default=True, row_default_height=150, size_hint_y=1)
        self.liveview_offer = LiveView(xlabel='Time', ylabel='Offer [W]', ymax=1750,y_ticks_major=500,)
        self.liveview_demand = LiveView(xlabel='Time', ylabel='Demand [W]', ymax=1050,y_ticks_major=500,)
        self.liveview_battery = LiveView(xlabel='Time', ylabel='Fill [%]', ymax=100,y_ticks_major=25)

        layout.add_widget(self.liveview_offer.graph)
        layout.add_widget(self.liveview_demand.graph)
        layout.add_widget(self.liveview_battery.graph)
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
        payload = json["event"]["payload"]
        date = str_to_quarter_no(payload["timestamp"])
        if json["event"]["type"] == "spannungsteiler_demand_publish":
            self.liveview_demand.update(date, payload["demand"])
        elif json["event"]["type"] == "spannungsteiler_fill_level_publish":
            self.liveview_battery.update(date, payload["fill_level"])
        elif json["event"]["type"] == "spannungsteiler_offer_publish":
            self.liveview_offer.update(date, payload["offer"])
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

    for topic in [ "spannungsteiler_demand_publish",
        "spannungsteiler_fill_level_publish",
        "spannungsteiler_offer_publish"]:
        broker_util.send("subscribe", {
            "sender": "spannungsteiler",
            "address": "http://194.94.239.78:5000/spannungsteiler",
            "interestedIn": topic
        })
    ui_app.run()
