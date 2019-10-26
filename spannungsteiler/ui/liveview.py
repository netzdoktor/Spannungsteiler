import collections
from math import sin, ceil
from kivy.clock import Clock
from kivy_garden.graph import Graph, MeshLinePlot
from kivy.uix.widget import Widget

SAMPLES = 4 * 24

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
        self.total_plot = MeshLinePlot(color=[0, 1, 1, 1])
        self.total_plot.points = [(x,0) for x in range(0,SAMPLES+1)]
        self.graph.add_plot(self.total_plot)

        self.values = collections.defaultdict(lambda: [0 for x in range(0,SAMPLES+1)])

    def update(self, sender, date, value):
        self.values[sender][date] = value
        total = [self.values[sender][date] for sender in self.values.keys()]

        self.plot.points[date] = (date, value)
        self.total_plot.points[date] = (date, sum(total))
