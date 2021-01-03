import websocket
import json
import threading
import time
from datetime import datetime
import config
from . import discord
import functions
import json
import copy
import handler

gateway = "wss://gateway.discord.gg/?v=6&encoding=json"
commands = {}
events = {}
default = []

class ctx:
    running = True
    token = config.token
    bot = discord.get_current_user()
    commands = {}
    events = {}
    default = []
    guilds = 0

def command(description, usage, category, _default):
    def _command(func):
        if func.__name__.startswith("_"):
            commands[func.__name__[1:]] = {}
            commands[func.__name__[1:]]["description"] = description
            commands[func.__name__[1:]]["usage"] = usage
            commands[func.__name__[1:]]["category"] = category
            commands[func.__name__[1:]]["function"] = func

            if _default:
                default.append(func.__name__[1:])

            with open(config.folder + "commands.json", "w") as f:
                cmds = copy.deepcopy(commands)
                for cmd in cmds:
                    del cmds[cmd]["function"]

                json.dump(cmds, f, indent=4)
                
            return

        commands[func.__name__] = {}
        commands[func.__name__]["description"] = description
        commands[func.__name__]["usage"] = usage
        commands[func.__name__]["category"] = category
        commands[func.__name__]["function"] = func

        if _default:
            default.append(func.__name__)

        with open(config.folder + "commands.json", "w") as f:
            cmds = copy.deepcopy(commands)
            for cmd in cmds:
                del cmds[cmd]["function"]

            json.dump(cmds, f, indent=4)

    return _command

def event(func):
    events[func.__name__] = func

def register_modules(modules: list, _gateway, _discord):
    for module in modules:
        __import__(module).load(_gateway, _discord)

def register_module(module, _gateway, _discord):
    __import__(module).load(_gateway, _discord)

def heartbeat(ws):
    while True:
        time.sleep(41250 / 1000)

        data = {
            "op": 1,
            "d": 251
        }

        data = json.dumps(data)
        ws.send(data)

def on_message(ws, msg):
    msg = json.loads(msg)

    if msg["op"] == 10:
        data = {
            "op": 1,
            "d": 251
        }

        data = json.dumps(data)
        ws.send(data)

        data = {
            "op": 2,
            "d": {
                "token": f"Bot {ctx.token}",
                "intents": 32511,
                "properties": {
                    "$os": "linux",
                    "$browser": "cenzuralib",
                    "$device": "cenzuralib"
                }
            }
        }

        data = json.dumps(data)
        ws.send(data)

        threading.Thread(target=heartbeat, args=(ws,)).start()
        
        if "ready" in events:
            ctx.data = {"ws": ws}
            events["ready"](ctx)

    if msg["t"] == "GUILD_CREATE":
        ctx.guilds += 1
    elif msg["t"] == "GUILD_DELETE":
        ctx.guilds -= 1
    elif msg["t"] == "MESSAGE_CREATE":
        ctx.data = msg["d"]

        guild = ctx.data["guild_id"]
        guilds = functions.read_json("guilds")

        if guild in guilds and "prefix" in guilds[guild]:
            prefix = guilds[guild]["prefix"]
        else:
            prefix = config.prefix

        if msg["d"]["content"].startswith(prefix):
            command = msg["d"]["content"].split(" ")[0][len(prefix)::]
            if command.startswith("_"):
                command = command[1:]
            args = msg["d"]["content"].split(" ")[1:]
            
            ctx.command = command
            ctx.args = args
            ctx.commands = commands
            ctx.events = events
            ctx.default = default

            if command in commands:
                commands[command]["function"](ctx)
            else:
                handler.error_handler(ctx, "commandnotfound")
        else:
            if msg["t"] in events:
                ctx.args = msg["d"]["content"].split(" ")
                events[msg["t"]](ctx)
    else:
        if msg["t"] in events:
            ctx.data = msg["d"]
            events[msg["t"]](ctx)

def on_close(ws):
    if ctx.running:
        time.sleep(10)
        ctx.guilds = 0
        run()
    else:
        exit(0)

def run():
    ws = websocket.WebSocketApp(gateway, on_message=on_message, on_close=on_close)
    ctx.ws = ws
    ws.run_forever()