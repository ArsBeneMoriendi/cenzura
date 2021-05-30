from lib import gateway
from lib import discord
import json
import config

bot = gateway.Bot(prefix=config.prefix)

modules = [
    "events",
    "help",
    "fun",
    "admin",
    "inne",
    "permissions_manager",
    "info",
    "dev"
]

bot.register_modules(modules, bot, discord)

@bot.event
def ready(ctx):
    data = {
        "op": 3,
        "d": {
            "since": None,
            "activities": [
                {
                    "name": "\u200b",
                    "type": 1
                }
            ],
            "status": "dnd",
            "afk": False
        }
    }

    data = json.dumps(data)
    ctx.ws.send(data)

    print("online")

bot.run(config.token)