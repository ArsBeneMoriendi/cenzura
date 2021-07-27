from lib import modules
from lib.ctx import ctx
import random
from PIL import Image, ImageDraw, ImageFont, ImageOps
import os
import pyfiglet
from functions import *
import config
import time
import arrays
from bs4 import BeautifulSoup
import lxml
import cchardet
from lib.errors import NoPermission, InvalidArgumentType
from lib.types import User, Member
from lib.embed import Embed
from lib.components import Components, Row, Button, Styles

interactions = []
results = {}

@modules.module
class Fun(ctx):
    def __init__(self, bot, discord):
        self.bot = bot
        self.discord = discord
        
    @modules.command(description="Losuje liczbe", usage="rnumber (od) (do)", default=True)
    def rnumber(self, _from: int, to: int):
        if not has_permission(self):
            raise NoPermission(f"{self.author.id} has no {self.command} permission", self.command)
        
        self.send(random.randint(_from, to))

    @modules.command(description="Losuje tekst z podanych", usage="rchoice (a) | (b) | [c] itd.", default=True)
    def rchoice(self, args):
        if not has_permission(self):
            raise NoPermission(f"{self.author.id} has no {self.command} permission", self.command)

        self.args = " ".join(self.args)
        self.args = self.args.split(" | ")

        if not len(self.args) >= 2:
            return self.send("Podaj chociaż więcej niż 2 argumenty")

        self.send(random.choice(self.args))

    @modules.command(description="Pokazuje avatar", usage="avatar [osoba]", default=True)
    def avatar(self, user: User = None):
        if not has_permission(self):
            raise NoPermission(f"{self.author.id} has no {self.command} permission", self.command)

        user = user or self.author
        image = self.requests.get(user.avatar_url).content

        self.send(files=[("avatar.png", image)])

    @modules.command(description="Pokazuje w ilu procentach osoby sie kochają", usage="ship (osoba) [osoba]", default=True)
    def ship(self, user: User, user2: User = None):
        if not has_permission(self):
            raise NoPermission(f"{self.author.id} has no {self.command} permission", self.command)

        if not user2:
            user2 = user
            user = self.author

        if user == user2:
            raise InvalidArgumentType("user is the same as user2", self.commands[self.command], ["user", "user2"], "user2")

        open("images/member1.png", "wb").write(self.requests.get(user.avatar_url).content)
        open("images/member2.png", "wb").write(self.requests.get(user2.avatar_url).content)
        
        para = Image.open("images/para.png").convert("RGBA")
        member1 = Image.open("images/member1.png").convert("RGBA")
        member2 = Image.open("images/member2.png").convert("RGBA")

        member1 = ImageOps.fit(member1, (300, 300))
        member2 = ImageOps.fit(member2, (300, 300))
        
        para.paste(member1, (360, 250), member1)
        para.paste(member2, (890, 180), member2)
        
        para.save("images/ship.png")

        random.seed(get_int(user, user2))
        self.send(f"**{user.username}** + **{user2.username}** = **{user.username[:round(len(user.username) / 2)].lower()}{user2.username[round(len(user2.username) / 2):].lower()}**\nIch miłość jest równa **{random.randint(0, 100)}%**!", files=[("ship.png", open("images/ship.png", "rb"))])

    @modules.command(description="Uderza osobe", usage="slap (osoba)", default=True)
    def slap(self, user: User):
        if not has_permission(self):
            raise NoPermission(f"{self.author.id} has no {self.command} permission", self.command)

        if user == self.author:
            raise InvalidArgumentType("user is the same as author", self.commands[self.command], ["user"], "user")

        image_url = self.requests.get("https://nekos.life/api/v2/img/slap").json()["url"]
        image = self.requests.get(image_url).content

        self.send(f"**{self.author.username}** uderzył **{user.username}**!", files=[("slap.gif", image)])

    @modules.command(description="Całuje osobe", usage="kiss (osoba)", default=True)
    def kiss(self, user: User):
        if not has_permission(self):
            raise NoPermission(f"{self.author.id} has no {self.command} permission", self.command)

        if user == self.author:
            raise InvalidArgumentType("user is the same as author", self.commands[self.command], ["user"], "user")

        image_url = self.requests.get("https://nekos.life/api/kiss").json()["url"]
        image = self.requests.get(image_url).content

        self.send(f"**{self.author.username}** pocałował **{user.username}**!", files=[("kiss.gif", image)])

    @modules.command(description="Przytula osobe", usage="hug (osoba)", default=True)
    def hug(self, user: User):
        if not has_permission(self):
            raise NoPermission(f"{self.author.id} has no {self.command} permission", self.command)

        if user == self.author:
            raise InvalidArgumentType("user is the same as author", self.commands[self.command], ["user"], "user")

        image_url = self.requests.get("https://nekos.life/api/hug").json()["url"]
        image = self.requests.get(image_url).content

        self.send(f"**{self.author.username}** przytulił **{user.username}**!", files=[("hug.gif", image)])

    @modules.command(description="Pokazuje losowe zdjęcie kota", usage="cat", default=True)
    def cat(self):
        if not has_permission(self):
            raise NoPermission(f"{self.author.id} has no {self.command} permission", self.command)

        image_url = self.requests.get("https://some-random-api.ml/img/cat").json()["link"]
        image = self.requests.get(image_url).content

        self.send(files=[("cat.png", image)])

    @modules.command(description="Pokazuje losowe zdjęcie psa", usage="dog", default=True)
    def dog(self):
        if not has_permission(self):
            raise NoPermission(f"{self.author.id} has no {self.command} permission", self.command)

        image_url = self.requests.get("https://some-random-api.ml/img/dog").json()["link"]
        image = self.requests.get(image_url).content

        self.send(files=[("dog.png", image)])

    @modules.command(description="Pokazuje losowe zdjęcie pandy", usage="panda", default=True)
    def panda(self):
        if not has_permission(self):
            raise NoPermission(f"{self.author.id} has no {self.command} permission", self.command)

        image_url = self.requests.get("https://some-random-api.ml/img/panda").json()["link"]
        image = self.requests.get(image_url).content

        self.send(files=[("panda.png", image)])

    @modules.command(description="Generuje tekst w ascii", usage="ascii (tekst)", default=True)
    def _ascii(self, text):
        if not has_permission(self):
            raise NoPermission(f"{self.author.id} has no {self.command} permission", self.command)

        self.send("```" + pyfiglet.Figlet().renderText(" ".join(self.args)) + "```")

    @modules.command(description="Pokazuje w ilu procentach jest sie gejem", usage="howgay [osoba]", default=True)
    def howgay(self, user: User = None):
        if not has_permission(self):
            raise NoPermission(f"{self.author.id} has no {self.command} permission", self.command)

        user = user or self.author

        random.seed(get_int(self.bot_user, user))
        self.send(f"{user.username} jest gejem w {random.randint(0, 100)}%!")

    @modules.command(description="Wysyła obrazek \"Achievement Get!\"", usage="achievement (tekst)", default=True)
    def achievement(self, text):
        if not has_permission(self):
            raise NoPermission(f"{self.author.id} has no {self.command} permission", self.command)

        self.args = " ".join(self.args)

        if len(self.args) > 23:
            return self.send("Tekst jest za długi (maksymalna długość to 23)")

        polish_chars = {
            "ą": "a",
            "ś": "s",
            "ó": "o",
            "ł": "l",
            "ę": "e",
            "ń": "n",
            "ź": "z",
            "ż": "z",
            "ć": "c"
        }

        text = ""

        for char in self.args:
            if char in polish_chars:
                text += polish_chars[char]
            else:
                text += char

        image = self.requests.get(f"https://minecraftskinstealer.com/achievement/{random.randint(1, 40)}/Achievement+Get%21/{text}").content

        self.send(files=[("achievement.png", image)])

    @modules.command(description="Wysyła tekst w emotkach garfield", usage="garfield (tekst)", default=True)
    def garfield(self, text):
        if not has_permission(self):
            raise NoPermission(f"{self.author.id} has no {self.command} permission", self.command)

        self.args = (" ".join(self.args)).lower()

        if len(self.args) > 100:
            return self.send("Tekst jest za długi (maksymalna długość to 100)")

        other = {
            "ą": "a",
            "ś": "s",
            "ó": "o",
            "ł": "l",
            "ę": "e",
            "ń": "n",
            "ź": "z",
            "ż": "z",
            "ć": "c"
        }

        text = ""

        for letter in self.args:
            if ("garfield_" + letter in arrays.emotes) or (letter in other):
                if letter in other:
                    letter = other[letter]
                letter = "garfield_" + letter
                text += f"<:{letter}:{arrays.emotes[letter]}>"
            elif letter in ["`", "\\"]:
                text += ""
            elif letter == " ":
                text += f"<:space:{arrays.emotes[' ']}>"
            else:
                text += letter

        self.send(text)

    @modules.event
    def INTERACTION_CREATE(self):
        if ("calc", self.member.id, self.channel.id, self.data["message"]["id"]) in interactions:
            if not self.data["message"]["id"] in results:
                results[self.data["message"]["id"]] = ""

            custom_id = self.data["data"]["custom_id"]
            message_id = self.data["message"]["id"]

            if "=" in results[message_id]:
                results[message_id] = ""

            if custom_id == "leftbracket":
                results[message_id] += "("
            elif custom_id == "rightbracket":
                results[message_id] += ")"
            elif custom_id == "power":
                results[message_id] += "**"
            elif custom_id == "percent":
                results[message_id] += "%"
            elif custom_id == "backspace":
                results[message_id] = results[message_id][:-1]
            elif custom_id == "clear":
                results[message_id] = ""
            elif custom_id == "divide":
                results[message_id] += "/"
            elif custom_id == "multiply":
                results[message_id] += "*"
            elif custom_id == "minus":
                results[message_id] += "-"
            elif custom_id == "dot":
                results[message_id] += "."
            elif custom_id == "equal":
                try:
                    result = eval(results[message_id])
                    if type(result) == float:
                        result = round(result, 2)
                    results[message_id] += "=" + str(result)
                except:
                    if results[message_id] == "/0":
                        results[message_id] = "KABOOM!"
                    else:
                        results[message_id] = ""
            elif custom_id == "add":
                results[message_id] += "+"
            elif custom_id == "0":
                if not (results[message_id][0] == "0" and len(results[message_id]) == 1):
                    results[message_id] += "0"
            else:
                results[message_id] += custom_id

            self.requests.post(f"https://discord.com/api/v8/interactions/{self.data['id']}/{self.data['token']}/callback", json={
                "type": 7,
                "data": {
                    "content": f"```{results[message_id] if results[message_id] else '0'}```{'https://imgur.com/a/N19WxP4' if results[message_id] == 'KABOOM!' else ''}",
                    "components" if results[message_id] == "KABOOM!" else None: []
                }
            })

    @modules.command(description="Kalkulator", usage="calc", default=True)
    def calc(self):
        if not has_permission(self):
            raise NoPermission(f"{self.author.id} has no {self.command} permission", self.command)

        components = Components(
            Row(
                Button("x\u02b8", style=Styles.Gray, custom_id="power"),
                Button("%", style=Styles.Gray, custom_id="percent"),
                Button("<-", style=Styles.Gray, custom_id="backspace"),
                Button("C", style=Styles.Red, custom_id="clear")
            ),
            Row(
                Button("7", style=Styles.Gray, custom_id="7"),
                Button("8", style=Styles.Gray, custom_id="8"),
                Button("9", style=Styles.Gray, custom_id="9"),
                Button("/", style=Styles.Gray, custom_id="divide"),
                Button("(", style=Styles.Gray, custom_id="leftbracket")
            ),
            Row(
                Button("4", style=Styles.Gray, custom_id="4"),
                Button("5", style=Styles.Gray, custom_id="5"),
                Button("6", style=Styles.Gray, custom_id="6"),
                Button("*", style=Styles.Gray, custom_id="multiply"),
                Button(")", style=Styles.Gray, custom_id="rightbracket")
            ),
            Row(
                Button("1", style=Styles.Gray, custom_id="1"),
                Button("2", style=Styles.Gray, custom_id="2"),
                Button("3", style=Styles.Gray, custom_id="3"),
                Button("-", style=Styles.Gray, custom_id="minus")
            ),
            Row(
                Button("0", style=Styles.Gray, custom_id="0"),
                Button(".", style=Styles.Gray, custom_id="dot"),
                Button("=", style=Styles.Blue, custom_id="equal"),
                Button("+", style=Styles.Gray, custom_id="add")
            )
        )

        msg = self.send("```0```", components=components)

        msg = msg.json()
        interactions.append(("calc", self.author.id, self.channel.id, msg["id"]))

    @modules.command(description="Ukrywa tekst w tekście", usage="encode (tekst wyświetlany) | (tekst ukryty)", default=True)
    def encode(self, text):
        if not has_permission(self):
            raise NoPermission(f"{self.author.id} has no {self.command} permission", self.command)

        self.args = " ".join(self.args).lower().split(" | ")

        text = self.args[0][0]

        other = {
            "ą": "a",
            "ś": "s",
            "ó": "o",
            "ł": "l",
            "ę": "e",
            "ń": "n",
            "ź": "z",
            "ż": "z",
            "ć": "c"
        }

        for char in self.args[1]:
            if char in other:
                self.args[1] = self.args[1].replace(char, other[char])

        for char in self.args[1]:
            if char in arrays._characters:
                text += arrays._characters[char] + "\u200f"

        text += self.args[0][1:]

        self.send("`" + text + "`")

    @modules.command(description="Pokazuje ukryty tekst", usage="decode (tekst)", default=True)
    def decode(self, text):
        if not has_permission(self):
            raise NoPermission(f"{self.author.id} has no {self.command} permission", self.command)

        self.args = " ".join(self.args)

        text = ""
        letter = ""
        chars = {value:key for key, value in arrays._characters.items()}

        for char in self.args:
            if char in chars or char == "\u200f":
                if char == "\u200f":
                    text += chars[letter]
                    letter = ""
                else:
                    letter += char

        if not text:
            return self.send("W tej wiadomości nie ma ukrytego tekstu")

        self.send("`" + text + "`")

    @modules.command(description="\"nie widać mnie\" mem z poligonu", usage="cantseeme [tekst/osoba/obrazek/url]", default=True)
    def cantseeme(self, text = None):
        if not has_permission(self):
            raise NoPermission(f"{self.author.id} has no {self.command} permission", self.command)

        formats = ("image/png", "image/jpeg", "image/gif", "image/webp")

        if not text and not self.data["attachments"]:
            self.mentions.append(self.author)

        if self.mentions:
            message_type = "image"
            content = self.requests.get(self.mentions[0].avatar_url).content
            open("images/image.png", "wb").write(content)

        elif self.data["attachments"]:
            req = self.requests.get(self.data["attachments"][0]["url"])
            message_type = "text"
            if req.headers["content-type"] in formats:
                message_type = "image"
                open("images/image.png", "wb").write(req.content)

        elif text and text.startswith(("https://", "http://")):
            req = self.requests.get(text)
            message_type = "text"
            if req.headers["content-type"] in formats:
                message_type = "image"
                open("images/image.png", "wb").write(req.content)

        elif len(self.args) >= 1:
            message_type = "text"

        elif not self.args:
            message_type = "image"
            content = self.requests.get(self.author.avatar_url).content
            open("images/image.png", "wb").write(content)

        krzak = Image.open("images/krzak.png")
        image = Image.open("images/image.png")

        if message_type == "text":
            self.args = " ".join(self.args)
            center = [round(krzak.size[0] / 2) - 50, round(krzak.size[1] / 2) - 60]
            if len(self.args) > 15:
                new_args = ""
                x = 0
                for char in self.args:
                    if x == 16:
                        new_args += "\n"
                        x = 0

                    new_args += char
                    x += 1

                self.args = new_args

            draw = ImageDraw.Draw(krzak)
            font = ImageFont.truetype("fonts/arial.ttf", 30)

            center = (round(center[0]), round(center[1]))

            draw.text(center, self.args, font=font)

        elif message_type == "image":
            width, height = image.size
            if width > 150:
                width = 150
            if height > 100:
                height = 100

            image.thumbnail((width, height))

            center = (round(krzak.size[0] / 2) - round(image.size[0] / 2), round(krzak.size[1] / 2) - round(image.size[1] / 2) - 30)
            krzak.paste(image, center)
            
        krzak.save("images/cantseeme.png")
        
        self.send(files=[("cantseeme.png", open("images/cantseeme.png", "rb"))])

    @modules.command(description="Wysyła zatęczowany avatar", usage="gay [osoba]", default=True)
    def gay(self, user: User = None):
        if not has_permission(self):
            raise NoPermission(f"{self.author.id} has no {self.command} permission", self.command)

        user = user or self.author

        content = self.requests.get(user.avatar_url).content
        open("images/image.png", "wb").write(content)

        image = Image.open("images/image.png").convert("RGBA")
        lgbt = Image.open("images/lgbt.png").convert("RGBA")
        
        image = ImageOps.fit(image, (512, 512))
        lgbt = ImageOps.fit(lgbt, (512, 512))

        mask = Image.new("L", (512, 512), 128)

        avatar = Image.composite(image, lgbt, mask)
        avatar.save("images/gay.png")

        self.send(files=[("gay.png", open("images/gay.png", "rb"))])

    @modules.command(description="Wysyła losowego mema z jbzd", usage="meme", default=True)
    def meme(self):
        if not has_permission(self):
            raise NoPermission(f"{self.author.id} has no {self.command} permission", self.command)

        if not self.channel.nsfw:
            return self.send("Kanał nie jest nsfw")

        memes = []

        while not memes:
            memes_page = self.requests.get(f"https://jbzd.com.pl/str/{random.randint(1, 235)}").content
            memes_soup = BeautifulSoup(memes_page, "lxml")

            memes = memes_soup.find_all("img", {"class": "article-image"})
            memes = [meme["src"] for meme in memes]

        self.send(random.choice(memes))

    @modules.command(description="Pokazuje informacje o użytkowniku", usage="userinfo [osoba]", default=True)
    def userinfo(self, user: find_working(Member, User) = None):
        if not has_permission(self):
            raise NoPermission(f"{self.author.id} has no {self.command} permission", self.command)

        user = user or self.author

        embed = Embed(title=f"Informacje o {user.username}{' (bot)' if user.bot else ''}:", color=0xe74c3c)
        embed.set_thumbnail(url=user.avatar_url)

        embed.add_field(name="ID:", value=user.id)
        embed.add_field(name="Nick z tagiem:", value=user.user)
        if isinstance(user, Member):
            if user.roles[:-1]:
                embed.add_field(name="Role:", value=", ".join([role.name for role in user.roles][:-1]))
            embed.add_field(name="Dołączył na serwer:", value=f"<t:{int(user.joined_at.timestamp())}:F>")
        embed.add_field(name="Utworzył konto:" if not user.bot else "Stworzony dnia:", value=f"<t:{int(user.created_at.timestamp())}:F>")
        if user.public_flags:
            embed.add_field(name="Odznaki:", value=", ".join([f"<:{flag}:{arrays.flags[flag]}>" for flag in user.public_flags]))
        embed.add_field(name="Avatar:", value=f"[link]({user.avatar_url})")
        if user.bot:
            embed.add_field(name="Zaproszenie:", value=f"[link](https://discord.com/oauth2/authorize?client_id={user.id}&scope=bot)")

        self.send(embed=embed)

    @modules.command(description="Pokazuje informacje o serwerze", usage="serverinfo", default=True)
    def serverinfo(self):
        if not has_permission(self):
            raise NoPermission(f"{self.author.id} has no {self.command} permission", self.command)

        embed = Embed(title=f"Informacje o {self.guild.name}:", color=0xe74c3c)
        embed.set_thumbnail(url=self.guild.icon_url)

        embed.add_field(name="Właściciel:", value=f"{self.guild.owner.mention} ({self.guild.owner_id})")
        embed.add_field(name="ID:", value=self.guild.id)
        embed.add_field(name="Ilość osób:", value=self.guild.member_count)
        embed.add_field(name="Ilość kanałów:", value=len(self.guild.channels))
        embed.add_field(name="Ilość ról:", value=len(self.guild.roles))
        embed.add_field(name="Ilość emotek:", value=len(self.guild.emojis))
        embed.add_field(name="Został stworzony:", value=f"<t:{int(self.guild.created_at.timestamp())}:F>")
        embed.add_field(name="Boosty:", value=f"{self.guild.boosts} boosty / {self.guild.level} poziom")
        if self.guild.vanity_url:
            embed.add_field(name="Własny link:", value=f"discord.gg/{self.guild.vanity_url}")
        embed.add_field(name="Ikona:", value=f"[link]({self.guild.icon_url})")
        if self.guild.banner:
            embed.add_field(name="Banner:", value=f"[link]({self.guild.banner_url})")
            embed.set_image(url=self.guild.banner_url)

        self.send(embed=embed)

    @modules.command(description="\U0001F633", usage="dick [osoba]", default=True)
    def dick(self, user: User = None):
        if not has_permission(self):
            raise NoPermission(f"{self.author.id} has no {self.command} permission", self.command)

        user = user or self.author

        random.seed(get_int(self.bot_user, user))
        self.send(f"Kuktas {user.username}\n8{'=' * random.randint(1, 20)}D")
