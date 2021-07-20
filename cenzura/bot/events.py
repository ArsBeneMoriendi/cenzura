import functions
import config
import arrays
import threading
import time

def load(bot, discord):
    @bot.event
    def GUILD_MEMBER_ADD(ctx):
        guilds = functions.read_json("guilds")

        if not ctx.guild.id in guilds:
            return

        if "welcomemsg" in guilds[ctx.guild.id]:
            discord.send(guilds[ctx.guild.id]["welcomemsg"]["channel_id"], guilds[ctx.guild.id]["welcomemsg"]["text"].replace("<>", ctx.user.username).replace("[]", ctx.user.mention).replace("{}", str(ctx.guild.member_count)), reply=False)

        if "autorole" in guilds[ctx.guild.id]:
            discord.add_guild_member_role(ctx.guild.id, ctx.user.id, guilds[ctx.guild.id]["autorole"])

    @bot.event
    def GUILD_MEMBER_REMOVE(ctx):
        guilds = functions.read_json("guilds")

        if not ctx.guild.id in guilds:
            return

        if "welcomemsg" in guilds[ctx.guild.id]:
            discord.send(guilds[ctx.guild.id]["leavemsg"]["channel_id"], guilds[ctx.guild.id]["leavemsg"]["text"].replace("<>", ctx.user.username).replace("[]", ctx.user.mention).replace("{}", str(ctx.guild.member_count)), reply=False)

    @bot.event
    def MESSAGE_CREATE(ctx):
        guilds = functions.read_json("guilds")

        if not ctx.guild.id in guilds:
            guilds[ctx.guild.id] = {}
            functions.write_json("guilds", guilds)

        if ctx.author.bot:
            return

        users = functions.read_json("users")

        if not ctx.author.id in users:
            users[ctx.author.id] = {}
            functions.write_json("users", users)

        if not hasattr(ctx, "messages"):
            ctx.messages = {}

        if not ctx.data["guild_id"] in ctx.messages:
            ctx.messages[ctx.guild.id] = {}

        ctx.messages[ctx.data["guild_id"]][ctx.data["id"]] = {
            "author": ctx.author,
            "content": ctx.data["content"],
            "channel": ctx.channel
        }

        mentions = [member.id for member in ctx.mentions]
        
        if ctx.bot.id in mentions and len(ctx.data["content"].split()) == 1:
            guilds = functions.read_json("guilds")

            if ctx.guild.id in guilds and "prefix" in guilds[ctx.guild.id]:
                prefix = guilds[ctx.guild.id]["prefix"]
            else:
                prefix = config.prefix

            return ctx.send(f"Mój prefix na tym serwerze to `{prefix}`")

        if ctx.guild.id in guilds and "cmd" in guilds[ctx.guild.id] and ctx.data["content"] in guilds[ctx.guild.id]["cmd"]:
            ctx.send(guilds[ctx.guild.id]["cmd"][ctx.data["content"]]["text"].replace("<>", ctx.author.username).replace("[]", ctx.author.mention))

        if ctx.author.has_permission("ADMINISTRATOR"):
            return
        
        if ctx.guild.id in guilds and not "badwords" in guilds[ctx.guild.id]:
            for badword in arrays.badwords:
                if badword in ctx.data["content"].upper():
                    if not ctx.channel.nsfw:
                        if not ("badword_channels" in guilds[ctx.guild.id] and ctx.channel.id in guilds[ctx.guild.id]["badword_channels"]):
                            remove = True
                            if "badword_roles" in guilds[ctx.guild.id]:
                                for role in ctx.author.roles:
                                    if role.id in guilds[ctx.guild.id]["badword_roles"]:
                                        remove = False

                            if remove:
                                status = discord.delete_message(ctx.channel.id, ctx.data["id"])

                                if status.status_code == 204:
                                    ctx.send("Na tym serwerze przeklinanie jest wyłączone", reply=False)

                    break

        if ctx.guild.id in guilds and not "invites" in guilds[ctx.guild.id]:
            for url in ["discord.gg/", "discord.com/invite/", "discordapp.com/invite/"]:
                if url.upper() in ctx.data["content"].upper():
                    if not ("invites_channels" in guilds[ctx.guild.id] and ctx.channel.id in guilds[ctx.guild.id]["invites_channels"]):
                        remove = True
                        if "invites_roles" in guilds[ctx.guild.id]:
                            for role in ctx.author.roles:
                                if role.id in guilds[ctx.guild.id]["invites_roles"]:
                                    remove = False

                        if remove:
                            status = discord.delete_message(ctx.channel.id, ctx.data["id"])

                            if status.status_code == 204:
                                ctx.send("Na tym serwerze wysyłanie zaproszeń jest wyłączone", reply=False)

                    break

    @bot.event
    def MESSAGE_DELETE(ctx):
        if not hasattr(ctx, "snipe"):
            ctx.snipe = {}

        if not ctx.guild.id in ctx.snipe:
            ctx.snipe[ctx.guild.id] = []
            
        ctx.snipe[ctx.guild.id].append(ctx.messages[ctx.guild.id][ctx.data["id"]])

    @bot.event
    def GUILD_ROLE_DELETE(ctx):
        guilds = functions.read_json("guilds")

        if "mute_role" in guilds[ctx.guild.id] and guilds[ctx.guild.id]["mute_role"] == ctx.role.id:
            del guilds[ctx.guild.id]["mute_role"]
            functions.write_json("guilds", guilds)
