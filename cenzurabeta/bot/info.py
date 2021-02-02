import psutil
import humanize
import platform
from datetime import datetime
from dateutil.relativedelta import relativedelta

def load(gateway, discord):
    @gateway.command(description="Statystyki bota", usage="botstats", category="Info", _default=True)
    def botstats(ctx):
        bot_start = relativedelta(datetime.now(), ctx.bot_start)
        connection_start = relativedelta(datetime.now(), ctx.connection_start)
        description = f"""Serwery: `{len(ctx.guilds)}`
        
        Komendy: `{len(ctx.commands)}`
        
        Wersja Python: `{platform.python_version()}`

        RAM: `{humanize.naturalsize(psutil.Process().memory_full_info().rss)}`
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

    @gateway.command(description="Pokazuje autorów bota", usage="authors", category="Info", _default=True)
    def authors(ctx):
        _authors = {
            "636096693712060416": "developer",
            "264905890824585216": "pomocnik"
        }

        discord.create_message(ctx.data["channel_id"], {
            "embed": {
                "title": "Autorzy:",
                "description": "\n".join([f"{discord.get_user(user)['username']}#{discord.get_user(user)['discriminator']} - {_authors[user]}" for user in _authors]),
                "color": 0xe74c3c,
                "thumbnail": {
                    "url": f"http://cdn.discordapp.com/avatars/{ctx.bot['id']}/{ctx.bot['avatar']}.png?size=2048"
                },
            }
        })
