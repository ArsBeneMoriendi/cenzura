import psutil
import humanize
import platform
from datetime import datetime
from dateutil.relativedelta import relativedelta

def load(bot, discord):
    @bot.command(description="Statystyki bota", usage="botstats", category="Info", _default=True)
    def botstats(ctx):
        bot_start = relativedelta(datetime.now(), ctx.bot_start)
        connection_start = relativedelta(datetime.now(), ctx.connection_start)

        memory = psutil.virtual_memory()

        description = f"""Serwery: `{len(ctx.guilds)}`
        
Komendy: `{len(ctx.commands)}`
        
Wersja Python: `{platform.python_version()}`

RAM: `{humanize.naturalsize(psutil.Process().memory_full_info().rss)} ({humanize.naturalsize(memory.total - memory.available)} / {humanize.naturalsize(memory.total)})`
Procesor: `{psutil.cpu_percent()}%`
        
Uptime bota: `{bot_start.days} dni, {bot_start.hours} godzin, {bot_start.minutes} minut, {bot_start.seconds} sekund`
Uptime połączenia: `{connection_start.days} dni, {connection_start.hours} godzin, {connection_start.minutes} minut, {connection_start.seconds} sekund`"""

        discord.create_message(ctx.data["channel_id"], {
            "embed": {
                "title": "Statystyki bota:",
                "description": description,
                "color": 0xe74c3c
            }
        })
