import broker_util
import math
import itertools
from user import User

class UserLightStatus():
    def __init__(self):
        self.users = [
            User("30aa4c7f-faa4-4941-968f-3b024a5f1efe", "spannungsteiler"),
            User("9c55ac05-e4b5-47e5-8596-9ac7346e84ff", "stromteiler")
        ]
        self.lights_count = 60
        lights_per_user = math.ceil(self.lights_count / len(self.users))
        for i, user in enumerate(self.users):
            user.lights = [{
                "id":  + x,
                "color": user.color
            } for x in range(i * lights_per_user, (i+1) * lights_per_user)]

        self.update_lights()


    def update_user(self, id, color):
        self.users[id].update_color(color)
        self.update_lights()

    def update_lights(self):
        lights = list(itertools.chain([x.lights for x in self.users]))
        res = broker_util.send("publish", {
            "type": "lightcontrol",
            "sender": "spannungsteiler",
            "payload": {
                "lights": lights
            }
        })
        print(res)
