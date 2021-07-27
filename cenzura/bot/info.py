from lib import modules
from lib.ctx import ctx
from psutil import virtual_memory, Process, cpu_percent
from humanize import naturalsize
from datetime import datetime
from dateutil.relativedelta import relativedelta
from lib.embed import Embed

@modules.module
class Info(ctx):
    def __init__(self, bot, discord):
        self.bot = bot
        self.discord = discord

    @modules.command(description="Statystyki bota", usage="botstats", default=True)
    def botstats(self):
        bot_start = relativedelta(datetime.now(), self.bot_start)
        connection_start = relativedelta(datetime.now(), self.connection_start)

        memory = virtual_memory()

        description = f"""Serwery: `{len(self.guilds)}`

Komendy: `{len(self.commands)}`

RAM: `{naturalsize(Process().memory_full_info().rss)} ({naturalsize(memory.total - memory.available)} / {naturalsize(memory.total)})`
Procesor: `{cpu_percent()}%`

Uptime bota: `{bot_start.days} dni, {bot_start.hours} godzin, {bot_start.minutes} minut, {bot_start.seconds} sekund`
Uptime połączenia: `{connection_start.days} dni, {connection_start.hours} godzin, {connection_start.minutes} minut, {connection_start.seconds} sekund`"""

        embed = Embed(title="Statystyki bota:", description=description, color=0xe74c3c)
        self.send(embed=embed)