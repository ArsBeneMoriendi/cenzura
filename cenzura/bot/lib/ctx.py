import requests
from datetime import datetime

class ctx:
    requests = requests.Session()
    data: dict = {}
    commands: dict = {}
    modules: dict = {}
    events: dict = {}
    default: list = []
    guilds: dict = {}
    ws = None
    bot_start = datetime.now()
    connection_start = None