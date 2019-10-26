from math import ceil
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from datetime import datetime
from .household import Household
from .ui.liveview import LiveView
from .util.color_util import UserLightStatus


def str_to_quarter_no(s):
    FMT = '%H:%M:%S'
    tdelta = (datetime.strptime(s, FMT) - datetime.strptime("00:00:00", FMT)).total_seconds()
    return ceil(tdelta / (60*16))


class SpannungsteilerApp(App):
    def __init__(self, user):
        self.user = user
        self.household = Household(user)
        super().__init__()

    def build_graphs(self):
        layout = GridLayout(cols=1, row_force_default=True, row_default_height=150, size_hint_y=1)
        self.liveview_offer = LiveView(xlabel='Time', ylabel='Offer [W]', ymax=3000,y_ticks_major=1000,)
        self.liveview_demand = LiveView(xlabel='Time', ylabel='Demand [W]', ymax=3000,y_ticks_major=1000,)
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
        cb = self.household.round_callback()
        def callback(dt):
            cb(dt)
            self.liveview_demand.update(self.user.id, self.household._current_time, self.household.demand)
            self.liveview_offer.update(self.user.id, self.household._current_time, self.household.offer)
            self.liveview_battery.update(self.user.id, self.household._current_time, self.household.buffer*100)

        Clock.schedule_interval(callback, 0.06)

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
        sender = json["event"]["sender"]
        if(sender == self.user.id):
            return
        if self.household.balance < 0.0:
            color = "red"
        else:
            color = "green"


        self.user_status_lights.update_user(0, color)
        payload = json["event"]["payload"]
        date = payload["timestamp"]
        if json["event"]["type"] == "spannungsteiler_demand_publish":
            self.liveview_demand.update(sender, date, payload["demand"])
        elif json["event"]["type"] == "spannungsteiler_fill_level_publish":
            self.liveview_battery.update(sender, date, payload["fill_level"])
        elif json["event"]["type"] == "spannungsteiler_offer_publish":
            self.liveview_offer.update(sender, date, payload["offer"])
        else:
            pass
