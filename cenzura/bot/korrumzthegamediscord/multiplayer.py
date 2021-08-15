import websocket, json, random
from .objects import Player, Bug

url = "wss://ws.korrumzthegame.cf"

class PlayerMe:
    def __init__(self, update, username: str, x: int, y: int, pull_requests: int, image_number: int):
        self.ws = websocket.WebSocketApp(url, on_open=self.on_open, on_message=self.on_message)
        self.update = update

        self.username = username
        self.x = x
        self.y = y
        self.pull_requests = pull_requests
        self.image_number = image_number

        self.players = []
        self.bugs = []

    def __eq__(self, player: dict):
        return "username" in player and self.username == player["username"]

    def move(self, direction, _id, token):
        directions = {
            "up": (0, -75),
            "down": (0, 75),
            "left": (-75, 0),
            "right": (75, 0),
            "left up": (-75, -75),
            "right up": (75, -75),
            "left down": (-75, 75),
            "right down": (75, 75),
        }

        self.x += directions[direction][0]
        self.y += directions[direction][1]

        if self.x < 0 or self.x > 1920:
            self.x = random.randint(0, 1920)
        if self.y < 0 or self.y > 1080:
            self.y = random.randint(0, 1080)

        data = {
            "event": "move",
            "data": {
                "username": self.username,
                "x": round(self.x),
                "y": round(self.y)
            }
        }

        data = json.dumps(data)
        self.ws.send(data)

        self.update(_id, token)

    def on_open(self):
        data = {
            "event": "new player",
            "data": {
                "username": self.username,
                "x": round(self.x),
                "y": round(self.y),
                "canvasWidth": 5000,
                "canvasHeight": 5000,
                "imageNumber": self.image_number
            }
        }

        data = json.dumps(data)
        self.ws.send(data)

        self.update()

    def on_message(self, msg):
        msg = json.loads(msg)
        event = msg["event"]
        data = msg["data"]
        p = None

        for player in self.players + [self]:
            if player == data:
                p = player

        if event == "new player":
            self.players.append(Player(**data))

        elif event == "new username":
            self.username = data["username"]

        elif event == "new image":
            self.image_number = data["imageNumber"]

        elif event == "move":
            if not p == self:
                p.x = data["x"]
                p.y = data["y"]

        elif event == "new bug":
            self.bugs.append(Bug(**data))

        elif event == "pull request":
            b = None

            for bug in self.bugs:
                if (bug.x, bug.y, bug.image_number) == (data["bug"]["x"], data["bug"]["y"], data["bug"]["imageNumber"]):
                    b = bug

            self.bugs.remove(b)
            p.pull_requests = data["pullRequests"]

            if self.username == data["username"]:
                self.update()

        elif event == "player disconnected":
            self.players.remove(p)

    def run(self):
        self.ws.run_forever()