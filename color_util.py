import broker_util

class User():
    def __init__(self, name):
        self.name = name
        self.color = "black"

class UserLightStatus():
    def __init__(self):
        self.users = [User("1"), User("2"), User("3")]

    def update_user(self, id, color):
        res = broker_util.send("publish", {
            "type": "lightcontrol",
            "sender": "foo",
            "payload": {
                "lights": [
                    {
                        "id": x,
                        "color": self.users[0].color
                    } for x in range(21)
                ] + [
                    {
                        "id": x,
                        "color":self.users[1].color
                    } for x in range(20,41)
                ] + [
                    {
                        "id": x,
                        "color": self.users[2].color
                    } for x in range(40,61)
                ]
            }
        })
        print(res)
