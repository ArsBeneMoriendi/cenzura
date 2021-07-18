import functions
import config
from lib.embed import Embed
from lib.errors import CommandNotFound

def load(bot, discord):
    @bot.command(description="Pokazuje pomoc", usage="help [komenda]", category="help", default=True)
    def _help(ctx, command = None):
        if command:
            if not command in ctx.commands:
                raise CommandNotFound(f"{command} was not found")

            embed = Embed(title="POMOC:", description=f"Opis: `{ctx.commands[command]['description']}`\nUżycie: `{ctx.commands[command]['usage']}`", color=0xe74c3c)
            embed.set_thumbnail(url=ctx.bot.avatar_url)
            embed.set_footer(text="() - obowiązkowe, [] - opcjonalne")
                
            return ctx.send(embed=embed)

        guilds = functions.read_json("guilds")

        if ctx.guild.id in guilds and "prefix" in guilds[ctx.guild.id]:
            prefix = guilds[ctx.guild.id]["prefix"]
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

        embed.add_field(name="\u200b", value=f"\[ [Dodaj bota](https://discord.com/oauth2/authorize?client_id={ctx.bot.id}&permissions=268561494&scope=bot) \] \[ [Support](https://discord.gg/tDQURnVtGC) \] \[ [Kod bota](https://github.com/CZUBIX/cenzura) \] \[ [Strona](https://cenzurabot.com) \]")
        ctx.send(embed=embed)
