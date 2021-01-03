import functions
import config

def load(gateway, discord):
    @gateway.command(description="Pokazuje pomoc", usage="help", category="help", _default=True)
    def help(ctx):
        if len(ctx.args) == 1:
            return discord.create_message(ctx.data["channel_id"], {
                "embed": {
                    "title": "POMOC:",
                    "description": f"Opis: `{ctx.commands[ctx.args[0]]['description']}`\nUżycie: `{ctx.commands[ctx.args[0]]['usage']}`",
                    "color": 0xe74c3c,
                    "thumbnail": {
                        "url": f"http://cdn.discordapp.com/avatars/{ctx.bot['id']}/{ctx.bot['avatar']}.png?size=2048"
                    },
                    "footer": {
                        "text": "() - obowiązkowe, [] - opcjonalne"
                    }
                }
            })

        guild = ctx.data["guild_id"]
        guilds = functions.read_json("guilds")

        if guild in guilds and "prefix" in guilds[guild]:
            prefix = guilds[guild]["prefix"]
        else:
            prefix = config.prefix
        
        blacklist = ["help", "dev"]

        categories = {}
        for command in ctx.commands:
            if not ctx.commands[command]["category"] in categories:
                categories[ctx.commands[command]["category"]] = []

        for command in ctx.commands:
            categories[ctx.commands[command]["category"]].append("`" + command + "`")

        fields = []
        for category in categories:
            if not category in blacklist:
                fields.append({
                    "name": category + ":",
                    "value": "> " + ", ".join(categories[category]),
                    "inline": False
                })

        fields.append({
                        "name": "\u200b",
                        "value": f"\[ [Dodaj bota](https://discord.com/api/oauth2/authorize?client_id={ctx.bot['id']}&permissions=268561494&scope=bot) \] \[ [Support](https://discord.gg/kJuGceekR5) \] \[ [Kod bota](https://github.com/CZUBIX/cenzura) \] \[ [Strona](https://cenzurabot.pl) \]",
                        "inline": False
                    })

        discord.create_message(ctx.data["channel_id"], {
            "embed": {
                "title": "POMOC:",
                "description": f"Prefix na tym serwerze to: `{prefix}`\nWpisz `pomoc [komenda]` by sprawdzić użycie danej komendy",
                "color": 0xe74c3c,
                "fields": fields
            }
        })
