from kivy.clock import Clock
from kivy_garden.graph import Graph, MeshLinePlot
from kivy.uix.widget import Widget
from math import sin

class LiveView(Widget):
    def create_callback(self):
        self.i = 0
        self.plot = MeshLinePlot(color=[1, 0, 0, 1])
        self.plot.points = [(x,0) for x in range(0,101)]
        self.graph.add_plot(self.plot)

        def callback(dt):
            self.plot.points[self.i] = (self.i, sin((self.i) / 10.))
            self.i += 1
            if self.i > 100:
                self.i = 0

        return callback

    def register(self):
        # call my_callback every 0.5 seconds
        Clock.schedule_interval(self.create_callback(), 0.05)

    graph = Graph(xlabel='X', ylabel='Y', x_ticks_minor=5,
    x_ticks_major=25, y_ticks_major=1,
    y_grid_label=True, x_grid_label=True, padding=5,
    x_grid=True, y_grid=True, xmin=-0, xmax=100, ymin=-1, ymax=1)
