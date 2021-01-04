import psutil
import humanize
import platform

def load(gateway, discord):
    @gateway.command(description="Statystyki bota", usage="botstats", category="Info", _default=True)
    def botstats(ctx):
        discord.create_message(ctx.data["channel_id"], {
            "embed": {
                "title": "Statystyki bota:",
                "description": f"Serwery: `{len(ctx.guilds)}`\n\nKomendy: `{len(ctx.commands)}`\n\nWersja Python: `{platform.python_version()}`\nWersja cenzuralib: `0.1`\n\nRAM: `{humanize.naturalsize(psutil.Process().memory_full_info().rss)}`\nProcesor: `{psutil.cpu_percent()}%`",
                "color": 0xe74c3c
            }
        })

    @gateway.command(description="Pokazuje autorów bota", usage="authors", category="Info", _default=True)
    def authors(ctx):
        _authors = {
            "636096693712060416": "developer",
            "264905890824585216": "pomocnik",
            "651511209585147904": "grafik"
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
