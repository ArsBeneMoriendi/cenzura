from psutil import virtual_memory, Process, cpu_percent
from humanize import naturalsize
from datetime import datetime
from dateutil.relativedelta import relativedelta
from lib.embed import Embed

def load(bot, discord):
    @bot.command(description="Statystyki bota", usage="botstats", category="Info", default=True)
    def botstats(ctx):
        bot_start = relativedelta(datetime.now(), ctx.bot_start)
        connection_start = relativedelta(datetime.now(), ctx.connection_start)

        memory = virtual_memory()

        description = f"""Serwery: `{len(ctx.guilds)}`

Komendy: `{len(ctx.commands)}`

RAM: `{naturalsize(Process().memory_full_info().rss)} ({naturalsize(memory.total - memory.available)} / {naturalsize(memory.total)})`
Procesor: `{cpu_percent()}%`

Uptime bota: `{bot_start.days} dni, {bot_start.hours} godzin, {bot_start.minutes} minut, {bot_start.seconds} sekund`
Uptime połączenia: `{connection_start.days} dni, {connection_start.hours} godzin, {connection_start.minutes} minut, {connection_start.seconds} sekund`"""

        embed = Embed(title="Statystyki bota:", description=description, color=0xe74c3c)
        ctx.send(embed=embed)