import lib.gateway as gateway
import lib.discord as discord
import json
import threading
import time

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

gateway.register_modules(modules, gateway, discord)

def status(ws):
    while True:
        statuses = [
            {
                "name": f"{gateway.ctx.guilds} pustych serwerów",
                "type": 2
            },
            {
                "name": "czubixa jak trzepie freda",
                "type": 3
            },
            {
                "name": "Fortnite w usłudze GeForce NOW",
                "type": 5
            },
            {
                "name": "kanał Kamuś",
                "type": 3
            },
            {
                "name": "jak papież tańczy",
                "type": 3
            },
            {
                "name": "NEKOPARA Vol. 1",
                "type": 1
            }
        ]

        for _status in statuses:
            data = {
                "op": 3,
                "d": {
                    "since": 91879201,
                    "activities": [_status],
                    "status": "dnd",
                    "afk": False
                }
            }
            
            data = json.dumps(data)
            ws.send(data)
            time.sleep(10)

@gateway.event
def ready(ctx):
    threading.Thread(target=status, args=(ctx.data["ws"],)).start()
    print("online")

gateway.run()