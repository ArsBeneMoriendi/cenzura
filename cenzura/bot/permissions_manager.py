import functions
from lib.embed import Embed
from lib.errors import NoPermission, NotFound
from lib.types import Role

def load(bot, discord):
    @bot.command(description="Zarządzanie permisjami", usage="pm", category="Zarządzanie permisjami")
    def pm(ctx, subcommand = None, role: Role = None, command = None):
        if not ctx.author.has_permission("ADMINISTRATOR"):
            raise NoPermission(f"{ctx.author.id} has no ADMINISTRATOR permission", "ADMINISTRATOR")

        help_embed = Embed(title="Komendy pm:", description="> `pm add (rola) (komenda)`, `pm remove (rola) (komenda)`, `pm delete (rola)`", color=0xe74c3c)

        if not subcommand and not role:
            return ctx.send(embed=help_embed)

        blacklist = ["help", "botstats", "profile", "todo", "eval", "reload"]
        guilds = functions.read_json("guilds")

        if subcommand == "add":
            if not command in ctx.commands:
                raise NotFound()
            elif command in blacklist:
                return ctx.send("Tej komendy nie można dodać/odebrać!")

            if not role.id in guilds[ctx.guild.id]["permissions"]:
                guilds[ctx.guild.id]["permissions"][role.id] = {}

            guilds[ctx.guild.id]["permissions"][role.id][command] = True

            ctx.send("Dodano permisje")

        elif subcommand == "remove":
            if not command in ctx.commands:
                raise NotFound()
            elif command in blacklist:
                return ctx.send("Tej komendy nie można dodać/odebrać!")

            if not role.id in guilds[ctx.guild.id]["permissions"]:
                guilds[ctx.guild.id]["permissions"][role.id] = {}

            guilds[ctx.guild.id]["permissions"][role.id][command] = False

            ctx.send("Usunięto permisje")
        
        elif subcommand == "delete":
            del guilds[ctx.guild.id]["permissions"][role.id]
            ctx.send("Usunięto role")

        else:
            return ctx.send(embed=help_embed)

        functions.write_json("guilds", guilds)