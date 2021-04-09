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

url = "wss://gateway.discord.gg/?v=6&encoding=json"

class ctx:
    running = True
    bot = discord.get_current_user()
    requests = requests.Session()
    commands = {}
    events = {}
    default = []
    guilds = {}
    ws = None
    bot_start = datetime.now()
    connection_start = datetime
    ping = {}

class Bot:
    def __init__(self, prefix):
        ws = websocket.WebSocketApp(url, on_message=self.on_message, on_close=self.on_close)
        self.ws = ws
        self.prefix = prefix
        self.token = None
        ctx.ws = ws
        ctx.connection_start = datetime.now()

    def register_modules(self, modules: list, _gateway, _discord):
        for module in modules:
            __import__(module).load(_gateway, _discord)

    def register_module(self, module, _gateway, _discord):
        _module = __import__(module)
        importlib.reload(_module)
        _module.load(_gateway, _discord)

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

    def heartbeat(self):
        while True:
            time.sleep(41250 / 1000)

            data = {
                "op": 1,
                "d": 251
            }

            data = json.dumps(data)
            self.ws.send(data)

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
                    "intents": 32511,
                    "properties": {
                        "$os": "linux",
                        "$browser": "cenzuralib",
                        "$device": "cenzuralib"
                    }
                }
            }

            data = json.dumps(data)
            self.ws.send(data)

            threading.Thread(target=self.heartbeat).start()
            
            if "ready" in ctx.events:
                ctx.data = {"ws": self.ws}
                ctx.events["ready"](ctx)
                
        elif msg["op"] == 11:
            now = datetime.now()
            channels = []
            for channel in ctx.ping:
                x = discord.create_message(channel, {"content": "obliczanie..."}).json()
                gateway_ping = now - ctx.ping[channel]["datetime"]
                gateway_ping = int(gateway_ping.total_seconds() * 1000)
                x_timestamp = ((int(x["id"]) >> 22) + 1420070400000) / 1000
                x_timestamp = datetime.fromtimestamp(x_timestamp)
                i_timestamp = ((int(ctx.ping[channel]["ctx"]["id"]) >> 22) + 1420070400000) / 1000
                i_timestamp = datetime.fromtimestamp(i_timestamp)
                bot_ping = int((x_timestamp - i_timestamp).total_seconds() * 1000)
                ctx.ping[channel]["data"]["content"] = ctx.ping[channel]["data"]["content"].format(bot_ping, gateway_ping)
                discord.edit_message(channel, x["id"], ctx.ping[channel]["data"])
                channels.append(channel)

            for channel in channels:    
                del ctx.ping[channel]

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
        time.sleep(10)
        ctx.guilds = []
        self.ws = websocket.WebSocketApp(url, on_message=self.on_message, on_close=self.on_close)
        ctx.ws = self.ws
        ctx.connection_start = datetime.now()
        self.ws.run_forever()

    def run(self, token):
        self.token = token
        self.ws.run_forever()