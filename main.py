from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from liveview import LiveView
from flask import Flask, escape, request
from threading import Thread

class SpannungsteilerApp(App):
    def build(self):
        full = GridLayout(rows=2, row_default_height=10, row_force_default=False)
        full.add_widget(Label(text='Overview', height=1))

        layout = GridLayout(cols=2, row_force_default=True, row_default_height=300, height=1000)

        self.liveview = LiveView()
        self.liveview.register()


        layout.add_widget(self.liveview.graph)

        full.add_widget(layout)

        return full

    def update(self, json):
        self.liveview.update(json)

if __name__ == '__main__':
    app = Flask(__name__)
    ui_app = SpannungsteilerApp()

    @app.route('/spannungsteiler', methods=["POST"])
    def endpoint():
        ui_app.update(request.json)
        return ""

    t = Thread(target=app.run);
    t.start()
    ui_app.run()
