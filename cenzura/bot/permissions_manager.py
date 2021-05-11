from lib import permissions
import handler
import json
import functions

def load(bot, discord):
    @bot.command(description="Zarządzanie permisjami", usage="pm", category="Zarządzanie permisjami", _default=False)
    def pm(ctx):
        permission = "ADMINISTRATOR"
        if not (permissions.has_permission(ctx, ctx.data["author"]["id"], permission) or (ctx.data["author"]["id"] == ctx.guilds[ctx.data["guild_id"]]["owner_id"])):
            return handler.error_handler(ctx, "nopermission", permission)

        if not (ctx.args and ctx.data["mention_roles"]):
            return discord.create_message(ctx.data["channel_id"], {
                "embed": {
                    "title": "Komendy pm:",
                    "description": "> `pm add (rola) (komenda)`, `pm remove (rola) (komenda)`, `pm delete (rola)`",
                    "color": 0xe74c3c
                }
            })

        blacklist = ["help", "botstats", "profile", "todo", "eval", "reload"]

        guild = ctx.data["guild_id"]
        guilds = functions.read_json("guilds")

        if ctx.args[0] == "add":
            if not ctx.args[2] in ctx.commands:
                return handler.error_handler(ctx, "notfound")
            elif ctx.args[2] in blacklist:
                return discord.create_message(ctx.data["channel_id"], {
                    "content": "Tej komendy nie można dodać/odebrać!"
                })

            if not ctx.data["mention_roles"][0] in guilds[guild]["permissions"]:
                guilds[guild]["permissions"][ctx.data["mention_roles"][0]] = {}

            guilds[guild]["permissions"][ctx.data["mention_roles"][0]][ctx.args[2]] = True

            discord.create_message(ctx.data["channel_id"], {
                "content": "Dodano permisje"
            })

        elif ctx.args[0] == "remove":
            if not ctx.args[2] in ctx.commands:
                return handler.error_handler(ctx, "notfound")
            elif ctx.args[2] in blacklist:
                return discord.create_message(ctx.data["channel_id"], {
                    "content": "Tej komendy nie można dodać/odebrać!"
                })

            if not ctx.data["mention_roles"][0] in guilds[guild]["permissions"]:
                guilds[guild]["permissions"][ctx.data["mention_roles"][0]] = {}

            guilds[guild]["permissions"][ctx.data["mention_roles"][0]][ctx.args[2]] = False

            discord.create_message(ctx.data["channel_id"], {
                "content": "Usunięto permisje"
            })

        
        elif ctx.args[0] == "delete":
            del guilds[guild]["permissions"][ctx.data["mention_roles"][0]]

            discord.create_message(ctx.data["channel_id"], {
                "content": "Usunięto role"
            })

        else:
             return discord.create_message(ctx.data["channel_id"], {
                "embed": {
                    "title": "Komendy pm:",
                    "description": "> `pm add (rola) (komenda)`, `pm remove (rola) (komenda)`, `pm delete (rola)`",
                    "color": 0xe74c3c
                }
            })

        functions.write_json("guilds", guilds)
