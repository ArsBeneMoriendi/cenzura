import websocket
import json
import threading
import time
import functions
import json
import copy
from datetime import datetime
from . import intents
from .errors import *
from .types import *
from inspect import signature, _empty
from .ctx import ctx
from .discord import get_current_user, send

ctx.bot_user = User(get_current_user())

url = "wss://gateway.discord.gg/?v=9&encoding=json"

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

    def __repr__(self) -> str:
        return "zajebisty bot!!1!"

    def __str__(self) -> str:
        return "zajebisty bot!!1!"

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

        if msg["t"] in ctx.events:
            ctx.data = msg["d"]
            if "author" in ctx.data:
                ctx.data["author"]["member"] = ctx.data["member"]
                ctx.author = Member(ctx.data["author"])
            if "member" in ctx.data:
                if "user" in ctx.data["member"]:
                    member = ctx.data["member"]["user"]
                    member["member"] = ctx.data["member"]
                    del member["member"]["user"]
                    ctx.member = Member(member)
            if "user" in ctx.data:
                ctx.user = User(ctx.data["user"])
            if "guild_id" in ctx.data:
                ctx.guild = ctx.guilds[ctx.data["guild_id"]]
            if "channel_id" in ctx.data:
                ctx.channel = ctx.guild.channels[ctx.data["channel_id"]]
                ctx.send = ctx.channel.send
            if "role_id" in ctx.data:
                ctx.role = Role(ctx.data["role_id"])
            if "mentions" in ctx.data:
                ctx.mentions = [Member(member) for member in ctx.data["mentions"]]
            try:
                ctx.events[msg["t"]](ctx.modules["Events"], ctx)
            except:
                pass

        if msg["t"] in ("GUILD_CREATE", "GUILD_UPDATE"):
            channels = {}
            roles = {}
            for channel in msg["d"]["channels"]:
                channels[channel["id"]] = Channel(channel)
            for role in msg["d"]["roles"]:
                roles[role["id"]] = Role(role)
            msg["d"]["channels"] = channels
            msg["d"]["roles"] = roles
            ctx.guilds[msg["d"]["id"]] = Guild(msg["d"])

        elif msg["t"] == "GUILD_DELETE":
            del ctx.guilds[msg["d"]["id"]]

        elif msg["t"] in ("CHANNEL_CREATE", "CHANNEL_UPDATE"):
            ctx.guilds[msg["d"]["guild_id"]]._guild["channels"][msg["d"]["id"]] = Channel(msg["d"])

        elif msg["t"] == "CHANNEL_DELETE":
            del ctx.guilds[msg["d"]["guild_id"]]._guild["channels"][msg["d"]["id"]]

        elif msg["t"] in ("GUILD_ROLE_CREATE", "GUILD_ROLE_UPDATE"):
            ctx.guilds[msg["d"]["guild_id"]]._guild["roles"][msg["d"]["role"]["id"]] = Role(msg["d"]["role"])

        elif msg["t"] == "GUILD_ROLE_DELETE":
            del ctx.guilds[msg["d"]["guild_id"]]._guild["roles"][msg["d"]["role_id"]]

        elif msg["t"] == "GUILD_EMOJIS_UPDATE":
            ctx.guilds[msg["d"]["guild_id"]]._guild["emojis"] = msg["d"]["emojis"]

        elif msg["t"] == "GUILD_MEMBER_ADD":
            ctx.guilds[msg["d"]["guild_id"]]._guild["member_count"] += 1

        elif msg["t"] == "GUILD_MEMBER_REMOVE":
            ctx.guilds[msg["d"]["guild_id"]]._guild["member_count"] -= 1

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
                args = msg["d"]["content"].split(" ")[1:]

                if not command in ctx.commands:
                    for cmd in ctx.commands:
                        if "aliases" in ctx.commands[cmd] and command in ctx.commands[cmd]["aliases"]:
                            command = cmd
                            break

                ctx.command = command
                ctx.args = args
                ctx.token = self.token
                ctx.ws = self.ws

                ctx.data["author"]["member"] = ctx.data["member"]

                ctx.author = Member(ctx.data["author"])
                ctx.guild = ctx.guilds[ctx.data["guild_id"]]
                ctx.channel = ctx.guild.channels[ctx.data["channel_id"]]
                ctx.mentions = [Member(member) for member in ctx.data["mentions"]]

                ctx.send = ctx.channel.send

                try:
                    if command in ctx.commands:
                        func = ctx.commands[command]["function"]
                        needed_args = dict(list(signature(func).parameters.items())[2:])
                        parsed_args = []

                        for needed_arg in needed_args:
                            arg = needed_args[needed_arg]
                            if arg.annotation == _empty:
                                annotation = lambda x: str(x)
                            else:
                                annotation = arg.annotation

                            index = list(needed_args).index(needed_arg)
                            if index < len(args):
                                try:
                                    parsed_arg = annotation(args[index])
                                except:
                                    raise InvalidArgumentType(f"type {annotation} is not valid for {needed_arg} argument", ctx.commands[command], list(needed_args), needed_arg)
                                parsed_args.append(parsed_arg)
                            else:
                                if arg.default == _empty:
                                    raise NoArgument(f"{needed_arg} was not specified", ctx.commands[command], list(needed_args), needed_arg)
                        
                        func(ctx.modules[func.__qualname__.split(".")[0]], ctx, *parsed_args)
                    else:
                        raise CommandNotFound(f"{command} was not found")
                except Exception as error:
                    if "Handler" in ctx.modules and "on_error" in ctx.events:
                        ctx.events["on_error"](ctx.modules["Handler"], ctx, error)
            else:
                ctx.args = msg["d"]["content"].split(" ")

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
