class User():
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.color = "black"
        self.lights = []

    def update_color(self, color):
        self.color = color
        for light in self.lights:
            light["color"] = color
