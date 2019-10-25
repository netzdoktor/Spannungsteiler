from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from math import sin
from kivy_garden.graph import Graph, MeshLinePlot
from kivy.uix.button import Button

class SpannungsteilerApp(App):
    def build(self):
        layout = GridLayout(cols=2, row_force_default=True, row_default_height=300)

        graph = Graph(xlabel='X', ylabel='Y', x_ticks_minor=5,
        x_ticks_major=25, y_ticks_major=1,
        y_grid_label=True, x_grid_label=True, padding=5,
        x_grid=True, y_grid=True, xmin=-0, xmax=100, ymin=-1, ymax=1)
        plot = MeshLinePlot(color=[1, 0, 0, 1])
        plot.points = [(x, sin(x / 10.)) for x in range(0, 101)]
        graph.add_plot(plot)


        layout.add_widget(Button(text='Hello 1', size_hint_x=None, width=100))
        layout.add_widget(Button(text='World 1'))
        layout.add_widget(Button(text='Hello 2', size_hint_x=None, width=100))
        layout.add_widget(graph)
        return layout



        return HomeScreen()


if __name__ == '__main__':
    SpannungsteilerApp().run()
