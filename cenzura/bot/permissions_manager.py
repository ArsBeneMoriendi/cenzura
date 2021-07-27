from lib import modules
from lib.ctx import ctx
import functions
from lib.embed import Embed
from lib.errors import NoPermission, NotFound
from lib.types import Role

@modules.module
class PermissionsManager(ctx):
    def __init__(self, bot, discord):
        self.bot = bot
        self.discord = discord

    @modules.command(description="Zarządzanie permisjami", usage="pm")
    def pm(self, subcommand = None, role: Role = None, command = None):
        if not self.author.has_permission("ADMINISTRATOR"):
            raise NoPermission(f"{self.author.id} has no ADMINISTRATOR permission", "ADMINISTRATOR")

        help_embed = Embed(title="Komendy pm:", description="> `pm add (rola) (komenda)`, `pm remove (rola) (komenda)`, `pm delete (rola)`", color=0xe74c3c)

        if not subcommand and not role:
            return self.send(embed=help_embed)

        blacklist = ["help", "botstats", "profile", "todo", "eval", "reload"]
        guilds = functions.read_json("guilds")

        if subcommand == "add":
            if not command in self.commands:
                raise NotFound()
            elif command in blacklist:
                return self.send("Tej komendy nie można dodać/odebrać!")

            if not role.id in guilds[self.guild.id]["permissions"]:
                guilds[self.guild.id]["permissions"][role.id] = {}

            guilds[self.guild.id]["permissions"][role.id][command] = True

            self.send("Dodano permisje")

        elif subcommand == "remove":
            if not command in self.commands:
                raise NotFound()
            elif command in blacklist:
                return self.send("Tej komendy nie można dodać/odebrać!")

            if not role.id in guilds[self.guild.id]["permissions"]:
                guilds[self.guild.id]["permissions"][role.id] = {}

            guilds[self.guild.id]["permissions"][role.id][command] = False

            self.send("Usunięto permisje")
        
        elif subcommand == "delete":
            del guilds[self.guild.id]["permissions"][role.id]
            self.send("Usunięto role")

        else:
            return self.send(embed=help_embed)

        functions.write_json("guilds", guilds)