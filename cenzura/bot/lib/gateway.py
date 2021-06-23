import websocket
import json
import threading
import time
from . import discord
import functions
import json
import copy
import handler
from datetime import datetime
import traceback
import importlib
import requests
from . import intents

url = "wss://gateway.discord.gg/?v=9&encoding=json"

class ctx:
    bot = discord.get_current_user()
    requests = requests.Session()
    data: dict = {}
    commands: dict = {}
    events: dict = {}
    default: list = []
    guilds: dict = {}
    ws: websocket.WebSocketApp = None
    bot_start = datetime.now()
    connection_start = datetime
    send = lambda *args, **kwargs: discord.send(ctx.data["channel_id"], *args, **kwargs)

class Bot:
    def __init__(self, prefix, intents):
        ws = websocket.WebSocketApp(url, on_message=self.on_message, on_close=self.on_close)
        self.ws = ws
        self.prefix = prefix
        self.token = None
        self.intents: int = intents
        self._heartbeat: threading.Thread = None
        self.presence: dict = {}
        self.ready = False
        ctx.ws = ws
        ctx.connection_start = datetime.now()

    def register_modules(self, _discord, *modules):
        for module in modules:
            __import__(module).load(self, _discord)

    def register_module(self, module, _discord):
        _module = __import__(module)
        importlib.reload(_module)
        _module.load(self, _discord)

    def event(self, func):
        ctx.events[func.__name__] = func
        
    def command(self, **kwargs):
        def _command(func):
            while func.__name__[0] == "_":
                func.__name__ = func.__name__[1:]

            kwargs["function"] = func
            ctx.commands[func.__name__] = kwargs

            if kwargs["_default"]:
                ctx.default.append(func.__name__)

        return _command

    def set_presence(self, name, *, status_type: int = 0, status: str = "online"):
        self.presence = {
            "name": name,
            "status_type": status_type,
            "status": status
        }

        data = {
            "op": 3,
            "d": {
                "since": None,
                "activities": [
                    {
                        "name": name,
                        "type": status_type
                    }
                ],
                "status": status,
                "afk": False
            }
        }

        data = json.dumps(data)
        self.ws.send(data)

    def heartbeat(self):
        t = threading.currentThread()
        
        while True:
            time.sleep(41250 / 1000)
            if t.stop:
                break

            data = {
                "op": 1,
                "d": 251
            }

            data = json.dumps(data)
            try:
                self.ws.send(data)
            except:
                break

    def on_message(self, msg):
        msg = json.loads(msg)

        if msg["op"] == 10:
            data = {
                "op": 1,
                "d": 251
            }

            data = json.dumps(data)
            self.ws.send(data)

            data = {
                "op": 2,
                "d": {
                    "token": f"Bot {self.token}",
                    "intents": self.intents,
                    "properties": {
                        "$os": "linux",
                        "$browser": "cenzuralib",
                        "$device": "cenzuralib"
                    }
                }
            }

            data = json.dumps(data)
            self.ws.send(data)

            t = threading.Thread(target=self.heartbeat)
            t.start()
            self._heartbeat = t
            self._heartbeat.stop = False

            if self.presence:
                self.set_presence(**self.presence)
            
            if "ready" in ctx.events and not self.ready:
                ctx.data = {"ws": self.ws}
                ctx.events["ready"](ctx)
                self.ready = True

        if msg["t"] == "GUILD_CREATE":
            ctx.guilds[msg["d"]["id"]] = msg["d"]

        elif msg["t"] == "GUILD_DELETE":
            del ctx.guilds[msg["d"]["id"]]

        elif msg["t"] == "MESSAGE_CREATE":
            ctx.data = msg["d"]

            guild = ctx.data["guild_id"]
            guilds = functions.read_json("guilds")

            if guild in guilds and "prefix" in guilds[guild]:
                prefix = guilds[guild]["prefix"]
            else:
                prefix = self.prefix

            if msg["d"]["content"].startswith(prefix):
                if "bot" in msg["d"]["author"]:
                    return

                command = msg["d"]["content"].split(" ")[0][len(prefix):]

                while command[0] == "_":
                    command = command[1:]

                args = msg["d"]["content"].split(" ")[1:]
                
                ctx.command = command
                ctx.args = args
                ctx.token = self.token
                ctx.ws = self.ws

                if command in ctx.commands:
                    try:
                        ctx.commands[command]["function"](ctx)
                    except Exception:
                        handler.error_handler(ctx, "error", traceback.format_exc().splitlines()[-1])
                else:
                    handler.error_handler(ctx, "commandnotfound")
            else:
                ctx.args = msg["d"]["content"].split(" ")

        if msg["t"] in ctx.events:
            ctx.data = msg["d"]
            ctx.events[msg["t"]](ctx)

    def on_close(self):
        time.sleep(5)
        ctx.guilds = {}
        self.ws = websocket.WebSocketApp(url, on_message=self.on_message, on_close=self.on_close)
        self._heartbeat.stop = True
        self._heartbeat = None
        ctx.ws = self.ws
        ctx.connection_start = datetime.now()
        self.ws.run_forever()

    def run(self, token):
        self.token = token
        self.ws.run_forever()