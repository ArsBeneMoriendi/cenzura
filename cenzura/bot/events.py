from lib import modules
from lib.ctx import ctx
import functions
import config
import arrays
import threading
import time

@modules.module
class Events(ctx):
    def __init__(self, bot, discord):
        self.bot = bot
        self.discord = discord

    @modules.event
    def GUILD_MEMBER_ADD(self):
        guilds = functions.read_json("guilds")

        if not self.guild.id in guilds:
            return

        if "welcomemsg" in guilds[self.guild.id]:
            self.discord.send(guilds[self.guild.id]["welcomemsg"]["channel_id"], guilds[self.guild.id]["welcomemsg"]["text"].replace("<>", self.user.username).replace("[]", self.user.mention).replace("{}", str(self.guild.member_count)), reply=False)

        if "autorole" in guilds[self.guild.id]:
            self.discord.add_guild_member_role(self.guild.id, self.user.id, guilds[self.guild.id]["autorole"])

    @modules.event
    def GUILD_MEMBER_REMOVE(self):
        guilds = functions.read_json("guilds")

        if not self.guild.id in guilds:
            return

        if "welcomemsg" in guilds[self.guild.id]:
            self.discord.send(guilds[self.guild.id]["leavemsg"]["channel_id"], guilds[self.guild.id]["leavemsg"]["text"].replace("<>", self.user.username).replace("[]", self.user.mention).replace("{}", str(self.guild.member_count)), reply=False)

    @modules.event
    def MESSAGE_CREATE(self):
        guilds = functions.read_json("guilds")

        if not self.guild.id in guilds:
            guilds[self.guild.id] = {}
            functions.write_json("guilds", guilds)

        if self.author.bot:
            return

        users = functions.read_json("users")

        if not self.author.id in users:
            users[self.author.id] = {}
            functions.write_json("users", users)

        if not hasattr(self, "messages"):
            self.messages = {}

        if not self.data["guild_id"] in self.messages:
            self.messages[self.guild.id] = {}

        self.messages[self.data["guild_id"]][self.data["id"]] = {
            "author": self.author,
            "content": self.data["content"],
            "channel": self.channel
        }

        mentions = [member.id for member in self.mentions]
        
        if self.bot_user.id in mentions and len(self.data["content"].split()) == 1:
            guilds = functions.read_json("guilds")

            if self.guild.id in guilds and "prefix" in guilds[self.guild.id]:
                prefix = guilds[self.guild.id]["prefix"]
            else:
                prefix = config.prefix

            return self.send(f"Mój prefix na tym serwerze to `{prefix}`")

        if self.guild.id in guilds and "cmd" in guilds[self.guild.id] and self.data["content"] in guilds[self.guild.id]["cmd"]:
            self.send(guilds[self.guild.id]["cmd"][self.data["content"]]["text"].replace("<>", self.author.username).replace("[]", self.author.mention))

        if self.author.has_permission("ADMINISTRATOR"):
            return
        
        if self.guild.id in guilds and not "badwords" in guilds[self.guild.id]:
            for badword in arrays.badwords:
                if badword in self.data["content"].upper():
                    if not self.channel.nsfw:
                        if not ("badword_channels" in guilds[self.guild.id] and self.channel.id in guilds[self.guild.id]["badword_channels"]):
                            remove = True
                            if "badword_roles" in guilds[self.guild.id]:
                                for role in self.author.roles:
                                    if role.id in guilds[self.guild.id]["badword_roles"]:
                                        remove = False

                            if remove:
                                status = self.discord.delete_message(self.channel.id, self.data["id"])

                                if status.status_code == 204:
                                    self.send("Na tym serwerze przeklinanie jest wyłączone", reply=False)

                    break

        if self.guild.id in guilds and not "invites" in guilds[self.guild.id]:
            for url in ["discord.gg/", "discord.com/invite/", "discordapp.com/invite/"]:
                if url.upper() in self.data["content"].upper():
                    if not ("invites_channels" in guilds[self.guild.id] and self.channel.id in guilds[self.guild.id]["invites_channels"]):
                        remove = True
                        if "invites_roles" in guilds[self.guild.id]:
                            for role in self.author.roles:
                                if role.id in guilds[self.guild.id]["invites_roles"]:
                                    remove = False

                        if remove:
                            status = self.discord.delete_message(self.channel.id, self.data["id"])

                            if status.status_code == 204:
                                self.send("Na tym serwerze wysyłanie zaproszeń jest wyłączone", reply=False)

                    break

    @modules.event
    def MESSAGE_DELETE(self):
        if not hasattr(ctx, "snipe"):
            ctx.snipe = {}

        if not self.guild.id in self.snipe:
            ctx.snipe[self.guild.id] = []
            
        if self.guild.id in self.messages:
            ctx.snipe[self.guild.id].append(self.messages[self.guild.id][self.data["id"]])

    @modules.event
    def GUILD_ROLE_DELETE(self):
        guilds = functions.read_json("guilds")

        if "mute_role" in guilds[self.guild.id] and guilds[self.guild.id]["mute_role"] == self.role.id:
            del guilds[self.guild.id]["mute_role"]
            functions.write_json("guilds", guilds)