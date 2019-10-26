from kivy.clock import Clock
from kivy_garden.graph import Graph, MeshLinePlot
from kivy.uix.widget import Widget
from math import sin, ceil
from datetime import datetime

SAMPLES = 4 * 24

def str_to_quarter_no(s):
    FMT = '%H:%M:%S'
    tdelta = (datetime.strptime(s, FMT) - datetime.strptime("00:00:00", FMT)).total_seconds()
    return ceil(tdelta / (60*16))

class LiveView(Widget):
    def __init__(self, **kwargs):
        super().__init__()
        self.graph = Graph(x_ticks_minor=4,
                           x_ticks_major=16,
                           y_grid_label=True,
                           x_grid_label=True,
                           padding=5,
                           x_grid=True,
                           y_grid=True,
                           xmin=-0,
                           xmax=SAMPLES,
                           ymin=0, **kwargs)
        self.plot = MeshLinePlot(color=[1, 1, 0, 1])
        self.plot.points = [(x,0) for x in range(0,SAMPLES+1)]
        self.graph.add_plot(self.plot)

        #self.register()

    def create_callback(self):
        self.i = 0

        def callback(dt):
            self.plot.points[self.i] = (self.i, (sin((self.i) / 10.) + 1)/2)
            self.i += 1
            if self.i >= SAMPLES:
                self.i -= SAMPLES

        return callback

    def update(self, json, type):
        payload = json["event"]["payload"]
        print(payload)
        date = str_to_quarter_no(payload["timestamp"])
        value = payload[type]
        self.plot.points[date] = (date, value)


    def register(self):
        # call my_callback every 0.5 seconds
        Clock.schedule_interval(self.create_callback(), 0.05)
