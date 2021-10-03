from lib import modules
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
from lib.components import *
import threading

@modules.module
class Fun:
    def __init__(self, bot, discord):
        self.bot = bot
        self.discord = discord
        self.ustawione_kurwa = {
            ("ship", "636096693712060416", "290881759732563982"): 100,
            ("howgay", "290881759732563982"): 100,
            ("howgay", "746038046310531084c"): 100,
            ("howgay", "264905890824585216"): 10,
            ("howgay", "327899255249436672"): 5,
            ("howgay", "563718132863074324"): 98,
            ("howgay", "634766934486810624"): 100,
            ("dick", "264905890824585216"): 20,
            ("dick", "327899255249436672"): 19,
        }

    @modules.command(description="Losuje liczbe", usage="rnumber (od) (do)", default=True)
    def rnumber(self, ctx, _from: int, to: int):
        if not has_permission(ctx):
            raise NoPermission(f"{ctx.author.id} has no {ctx.command} permission", ctx.command)
        
        ctx.send(random.randint(_from, to))

    @modules.command(description="Losuje tekst z podanych", usage="rchoice (a) | (b) | [c] itd.", default=True)
    def rchoice(self, ctx, args):
        if not has_permission(ctx):
            raise NoPermission(f"{ctx.author.id} has no {ctx.command} permission", ctx.command)

        ctx.args = " ".join(ctx.args)
        ctx.args = ctx.args.split(" | ")

        if not len(ctx.ctx) >= 2:
            return ctx.send("Podaj chociaż więcej niż 2 argumenty")

        ctx.send(random.choice(ctx.args))

    @modules.command(description="Pokazuje avatar", usage="avatar [osoba]", default=True)
    def avatar(self, ctx, user: User = None):
        if not has_permission(ctx):
            raise NoPermission(f"{ctx.author.id} has no {ctx.command} permission", ctx.command)

        user = user or ctx.author
        image = ctx.requests.get(user.avatar_url).content

        ctx.send(files=[("avatar.png", image)])

    @modules.command(description="Pokazuje w ilu procentach osoby sie kochają", usage="ship (osoba) [osoba]", default=True)
    def ship(self, ctx, user: User, user2: User = None):
        if not has_permission(ctx):
            raise NoPermission(f"{ctx.author.id} has no {ctx.command} permission", ctx.command)

        if not user2:
            user2 = user
            user = ctx.author

        if user == user2:
            raise InvalidArgumentType("user is the same as user2", ctx.commands[ctx.command], ["user", "user2"], "user2")

        open("images/member1.png", "wb").write(ctx.requests.get(user.avatar_url).content)
        open("images/member2.png", "wb").write(ctx.requests.get(user2.avatar_url).content)
        
        para = Image.open("images/para.png").convert("RGBA")
        member1 = Image.open("images/member1.png").convert("RGBA")
        member2 = Image.open("images/member2.png").convert("RGBA")

        member1 = ImageOps.fit(member1, (300, 300))
        member2 = ImageOps.fit(member2, (300, 300))
        
        para.paste(member1, (360, 250), member1)
        para.paste(member2, (890, 180), member2)
        
        para.save("images/ship.png")

        if ("ship", user.id, user2.id) in self.ustawione_kurwa:
            percent = self.ustawione_kurwa[("ship", user.id, user2.id)]
        elif ("ship", user2.id, user.id) in self.ustawione_kurwa:
            percent = self.ustawione_kurwa[("ship", user2.id, user.id)]
        else:
            percent = get_int(user, user2)

        ctx.send(f"**{user.username}** + **{user2.username}** = **{user.username[:round(len(user.username) / 2)].lower()}{user2.username[round(len(user2.username) / 2):].lower()}**\nIch miłość jest równa **{percent}%**!", files=[("ship.png", open("images/ship.png", "rb"))])

    @modules.command(description="Uderza osobe", usage="slap (osoba)", default=True)
    def slap(self, ctx, user: User):
        if not has_permission(ctx):
            raise NoPermission(f"{ctx.author.id} has no {ctx.command} permission", ctx.command)

        if user == ctx.author:
            raise InvalidArgumentType("user is the same as author", ctx.commands[ctx.command], ["user"], "user")

        image_url = ctx.requests.get("https://nekos.life/api/v2/img/slap").json()["url"]
        image = ctx.requests.get(image_url).content

        ctx.send(f"**{ctx.author.username}** uderzył **{user.username}**!", files=[("slap.gif", image)])

    @modules.command(description="Całuje osobe", usage="kiss (osoba)", default=True)
    def kiss(self, ctx, user: User):
        if not has_permission(ctx):
            raise NoPermission(f"{ctx.author.id} has no {ctx.command} permission", ctx.command)

        if user == ctx.author:
            raise InvalidArgumentType("user is the same as author", ctx.commands[ctx.command], ["user"], "user")

        image_url = ctx.requests.get("https://nekos.life/api/kiss").json()["url"]
        image = ctx.requests.get(image_url).content

        ctx.send(f"**{ctx.author.username}** pocałował **{user.username}**!", files=[("kiss.gif", image)])

    @modules.command(description="Przytula osobe", usage="hug (osoba)", default=True)
    def hug(self, ctx, user: User):
        if not has_permission(ctx):
            raise NoPermission(f"{ctx.author.id} has no {ctx.command} permission", ctx.command)

        if user == ctx.author:
            raise InvalidArgumentType("user is the same as author", ctx.commands[ctx.command], ["user"], "user")

        image_url = ctx.requests.get("https://nekos.life/api/hug").json()["url"]
        image = ctx.requests.get(image_url).content

        ctx.send(f"**{ctx.author.username}** przytulił **{user.username}**!", files=[("hug.gif", image)])

    @modules.command(description="Pokazuje losowe zdjęcie kota", usage="cat", default=True)
    def cat(self, ctx):
        if not has_permission(ctx):
            raise NoPermission(f"{ctx.author.id} has no {ctx.command} permission", ctx.command)

        image_url = ctx.requests.get("https://some-random-api.ml/img/cat").json()["link"]
        image = ctx.requests.get(image_url).content

        ctx.send(files=[("cat.png", image)])

    @modules.command(description="Pokazuje losowe zdjęcie psa", usage="dog", default=True)
    def dog(self, ctx):
        if not has_permission(ctx):
            raise NoPermission(f"{ctx.author.id} has no {ctx.command} permission", ctx.command)

        image_url = ctx.requests.get("https://some-random-api.ml/img/dog").json()["link"]
        image = ctx.requests.get(image_url).content

        ctx.send(files=[("dog.png", image)])

    @modules.command(description="Pokazuje losowe zdjęcie pandy", usage="panda", default=True)
    def panda(self, ctx):
        if not has_permission(ctx):
            raise NoPermission(f"{ctx.author.id} has no {ctx.command} permission", ctx.command)

        image_url = ctx.requests.get("https://some-random-api.ml/img/panda").json()["link"]
        image = ctx.requests.get(image_url).content

        ctx.send(files=[("panda.png", image)])

    @modules.command(description="Generuje tekst w ascii", usage="ascii (tekst)", default=True)
    def ascii(self, ctx, text):
        if not has_permission(ctx):
            raise NoPermission(f"{ctx.author.id} has no {ctx.command} permission", ctx.command)

        ctx.send("```" + pyfiglet.Figlet().renderText(" ".join(ctx.args)) + "```")

    @modules.command(description="Pokazuje w ilu procentach jest sie gejem", usage="howgay [osoba]", default=True)
    def howgay(self, ctx, user: User = None):
        if not has_permission(ctx):
            raise NoPermission(f"{ctx.author.id} has no {ctx.command} permission", ctx.command)

        user = user or ctx.author

        if ("howgay", user.id) in self.ustawione_kurwa:
            percent = self.ustawione_kurwa[("howgay", user.id)]
        else:
            percent = get_int(ctx.bot_user, user)

        ctx.send(f"{user.username} jest gejem w {percent}%!")

    @modules.command(description="Wysyła obrazek \"Achievement Get!\"", usage="achievement (tekst)", default=True)
    def achievement(self, ctx, text):
        if not has_permission(ctx):
            raise NoPermission(f"{ctx.author.id} has no {ctx.command} permission", ctx.command)

        ctx.args = " ".join(ctx.args)

        if len(ctx.args) > 23:
            return ctx.send("Tekst jest za długi (maksymalna długość to 23)")

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

        for char in ctx.args:
            if char in polish_chars:
                text += polish_chars[char]
            else:
                text += char

        image = ctx.requests.get(f"https://minecraftskinstealer.com/achievement/{random.randint(1, 40)}/Achievement+Get%21/{text}").content

        ctx.send(files=[("achievement.png", image)])

    @modules.command(description="Wysyła tekst w emotkach garfield", usage="garfield (tekst)", default=True)
    def garfield(self, ctx, text):
        if not has_permission(ctx):
            raise NoPermission(f"{ctx.author.id} has no {ctx.command} permission", ctx.command)

        ctx.args = (" ".join(ctx.args)).lower()

        if len(ctx.args) > 100:
            return ctx.send("Tekst jest za długi (maksymalna długość to 100)")

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

        for letter in ctx.args:
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

        ctx.send(text)

    @modules.command(description="Kalkulator", usage="calc", default=True)
    def calc(self, ctx):
        if not has_permission(ctx):
            raise NoPermission(f"{ctx.author.id} has no {ctx.command} permission", ctx.command)

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

        msg = ctx.send("```0```", components=components).json()

        if not hasattr(ctx, "interactions"):
            ctx.interactions = []

        ctx.interactions.append(("calc", ctx.author.id, ctx.channel.id, msg["id"]))

    @modules.command(description="Ukrywa tekst w tekście", usage="encode (tekst wyświetlany) | (tekst ukryty)", default=True)
    def encode(self, ctx, text):
        if not has_permission(ctx):
            raise NoPermission(f"{ctx.author.id} has no {ctx.command} permission", ctx.command)

        ctx.args = " ".join(ctx.args).lower().split(" | ")

        text = ctx.args[0][0]

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

        for char in ctx.args[1]:
            if char in other:
                ctx.args[1] = ctx.args[1].replace(char, other[char])

        for char in ctx.args[1]:
            if char in arrays._characters:
                text += arrays._characters[char] + "\u200f"

        text += ctx.args[0][1:]

        ctx.send("`" + text + "`")

    @modules.command(description="Pokazuje ukryty tekst", usage="decode (tekst)", default=True)
    def decode(self, ctx, text):
        if not has_permission(ctx):
            raise NoPermission(f"{ctx.author.id} has no {ctx.command} permission", ctx.command)

        ctx.args = " ".join(ctx.args)

        text = ""
        letter = ""
        chars = {value:key for key, value in arrays._characters.items()}

        for char in ctx.args:
            if char in chars or char == "\u200f":
                if char == "\u200f":
                    text += chars[letter]
                    letter = ""
                else:
                    letter += char

        if not text:
            return ctx.send("W tej wiadomości nie ma ukrytego tekstu")

        ctx.send("`" + text + "`")

    @modules.command(description="\"nie widać mnie\" mem z poligonu", usage="cantseeme [tekst/osoba/obrazek/url]", default=True)
    def cantseeme(self, ctx, text = None):
        if not has_permission(ctx):
            raise NoPermission(f"{ctx.author.id} has no {ctx.command} permission", ctx.command)

        formats = ("image/png", "image/jpeg", "image/gif", "image/webp")

        if not text and not ctx.data["attachments"]:
            ctx.mentions.append(ctx.author)

        if ctx.mentions:
            message_type = "image"
            content = ctx.requests.get(ctx.mentions[0].avatar_url).content
            open("images/image.png", "wb").write(content)

        elif ctx.data["attachments"]:
            req = ctx.requests.get(ctx.data["attachments"][0]["url"])
            message_type = "text"
            if req.headers["content-type"] in formats:
                message_type = "image"
                open("images/image.png", "wb").write(req.content)

        elif text and text.startswith(("https://", "http://")):
            req = ctx.requests.get(text)
            message_type = "text"
            if req.headers["content-type"] in formats:
                message_type = "image"
                open("images/image.png", "wb").write(req.content)

        elif len(ctx.args) >= 1:
            message_type = "text"

        elif not ctx.args:
            message_type = "image"
            content = ctx.requests.get(ctx.author.avatar_url).content
            open("images/image.png", "wb").write(content)

        krzak = Image.open("images/krzak.png")
        image = Image.open("images/image.png")

        if message_type == "text":
            ctx.args = " ".join(ctx.args)
            center = [round(krzak.size[0] / 2) - 50, round(krzak.size[1] / 2) - 60]
            if len(ctx.args) > 15:
                new_args = ""
                x = 0
                for char in ctx.args:
                    if x == 16:
                        new_args += "\n"
                        x = 0

                    new_args += char
                    x += 1

                ctx.args = new_args

            draw = ImageDraw.Draw(krzak)
            font = ImageFont.truetype("fonts/arial.ttf", 30)

            center = (round(center[0]), round(center[1]))

            draw.text(center, ctx.args, font=font)

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
        
        ctx.send(files=[("cantseeme.png", open("images/cantseeme.png", "rb"))])

    @modules.command(description="Wysyła zatęczowany avatar", usage="gay [osoba]", default=True)
    def gay(self, ctx, user: User = None):
        if not has_permission(ctx):
            raise NoPermission(f"{ctx.author.id} has no {ctx.command} permission", ctx.command)

        user = user or ctx.author

        content = ctx.requests.get(user.avatar_url).content
        open("images/image.png", "wb").write(content)

        image = Image.open("images/image.png").convert("RGBA")
        lgbt = Image.open("images/lgbt.png").convert("RGBA")
        
        image = ImageOps.fit(image, (512, 512))
        lgbt = ImageOps.fit(lgbt, (512, 512))

        mask = Image.new("L", (512, 512), 128)

        avatar = Image.composite(image, lgbt, mask)
        avatar.save("images/gay.png")

        ctx.send(files=[("gay.png", open("images/gay.png", "rb"))])

    @modules.command(description="Wysyła losowego mema z jbzd", usage="meme", aliases=["mem"], default=True)
    def meme(self, ctx):
        if not has_permission(ctx):
            raise NoPermission(f"{ctx.author.id} has no {ctx.command} permission", ctx.command)

        if not ctx.channel.nsfw:
            return ctx.send("Kanał nie jest nsfw")

        memes = []

        while not memes:
            memes_page = ctx.requests.get(f"https://jbzd.com.pl/str/{random.randint(1, 235)}").content
            memes_soup = BeautifulSoup(memes_page, "lxml")

            memes = memes_soup.find_all("img", {"class": "article-image"})
            memes = [meme["src"] for meme in memes]

        ctx.send(random.choice(memes))

    @modules.command(description="Pokazuje informacje o użytkowniku", usage="userinfo [osoba]", aliases=["ui", "user", "whois", "cotozacwel", "kimtykurwajestes", "ktoto"], default=True)
    def userinfo(self, ctx, user: find_working(Member, User) = None):
        if not has_permission(ctx):
            raise NoPermission(f"{ctx.author.id} has no {ctx.command} permission", ctx.command)

        user = user or ctx.author

        embed = Embed(title=f"Informacje o {user.username}{' (bot)' if user.bot else ''}:", color=0xe74c3c)
        embed.set_thumbnail(url=user.avatar_url)

        embed.add_field(name="ID:", value=user.id)
        embed.add_field(name="Nick z tagiem:", value=user.user)
        if isinstance(user, Member):
            if user.nick:
                embed.add_field(name="Nick na serwerze:", value=user.nick)
            if user.roles[:-1]:
                embed.add_field(name="Role:", value=", ".join([role.name for role in user.roles][:-1]))
            embed.add_field(name="Dołączył na serwer:", value=f"<t:{int(user.joined_at.timestamp())}:F>")
        embed.add_field(name="Utworzył konto:" if not user.bot else "Stworzony dnia:", value=f"<t:{int(user.created_at.timestamp())}:F>")
        if user.public_flags:
            embed.add_field(name="Odznaki:", value=", ".join([f"<:{flag}:{arrays.flags[flag]}>" for flag in user.public_flags]))
        embed.add_field(name="Avatar:", value=f"[link]({user.avatar_url})")
        if user.bot:
            embed.add_field(name="Zaproszenie:", value=f"[link](https://discord.com/oauth2/authorize?client_id={user.id}&scope=bot)")

        ctx.send(embed=embed)

    @modules.command(description="Pokazuje informacje o serwerze", usage="serverinfo", aliases=["si"], default=True)
    def serverinfo(self, ctx):
        if not has_permission(ctx):
            raise NoPermission(f"{ctx.author.id} has no {ctx.command} permission", ctx.command)

        embed = Embed(title=f"Informacje o {ctx.guild.name}:", color=0xe74c3c)
        embed.set_thumbnail(url=ctx.guild.icon_url)

        embed.add_field(name="Właściciel:", value=f"{ctx.guild.owner.mention} ({ctx.guild.owner_id})")
        embed.add_field(name="ID:", value=ctx.guild.id)
        embed.add_field(name="Ludzie:", value=ctx.guild.member_count)
        embed.add_field(name="Kanały:", value=len(ctx.guild.channels), inline=True)
        embed.add_field(name="Role:", value=len(ctx.guild.roles), inline=True)
        embed.add_field(name="Emotki:", value=len(ctx.guild.emojis), inline=True)
        embed.add_field(name="Został stworzony:", value=f"<t:{int(ctx.guild.created_at.timestamp())}:F>")
        embed.add_field(name="Boosty:", value=ctx.guild.boosts, inline=True)
        embed.add_field(name="Poziom:", value=ctx.guild.level, inline=True)
        if ctx.guild.vanity_url:
            embed.add_field(name="Własny link:", value=f"discord.gg/{ctx.guild.vanity_url}")
        embed.add_field(name="Ikona:", value=f"[link]({ctx.guild.icon_url})", inline=True)
        if ctx.guild.banner:
            embed.add_field(name="Banner:", value=f"[link]({ctx.guild.banner_url})", inline=True)
            embed.set_image(url=ctx.guild.banner_url)

        ctx.send(embed=embed)

    @modules.command(description="\U0001F633", usage="dick [osoba]", default=True)
    def dick(self, ctx, user: User = None):
        if not has_permission(ctx):
            raise NoPermission(f"{ctx.author.id} has no {ctx.command} permission", ctx.command)

        user = user or ctx.author

        if ("dick", user.id) in self.ustawione_kurwa:
            percent = self.ustawione_kurwa[("dick", user.id)] * 5
        else:
            percent = get_int(ctx.bot_user, user)

        ctx.send(f"Kuktas {user.username}\n8{'=' * int(percent / 5)}D")
