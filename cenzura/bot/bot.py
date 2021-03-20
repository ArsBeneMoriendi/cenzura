from lib import gateway
from lib import discord
import json
import threading
import time
import random
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

def status(ws):
    quotes = open("quotes.txt", "r")
    statuses = quotes.read().splitlines()
    quotes.close()

    while True:
        data = {
            "op": 3,
            "d": {
                "since": None,
                "activities": [
                    {
                        "name": random.choice(statuses),
                        "type": random.choice(list(range(1, 4)) + [5])
                    }
                ],
                "status": "dnd",
                "afk": False
            }
        }
        
        data = json.dumps(data)
        ws.send(data)
        time.sleep(10)

@bot.event
def ready(ctx):
    threading.Thread(target=status, args=(ctx.data["ws"],)).start()
    print("online")

bot.run(config.token)