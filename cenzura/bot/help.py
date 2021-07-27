from lib import modules
from lib.ctx import ctx
import functions
import config
from lib.embed import Embed
from lib.errors import CommandNotFound

@modules.module
class Help(ctx):
    def __init__(self, bot, discord):
        self.bot = bot
        self.discord = discord

    @modules.command(description="Pokazuje pomoc", usage="help [komenda]", default=True)
    def _help(self, command = None):
        if command:
            if not command in self.commands:
                raise CommandNotFound(f"{command} was not found")

            embed = Embed(title="POMOC:", description=f"Opis: `{self.commands[command]['description']}`\nUżycie: `{self.commands[command]['usage']}`", color=0xe74c3c)
            embed.set_thumbnail(url=self.bot_user.avatar_url)
            embed.set_footer(text="() - obowiązkowe, [] - opcjonalne")
                
            return self.send(embed=embed)

        guilds = functions.read_json("guilds")

        if self.guild.id in guilds and "prefix" in guilds[self.guild.id]:
            prefix = guilds[self.guild.id]["prefix"]
        else:
            prefix = config.prefix
        
        blacklist = ["Help", "Handler", "Dev"]

        names = {
            "PermissionsManager": "Zarządzanie permisjami"
        }

        categories = {}
        for command in self.commands:
            if not self.commands[command]["function"].__qualname__.split(".")[0] in categories:
                categories[self.commands[command]["function"].__qualname__.split(".")[0]] = []

            categories[self.commands[command]["function"].__qualname__.split(".")[0]].append("`" + command + "`")

        embed = Embed(title="POMOC:", description=f"Prefix na tym serwerze to: `{prefix}`\nWpisz `pomoc [komenda]` by sprawdzić użycie danej komendy", color=0xe74c3c)

        for category in categories:
            if not category in blacklist:
                embed.add_field(name=(category if not category in names else names[category]) + ":", value="> " + ", ".join(categories[category]))

        embed.add_field(name="\u200b", value=f"\[ [Dodaj bota](https://discord.com/oauth2/authorize?client_id={self.bot_user.id}&permissions=268561494&scope=bot) \] \[ [Support](https://discord.gg/tDQURnVtGC) \] \[ [Kod bota](https://github.com/CZUBIX/cenzura) \] \[ [Strona](https://cenzurabot.com) \]")
        self.send(embed=embed)
