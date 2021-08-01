from lib import modules
import functions
import config
import arrays
import threading
import time
import re
from lib.components import *
from lib.embed import Embed

@modules.module
class Events:
    def __init__(self, bot, discord):
        self.bot = bot
        self.discord = discord
        self.results = {}
        self.embeds = {}
        self.wait_for = []

    @modules.event
    def GUILD_MEMBER_ADD(self, ctx):
        guilds = functions.read_json("guilds")

        if not ctx.guild.id in guilds:
            return

        if "welcomemsg" in guilds[ctx.guild.id]:
            self.discord.send(guilds[ctx.guild.id]["welcomemsg"]["channel_id"], guilds[ctx.guild.id]["welcomemsg"]["text"].replace("<>", ctx.user.username).replace("[]", ctx.user.mention).replace("{}", str(ctx.guild.member_count)), reply=False)

        if "autorole" in guilds[ctx.guild.id]:
            self.discord.add_guild_member_role(ctx.guild.id, ctx.user.id, guilds[ctx.guild.id]["autorole"])

    @modules.event
    def GUILD_MEMBER_REMOVE(self, ctx):
        guilds = functions.read_json("guilds")

        if not ctx.guild.id in guilds:
            return

        if "welcomemsg" in guilds[ctx.guild.id]:
            self.discord.send(guilds[ctx.guild.id]["leavemsg"]["channel_id"], guilds[ctx.guild.id]["leavemsg"]["text"].replace("<>", ctx.user.username).replace("[]", ctx.user.mention).replace("{}", str(ctx.guild.member_count)), reply=False)

    @modules.event
    def MESSAGE_CREATE(self, ctx):
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

        if not hasattr(self, "messages"):
            ctx.messages = {}

        if not ctx.guild.id in ctx.messages:
            ctx.messages[ctx.guild.id] = {}

        ctx.messages[ctx.guild.id][ctx.data["id"]] = {
            "author": ctx.author,
            "content": ctx.data["content"],
            "channel": ctx.channel
        }

        mentions = [member.id for member in ctx.mentions]

        for func in self.wait_for:
            if func[0] == "MESSAGE_CREATE":
                if not func[1](func[2], func[3], ctx.data["content"]) == False:
                    self.wait_for.remove(func)
        
        if ctx.bot_user.id in mentions and len(ctx.data["content"].split()) == 1:
            guilds = functions.read_json("guilds")

            if ctx.guild.id in guilds and "prefix" in guilds[ctx.guild.id]:
                prefix = guilds[ctx.guild.id]["prefix"]
            else:
                prefix = config.prefix

            return ctx.send(f"Mój prefix na tym serwerze to `{prefix}`")

        if ctx.guild.id in guilds and "cmd" in guilds[ctx.guild.id] and ctx.data["content"] in guilds[ctx.guild.id]["cmd"]:
            cmd = guilds[ctx.guild.id]["cmd"][ctx.data["content"]]

            text = None
            embed = None
            
            if "text" in cmd:
                text = cmd["text"].replace("<>", ctx.author.username).replace("[]", ctx.author.mention)

            if "embed" in cmd:
                embed = cmd["embed"]
                
                if "title" in embed:
                    embed["title"] = embed["title"].replace("<>", ctx.author.username).replace("[]", ctx.author.mention)

                if "description" in embed:
                    embed["description"] = embed["description"].replace("<>", ctx.author.username).replace("[]", ctx.author.mention)

                if "description" in embed:
                    embed["description"] = embed["description"].replace("<>", ctx.author.username).replace("[]", ctx.author.mention)

                if "footer" in embed and "text" in embed["footer"]:
                    embed["footer"]["text"] = embed["footer"]["text"].replace("<>", ctx.author.username).replace("[]", ctx.author.mention)

                if "author" in embed and "name" in embed["author"]:
                    embed["author"]["name"] = embed["author"]["name"].replace("<>", ctx.author.username).replace("[]", ctx.author.mention)
                
                if "fields" in embed:
                    for field in embed["fields"]:
                        if "name" in field and "value" in field:
                            field["name"] = field["name"].replace("<>", ctx.author.username).replace("[]", ctx.author.mention)
                            field["value"] = field["value"].replace("<>", ctx.author.username).replace("[]", ctx.author.mention)

            ctx.send(text, embed=embed)

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
                                status = self.discord.delete_message(ctx.channel.id, ctx.data["id"])

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
                            status = self.discord.delete_message(ctx.channel.id, ctx.data["id"])

                            if status.status_code == 204:
                                ctx.send("Na tym serwerze wysyłanie zaproszeń jest wyłączone", reply=False)

                    break

    @modules.event
    def MESSAGE_DELETE(self, ctx):
        if not hasattr(ctx, "snipe"):
            ctx.snipe = {}

        if not ctx.guild.id in ctx.snipe:
            ctx.snipe[ctx.guild.id] = []
            
        if not ctx.guild.id in ctx.messages:
            ctx.messages[ctx.guild.id] = {}

        if ctx.data["id"] in ctx.messages[ctx.guild.id]:
            ctx.snipe[ctx.guild.id].append(ctx.messages[ctx.guild.id][ctx.data["id"]])

    @modules.event
    def GUILD_ROLE_DELETE(self, ctx):
        guilds = functions.read_json("guilds")

        if "mute_role" in guilds[ctx.guild.id] and guilds[ctx.guild.id]["mute_role"] == ctx.role.id:
            del guilds[ctx.guild.id]["mute_role"]
            functions.write_json("guilds", guilds)

    @modules.event
    def INTERACTION_CREATE(self, ctx):
        if not hasattr(ctx, "interactions"):
            ctx.interactions = []

        guilds = functions.read_json("guilds")

        if not "cmd" in guilds[ctx.guild.id]:
            guilds[ctx.guild.id]["cmd"] = {}

        message_id = ctx.data["message"]["id"]

        if ("calc", ctx.member.id, ctx.channel.id, message_id) in ctx.interactions:
            if not message_id in self.results:
                self.results[message_id] = ""

            custom_id = ctx.data["data"]["custom_id"]

            if "=" in self.results[message_id]:
                self.results[message_id] = ""

            if custom_id == "leftbracket":
                self.results[message_id] += "("
            elif custom_id == "rightbracket":
                self.results[message_id] += ")"
            elif custom_id == "power":
                self.results[message_id] += "**"
            elif custom_id == "percent":
                self.results[message_id] += "%"
            elif custom_id == "backspace":
                self.results[message_id] = self.results[message_id][:-1]
            elif custom_id == "clear":
                self.results[message_id] = ""
            elif custom_id == "divide":
                self.results[message_id] += "/"
            elif custom_id == "multiply":
                self.results[message_id] += "*"
            elif custom_id == "minus":
                self.results[message_id] += "-"
            elif custom_id == "dot":
                self.results[message_id] += "."
            elif custom_id == "equal":
                try:
                    result = eval(self.results[message_id])
                    if type(result) == float:
                        result = round(result, 2)
                    self.results[message_id] += "=" + str(result)
                except:
                    if self.results[message_id] == "/0":
                        self.results[message_id] = "KABOOM!"
                    else:
                        self.results[message_id] = ""
            elif custom_id == "add":
                self.results[message_id] += "+"
            elif custom_id == "0":
                if not (self.results[message_id][0] == "0" and len(self.results[message_id]) == 1):
                    self.results[message_id] += "0"
            else:
                self.results[message_id] += custom_id

            ctx.requests.post(f"https://discord.com/api/v8/interactions/{ctx.data['id']}/{ctx.data['token']}/callback", json={
                "type": 7,
                "data": {
                    "content": f"```{self.results[message_id] if self.results[message_id] else '0'}```{'https://imgur.com/a/N19WxP4' if self.results[message_id] == 'KABOOM!' else ''}",
                    "components" if self.results[message_id] == "KABOOM!" else None: []
                }
            })

        elif ("cmd_embed", ctx.member.id, ctx.channel.id, message_id) in ctx.interactions:
            if not message_id in self.embeds:
                self.embeds[message_id] = {
                    "embed": {},
                    "editing": False
                }
                
            if not self.embeds[message_id]["editing"]:
                if ctx.data["data"]["custom_id"] == "save":
                    guilds[ctx.guild.id]["cmd"][ctx.channel.args[1]]["embed"] = self.embeds[message_id]["embed"]
                    ctx.interactions.remove(("cmd_embed", ctx.member.id, ctx.channel.id, message_id))
                    del self.embeds[message_id]
                    
                    ctx.requests.post(f"https://discord.com/api/v8/interactions/{ctx.data['id']}/{ctx.data['token']}/callback", json={
                        "type": 4,
                        "data": {
                            "content": "Dodano embeda do komendy"
                        }
                    })
                
                elif ctx.data["data"]["custom_id"] == "remove":
                    del guilds[ctx.guild.id]["cmd"][ctx.channel.args[1]]["embed"]
                    ctx.interactions.remove(("cmd_embed", ctx.member.id, ctx.channel.id, message_id))
                    del self.embeds[message_id]
                    
                    ctx.requests.post(f"https://discord.com/api/v8/interactions/{ctx.data['id']}/{ctx.data['token']}/callback", json={
                        "type": 4,
                        "data": {
                            "content": "Usunięto embeda z komendy"
                        }
                    })
                    
                elif ctx.data["data"]["custom_id"] == "cancel":
                    ctx.interactions.remove(("cmd_embed", ctx.member.id, ctx.channel.id, message_id))
                    del self.embeds[message_id]

                    ctx.requests.post(f"https://discord.com/api/v8/interactions/{ctx.data['id']}/{ctx.data['token']}/callback", json={
                        "type": 4,
                        "data": {
                            "content": "Anulowano"
                        }
                    })

                elif ctx.data["data"]["custom_id"] in ("author_save", "footer_save"):
                    guilds[ctx.guild.id]["cmd"][ctx.channel.args[1]]["embed"] = self.embeds[message_id]["embed"]

                    components = Components(
                        Row(
                            SelectMenu(
                                custom_id = "embed_creator",
                                placeholder = "Wybierz co chcesz ustawić",
                                options = [
                                    Option("Tytuł", "title"),
                                    Option("Opis", "description"),
                                    Option("Kolor", "color"),
                                    Option("Link do obrazka", "image"),
                                    Option("Link do miniaturki", "thumbnail"),
                                    Option("Footer", "footer", description="konfigurator footera"),
                                    Option("Autor", "author", description="konfigurator autora")
                                ]
                            )
                        ),
                        Row(
                            Button("Zapisz", custom_id="save", style=Styles.Green),
                            Button("Usuń", custom_id="remove", style=Styles.Red),
                            Button("Anuluj", custom_id="cancel", style=Styles.Gray)
                        )
                    )

                    self.discord.edit_message(ctx.channel.id, message_id, components=components)
                    
                    ctx.requests.post(f"https://discord.com/api/v8/interactions/{ctx.data['id']}/{ctx.data['token']}/callback", json={
                        "type": 4,
                        "data": {
                            "content": f"Usunięto {ctx.data['data']['custom_id'].split('_')[0]}a"
                        }
                    })

                elif ctx.data["data"]["custom_id"] in ("author_remove", "footer_remove"):
                    del self.embeds[message_id]["embed"][ctx.data["data"]["custom_id"].split("_")[0]]

                    components = Components(
                        Row(
                            SelectMenu(
                                custom_id = "embed_creator",
                                placeholder = "Wybierz co chcesz ustawić",
                                options = [
                                    Option("Tytuł", "title"),
                                    Option("Opis", "description"),
                                    Option("Kolor", "color"),
                                    Option("Link do obrazka", "image"),
                                    Option("Link do miniaturki", "thumbnail"),
                                    Option("Footer", "footer", description="konfigurator footera"),
                                    Option("Autor", "author", description="konfigurator autora")
                                ]
                            )
                        ),
                        Row(
                            Button("Zapisz", custom_id="save", style=Styles.Green),
                            Button("Usuń", custom_id="remove", style=Styles.Red),
                            Button("Anuluj", custom_id="cancel", style=Styles.Gray)
                        )
                    )

                    self.discord.edit_message(ctx.channel.id, message_id, components=components)
                    
                    ctx.requests.post(f"https://discord.com/api/v8/interactions/{ctx.data['id']}/{ctx.data['token']}/callback", json={
                        "type": 4,
                        "data": {
                            "content": f"Usunięto {ctx.data['data']['custom_id'].split('_')[0]}a"
                        }
                    })

                elif ctx.data["data"]["custom_id"] in ("author_cancel", "footer_cancel"):
                    components = Components(
                        Row(
                            SelectMenu(
                                custom_id = "embed_creator",
                                placeholder = "Wybierz co chcesz ustawić",
                                options = [
                                    Option("Tytuł", "title"),
                                    Option("Opis", "description"),
                                    Option("Kolor", "color"),
                                    Option("Link do obrazka", "image"),
                                    Option("Link do miniaturki", "thumbnail"),
                                    Option("Footer", "footer", description="konfigurator footera"),
                                    Option("Autor", "author", description="konfigurator autora")
                                ]
                            )
                        ),
                        Row(
                            Button("Zapisz", custom_id="save", style=Styles.Green),
                            Button("Usuń", custom_id="remove", style=Styles.Red),
                            Button("Anuluj", custom_id="cancel", style=Styles.Gray)
                        )
                    )

                    self.discord.edit_message(ctx.channel.id, message_id, components=components)
                    
                    ctx.requests.post(f"https://discord.com/api/v8/interactions/{ctx.data['id']}/{ctx.data['token']}/callback", json={
                        "type": 4,
                        "data": {
                            "content": "Anulowano"
                        }
                    })

                elif ctx.data["data"]["custom_id"] == "embed_creator":
                    self.embeds[message_id]["editing"] = True
                    selected = ctx.data["data"]["values"][0]
                    
                    data = {
                        "flags": 1 << 6
                    }

                    if selected in ("title", "description", "color", "image", "thumbnail", "footer_text", "footer_icon", "author_name", "author_icon"):
                        data["content"] = "Wyślij wiadomość aby ustawić %s (jeśli chcesz usunąć to wpisz `usun`)" % {"title": "tytuł", "description": "opis", "color": "kolor (hex albo rgb)", "image": "obrazek", "thumbnail": "miniaturke", "footer": "footer", "author": "autora", "author_name": "nazwe autora", "author_icon": "ikonke autora", "footer_text": "tekst footera", "footer_icon": "ikonke footera"}[selected]
                        
                        def func(channel, member, content):
                            if not (channel == ctx.channel and member == ctx.author):
                                return False

                            _components = None

                            if not content in ("usun", "usuń", "remove", "delete"):
                                if selected == "color":
                                    color = re.search(r"(?:[0-9a-fA-F]{3}){1,2}$", content)

                                    if len(content.split(" ")) == 3:
                                        color = int("%02x%02x%02x" % tuple((0 if not x.isdigit() else int(x)) for x in content.split(" ")), 16)
                                    else:
                                        color = int("ffffff" if not color else color.group(), 16)

                                    content = color

                                elif selected in ("image", "thumbnail"):
                                    content = {
                                        "url": content
                                    }

                                elif selected == "author_name":
                                    content = {
                                        "name": content
                                    }

                                    components = Components(
                                        Row(
                                            SelectMenu(
                                                custom_id = "embed_creator",
                                                placeholder = "Wybierz co chcesz ustawić",
                                                options = [
                                                    Option("Nazwa", "author_name"),
                                                    Option("Link do ikonki", "author_icon")
                                                ]
                                            )
                                        ),
                                        Row(
                                            Button("Zapisz", custom_id="author_save", style=Styles.Green),
                                            Button("Usuń", custom_id="author_remove", style=Styles.Red),
                                            Button("Anuluj", custom_id="author_cancel", style=Styles.Gray)
                                        )
                                    )

                                    _components = components

                                elif selected == "author_icon":
                                    content = {
                                        "name": self.embeds[message_id]["embed"]["author"]["name"],
                                        "icon_url": content
                                    }

                                elif selected == "footer_text":
                                    content = {
                                        "text": content
                                    }

                                    components = Components(
                                        Row(
                                            SelectMenu(
                                                custom_id = "embed_creator",
                                                placeholder = "Wybierz co chcesz ustawić",
                                                options = [
                                                    Option("Tekst", "footer_name"),
                                                    Option("Link do ikonki", "footer_icon")
                                                ]
                                            )
                                        ),
                                        Row(
                                            Button("Zapisz", custom_id="footer_save", style=Styles.Green),
                                            Button("Usuń", custom_id="footer_remove", style=Styles.Red),
                                            Button("Anuluj", custom_id="footer_cancel", style=Styles.Gray)
                                        )
                                    )

                                    _components = components

                                elif selected == "footer_icon":
                                    content = {
                                        "text": self.embeds[message_id]["embed"]["footer"]["text"],
                                        "icon_url": content
                                    }

                                self.embeds[message_id]["embed"][selected.split("_")[0]] = content
                                ctx.send("Ustawiono %s" % {"title": "tytuł", "description": "opis", "color": "kolor", "image": "obrazek", "thumbnail": "miniaturke", "footer": "footer", "author": "autora", "author_name": "nazwe autora", "author_icon": "ikonke autora", "footer_text": "tekst footera", "footer_icon": "ikonke footera"}[selected])
                            else:
                                if selected in self.embeds[message_id]["embed"]:
                                    del self.embeds[message_id]["embed"][selected]
                                ctx.send("Usunięto %s" % {"title": "tytuł", "description": "opis", "color": "kolor", "image": "obrazek", "thumbnail": "miniaturke", "footer": "footer", "author": "autora", "author_name": "nazwe autora", "author_icon": "ikonke autora", "footer_text": "tekst footera", "footer_icon": "ikonke footera"}[selected])

                            self.embeds[message_id]["editing"] = False
                            if not _components:
                                self.discord.edit_message(channel.id, message_id, embed = self.embeds[message_id]["embed"])
                            else:
                                self.discord.edit_message(channel.id, message_id, embed = self.embeds[message_id]["embed"], components = _components)

                        self.wait_for.append(("MESSAGE_CREATE", func, ctx.channel, ctx.member))

                    elif selected == "author":
                        data["content"] = "Naciśnij na liste jeszcze raz"
                        
                        components = Components(
                            Row(
                                SelectMenu(
                                    custom_id = "embed_creator",
                                    placeholder = "Wybierz co chcesz ustawić",
                                    options = [
                                        Option("Nazwa", "author_name")
                                    ]
                                )
                            ),
                            Row(
                                Button("Zapisz", custom_id="author_save", style=Styles.Green),
                                Button("Usuń", custom_id="author_remove", style=Styles.Red),
                                Button("Anuluj", custom_id="author_cancel", style=Styles.Gray)
                            )
                        )

                        self.embeds[message_id]["editing"] = False
                        self.discord.edit_message(ctx.channel.id, message_id, components=components)

                    elif selected == "footer":
                        data["content"] = "Naciśnij na liste jeszcze raz"
                        
                        components = Components(
                            Row(
                                SelectMenu(
                                    custom_id = "embed_creator",
                                    placeholder = "Wybierz co chcesz ustawić",
                                    options = [
                                        Option("Tekst", "footer_text")
                                    ]
                                )
                            ),
                            Row(
                                Button("Zapisz", custom_id="footer_save", style=Styles.Green),
                                Button("Usuń", custom_id="footer_remove", style=Styles.Red),
                                Button("Anuluj", custom_id="footer_cancel", style=Styles.Gray)
                            )
                        )

                        self.embeds[message_id]["editing"] = False
                        self.discord.edit_message(ctx.channel.id, message_id, components=components)

                    ctx.requests.post(f"https://discord.com/api/v8/interactions/{ctx.data['id']}/{ctx.data['token']}/callback", json={
                        "type": 4,
                        "data": data
                    })

        functions.write_json("guilds", guilds)