import functions
import config
import handler
from lib.embed import Embed

def load(bot, discord):
    @bot.command(description="Pokazuje pomoc", usage="help", category="help", default=True)
    def _help(ctx):
        if len(ctx.args) == 1:
            if not ctx.args[0] in ctx.commands:
                return handler.error_handler(ctx, "commandnotfound")

            embed = Embed(title="POMOC:", description=f"Opis: `{ctx.commands[ctx.args[0]]['description']}`\nUżycie: `{ctx.commands[ctx.args[0]]['usage']}`", color=0xe74c3c)
            embed.set_thumbnail(url=f"http://cdn.discordapp.com/avatars/{ctx.bot['id']}/{ctx.bot['avatar']}.png?size=2048")
            embed.set_footer(text="() - obowiązkowe, [] - opcjonalne")
                
            return ctx.send(embed=embed)

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

        embed = Embed(title="POMOC:", description=f"Prefix na tym serwerze to: `{prefix}`\nWpisz `pomoc [komenda]` by sprawdzić użycie danej komendy", color=0xe74c3c)

        for category in categories:
            if not category in blacklist:
                embed.add_field(name=category + ":", value="> " + ", ".join(categories[category]))

        embed.add_field(name="\u200b", value=f"\[ [Dodaj bota](https://discord.com/api/oauth2/authorize?client_id={ctx.bot['id']}&permissions=268561494&scope=bot) \] \[ [Support](https://discord.gg/tDQURnVtGC) \] \[ [Kod bota](https://github.com/CZUBIX/cenzura) \] \[ [Strona](https://cenzurabot.com) \]")
        ctx.send(embed=embed)
