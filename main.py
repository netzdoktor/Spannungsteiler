from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from liveview import LiveView


class SpannungsteilerApp(App):
    def build(self):
        full = GridLayout(rows=2, row_default_height=10, row_force_default=False)
        full.add_widget(Label(text='Overview', height=1))

        layout = GridLayout(cols=2, row_force_default=True, row_default_height=300, height=1000)

        liveview = LiveView()
        liveview.register()


        layout.add_widget(liveview.graph)


        full.add_widget(layout)



        return full

if __name__ == '__main__':
    SpannungsteilerApp().run()
