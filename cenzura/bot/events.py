from lib import permissions
import functions
import config
import arrays
import threading
import time

def load(bot, discord):
    @bot.event
    def GUILD_MEMBER_ADD(ctx):
        guild = ctx.data["guild_id"]
        guilds = functions.read_json("guilds")

        if not guild in guilds:
            return

        if "welcomemsg" in guilds[guild]:
            discord.send(guilds[guild]["welcomemsg"]["channel_id"], guilds[guild]["welcomemsg"]["text"].replace("<>", ctx.data["user"]["username"]).replace("[]", "<@" + ctx.data["user"]["id"] + ">").replace("{}", str(len(discord.list_guild_members(ctx.data["guild_id"])))), reply=False)

        if "autorole" in guilds[guild]:
            discord.add_guild_member_role(ctx.data["guild_id"], ctx.data["user"]["id"], guilds[guild]["autorole"])

    @bot.event
    def GUILD_MEMBER_REMOVE(ctx):
        guild = ctx.data["guild_id"]
        guilds = functions.read_json("guilds")

        if not guild in guilds:
            return

        if "leavemsg" in guilds[guild]:
            discord.send(guilds[guild]["leavemsg"]["channel_id"], guilds[guild]["leavemsg"]["text"].replace("<>", ctx.data["user"]["username"]).replace("[]", "<@" + ctx.data["user"]["id"] + ">").replace("{}", str(len(discord.list_guild_members(ctx.data["guild_id"])))), reply=False)

    @bot.event
    def MESSAGE_CREATE(ctx):
        guild = ctx.data["guild_id"]
        guilds = functions.read_json("guilds")

        if not guild in guilds:
            guilds[guild] = {}
            functions.write_json("guilds", guilds)

        if "bot" in ctx.data["author"]:
            return

        user = ctx.data["author"]["id"]
        users = functions.read_json("users")

        if not user in users:
            users[user] = {}
            functions.write_json("users", users)

        if not hasattr(ctx, "messages"):
            ctx.messages = {}

        if not ctx.data["guild_id"] in ctx.messages:
            ctx.messages[ctx.data["guild_id"]] = {}

        ctx.messages[ctx.data["guild_id"]][ctx.data["id"]] = {
            "author": ctx.data["author"],
            "content": ctx.data["content"],
            "channel_id": ctx.data["channel_id"]
        }

        mentions = [user["id"] for user in ctx.data["mentions"]]
        
        if ctx.bot["id"] in mentions and len(ctx.data["content"].split()) == 1:
            guild = ctx.data["guild_id"]
            guilds = functions.read_json("guilds")

            if guild in guilds and "prefix" in guilds[guild]:
                prefix = guilds[guild]["prefix"]
            else:
                prefix = config.prefix

            return ctx.send(f"Mój prefix na tym serwerze to `{prefix}`")

        if guild in guilds and "cmd" in guilds[guild] and ctx.data["content"] in guilds[guild]["cmd"]:
            ctx.send(guilds[guild]["cmd"][ctx.data["content"]]["text"].replace("<>", ctx.data["author"]["username"]).replace("[]", "<@" + ctx.data["author"]["id"] + ">"))

        if permissions.has_permission(ctx, ctx.data["author"]["id"], "ADMINISTRATOR"):
            return
        
        if guild in guilds and not "badwords" in guilds[guild]:
            for badword in arrays.badwords:
                if badword in ctx.data["content"].upper():
                    channel = discord.get_channel(ctx.data["channel_id"])
                    
                    if not channel["nsfw"]:
                        status = discord.delete_message(ctx.data["channel_id"], ctx.data["id"])

                        if status.status_code == 204:
                            ctx.send("Na tym serwerze przeklinanie jest wyłączone", reply=False)

                    break

        elif guild in guilds and not "invites" in guilds[guild]:
            for url in ["discord.gg/", "discord.com/invite/", "discordapp.com/invite/"]:
                if url.upper() in ctx.data["content"].upper():
                    status = discord.delete_message(ctx.data["channel_id"], ctx.data["id"])

                    if status.status_code == 204:
                        ctx.send("Na tym serwerze wysyłanie zaproszeń jest wyłączone", reply=False)

                    break

    @bot.event
    def MESSAGE_DELETE(ctx):
        if not hasattr(ctx, "snipe"):
            ctx.snipe = {}

        if not ctx.data["guild_id"] in ctx.snipe:
            ctx.snipe[ctx.data["guild_id"]] = []
            
        ctx.snipe[ctx.data["guild_id"]].append(ctx.messages[ctx.data["guild_id"]][ctx.data["id"]])

    @bot.event
    def GUILD_ROLE_DELETE(ctx):
        guild = ctx.data["guild_id"]
        role = ctx.data["role_id"]

        guilds = functions.read_json("guilds")

        if "mute_role" in guilds[guild] and guilds[guild]["mute_role"] == role:
            del guilds[guild]["mute_role"]
            functions.write_json("guilds", guilds)
