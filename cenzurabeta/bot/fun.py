import urllib.parse
import requests
import random
import json
import handler
from PIL import Image, ImageDraw, ImageFont
import os
import pyfiglet
import functions
import config
import time

def load(gateway, discord):
    @gateway.command(description="Wysyła link google", usage="google (zapytanie)", category="Fun", _default=True)
    def google(ctx):
        if not functions.has_permission(ctx):
            return handler.error_handler(ctx, "nopermission", ctx.command)

        ctx.args = " ".join(ctx.args)
        if not ctx.args:
            return handler.error_handler(ctx, "arguments", "google (zapytanie)")

        discord.create_message(ctx.data["channel_id"], {
            "embed": {
                "color": 0xe74c3c,
                "fields": [
                    {
                        "name": "Twój wynik wyszukiwania:",
                        "value": f"[{ctx.args}](https://google.com/search?q={urllib.parse.quote_plus(ctx.args)})",
                        "inline": False
                    }
                ],
                "footer": {
                    "text": f"Wywołane przez {ctx.data['author']['id']}"
                }
            }
        })

    @gateway.command(description="Orzeł czy reszka", usage="coinflip", category="Fun", _default=True)
    def coinflip(ctx):
        if not functions.has_permission(ctx):
            return handler.error_handler(ctx, "nopermission", ctx.command)

        discord.create_message(ctx.data["channel_id"], {
            "content": random.choice(["Orzeł", "Reszka"])
        })

    @gateway.command(description="Losuje liczbe", usage="rnumber (od) (do)", category="Fun", _default=True)
    def rnumber(ctx):
        if not functions.has_permission(ctx):
            return handler.error_handler(ctx, "nopermission", ctx.command)

        if not len(ctx.args) == 2:
            return handler.error_handler(ctx, "arguments", "rnumber (od) (do)")

        ctx.args = list(map(lambda x: int(x), ctx.args))

        discord.create_message(ctx.data["channel_id"], {
            "content": random.randint(ctx.args[0], ctx.args[1])
        })

    @gateway.command(description="Losuje tekst z podanych", usage="rchoice (a) | (b) | [c] itd.", category="Fun", _default=True)
    def rchoice(ctx):
        if not functions.has_permission(ctx):
            return handler.error_handler(ctx, "nopermission", ctx.command)

        ctx.args = " ".join(ctx.args)
        ctx.args = ctx.args.split(" | ")

        if not len(ctx.args) >= 2:
            return handler.error_handler(ctx, "arguments", "rchoice (a) | (b) | [c] itd.")

        discord.create_message(ctx.data["channel_id"], {
            "embed": {
                "description": random.choice(ctx.args),
                "color": 0xe74c3c,
                "footer": {
                    "text": f"Wywołane przez {ctx.data['author']['id']}"
                } 
            }
        })

    @gateway.command(description="Pokazuje avatar", usage="avatar [osoba]", category="Fun", _default=True)
    def avatar(ctx):
        if not functions.has_permission(ctx):
            return handler.error_handler(ctx, "nopermission", ctx.command)

        if not ctx.data["mentions"]:
            user = ctx.data["author"]["id"], ctx.data["author"]["avatar"]
        else:
            user = ctx.data["mentions"][0]["id"], ctx.data["mentions"][0]["avatar"]

        image = requests.get(f"https://cdn.discordapp.com/avatars/{user[0]}/{user[1]}.png?size=2048").content

        discord.create_message(ctx.data["channel_id"], None, {
            "file": ("avatar.png", image, "multipart/form-data")
        })

    @gateway.command(description="Pokazuje w ilu procentach osoby sie kochają", usage="love (osoba) [osoba]", category="Fun", _default=True)
    def love(ctx):
        if not functions.has_permission(ctx):
            return handler.error_handler(ctx, "nopermission", ctx.command)

        if len(ctx.data["mentions"]) == 1:
            me = ctx.data["author"]["id"], ctx.data["author"]["avatar"], ctx.data["author"]["username"]
            me_avatar = f"https://cdn.discordapp.com/avatars/{me[0]}/{me[1]}.png?size=2048"
            m = ctx.data["mentions"][0]["id"], ctx.data["mentions"][0]["avatar"], ctx.data["mentions"][0]["username"]
            m_avatar = f"https://cdn.discordapp.com/avatars/{m[0]}/{m[1]}.png?size=2048"
        elif len(ctx.data["mentions"]) == 2:
            me = ctx.data["mentions"][1]["id"], ctx.data["mentions"][1]["avatar"], ctx.data["mentions"][1]["username"]
            me_avatar = f"https://cdn.discordapp.com/avatars/{me[0]}/{me[1]}.png?size=2048"
            m = ctx.data["mentions"][0]["id"], ctx.data["mentions"][0]["avatar"], ctx.data["mentions"][0]["username"]
            m_avatar = f"https://cdn.discordapp.com/avatars/{m[0]}/{m[1]}.png?size=2048"
        else:
            return handler.error_handler(ctx, "arguments", "love (osoba 1) (osoba 2)")

        open("member1.png", "wb").write(requests.get(m_avatar).content)
        open("member2.png", "wb").write(requests.get(me_avatar).content)
        
        para = Image.open("para.png")
        member1 = Image.open("member1.png")
        member2 = Image.open("member2.png")
        
        member1.thumbnail((300, 300))
        member2.thumbnail((300, 300))
        
        para.paste(member1, (360, 250))
        para.paste(member2, (890, 180))
        
        para.save("ship.png")

        discord.create_message(ctx.data["channel_id"], {
            "content": f"**{m[2]}** + **{me[2]}** = **{m[2][:round(len(m[2]) / 2)].lower()}{me[2][round(len(me[2]) / 2):].lower()}**\nIch miłość jest równa **{random.randint(0, 100)}%**!"
        },
        {
            "file": ("ship.png", open("ship.png", "rb"), "multipart/form-data")
        })

        os.remove("member1.png")
        os.remove("member2.png")
        os.remove("ship.png")

    @gateway.command(description="Odpowiada na pytanie", usage="8ball (pytanie)", category="Fun", _default=True)
    def _8ball(ctx):
        if not functions.has_permission(ctx):
            return handler.error_handler(ctx, "nopermission", ctx.command)

        if not ctx.args:
            return handler.error_handler(ctx, "arguments", "8ball (pytanie)")

        discord.create_message(ctx.data["channel_id"], {
            "content": random.choice("Tak, Nie, Możliwe że tak, Możliwe że nie, Możliwe lecz nie wiem, Raczej tak, Raczej nie, Oczywiście że tak, Oczywiście że nie, Na pewno tak, Na pewno nie, Jeszczee jak, Jak najbardziej".split(", "))
        })

    @gateway.command(description="Pokazuje ikone serwera", usage="servericon", category="Fun", _default=True)
    def servericon(ctx):
        if not functions.has_permission(ctx):
            return handler.error_handler(ctx, "nopermission", ctx.command)

        guild = discord.get_guild(ctx.data["guild_id"])

        image = requests.get(f"https://cdn.discordapp.com/icons/{ctx.data['guild_id']}/{guild['icon']}.png?size=2048").content

        discord.create_message(ctx.data["channel_id"], None, {
            "file": ("servericon.png", image, "multipart/form-data")
        })

    @gateway.command(description="Uderza osobe", usage="slap (osoba)", category="Fun", _default=True)
    def slap(ctx):
        if not functions.has_permission(ctx):
            return handler.error_handler(ctx, "nopermission", ctx.command)

        if not len(ctx.data["mentions"]) == 1:
            return handler.error_handler(ctx, "arguments", "slap (osoba)")

        image_url = requests.get("https://nekos.life/api/v2/img/slap").json()["url"]
        image = requests.get(image_url).content

        discord.create_message(ctx.data["channel_id"], {
            "content": f"**{ctx.data['author']['username']}** uderzył **{ctx.data['mentions'][0]['username']}**!"
        },
        {
            "file": ("slap.gif", image, "multipart/form-data")
        })

    @gateway.command(description="Całuje osobe", usage="kiss (osoba)", category="Fun", _default=True)
    def kiss(ctx):
        if not functions.has_permission(ctx):
            return handler.error_handler(ctx, "nopermission", ctx.command)

        if not len(ctx.data["mentions"]) == 1:
            return handler.error_handler(ctx, "arguments", "kiss (osoba)")

        image_url = requests.get("https://nekos.life/api/kiss").json()["url"]
        image = requests.get(image_url).content

        discord.create_message(ctx.data["channel_id"], {
            "content": f"**{ctx.data['author']['username']}** pocałował **{ctx.data['mentions'][0]['username']}**!"
        },
        {
            "file": ("kiss.gif", image, "multipart/form-data")
        })

    @gateway.command(description="Przytula osobe", usage="hug (osoba)", category="Fun", _default=True)
    def hug(ctx):
        if not functions.has_permission(ctx):
            return handler.error_handler(ctx, "nopermission", ctx.command)

        if not len(ctx.data["mentions"]) == 1:
            return handler.error_handler(ctx, "arguments", "hug (osoba)")

        image_url = requests.get("https://nekos.life/api/hug").json()["url"]
        image = requests.get(image_url).content

        discord.create_message(ctx.data["channel_id"], {
            "content": f"**{ctx.data['author']['username']}** przytulił **{ctx.data['mentions'][0]['username']}**!"
        },
        {
            "file": ("hug.gif", image, "multipart/form-data")
        })

    @gateway.command(description="Pokazuje losowe zdjęcie kota", usage="cat", category="Fun", _default=True)
    def cat(ctx):
        if not functions.has_permission(ctx):
            return handler.error_handler(ctx, "nopermission", ctx.command)

        image_url = requests.get("https://some-random-api.ml/img/cat").json()["link"]
        image = requests.get(image_url).content

        discord.create_message(ctx.data["channel_id"], None, {
            "file": ("cat.png", image, "multipart/form-data")
        })

    @gateway.command(description="Pokazuje losowe zdjęcie psa", usage="dog", category="Fun", _default=True)
    def dog(ctx):
        if not functions.has_permission(ctx):
            return handler.error_handler(ctx, "nopermission", ctx.command)

        image_url = requests.get("https://some-random-api.ml/img/dog").json()["link"]
        image = requests.get(image_url).content

        discord.create_message(ctx.data["channel_id"], None, {
            "file": ("dog.png", image, "multipart/form-data")
        })

    @gateway.command(description="Pokazuje losowe zdjęcie pandy", usage="panda", category="Fun", _default=True)
    def panda(ctx):
        if not functions.has_permission(ctx):
            return handler.error_handler(ctx, "nopermission", ctx.command)

        image_url = requests.get("https://some-random-api.ml/img/panda").json()["link"]
        image = requests.get(image_url).content

        discord.create_message(ctx.data["channel_id"], None, {
            "file": ("panda.png", image, "multipart/form-data")
        })

    @gateway.command(description="Generuje tekst w ascii", usage="ascii (tekst)", category="Fun", _default=True)
    def ascii(ctx):
        if not functions.has_permission(ctx):
            return handler.error_handler(ctx, "nopermission", ctx.command)

        if not ctx.args:
            return handler.error_handler(ctx, "arguments", "ascii (tekst)")

        discord.create_message(ctx.data["channel_id"], {
            "content": "```" + pyfiglet.Figlet().renderText(" ".join(ctx.args)) + "```"
        })

    @gateway.command(description="Pokazuje w ilu procentach jest sie gejem", usage="howgay [osoba]", category="Fun", _default=True)
    def howgay(ctx):
        if not functions.has_permission(ctx):
            return handler.error_handler(ctx, "nopermission", ctx.command)

        if not ctx.data["mentions"]:
            user = ctx.data["author"]["username"]
        else:
            user = ctx.data["mentions"][0]["username"]

        discord.create_message(ctx.data["channel_id"], {
            "content": f"{user} jest gejem w {random.randint(0, 100)}%!"
        })

    @gateway.command(description="Wysyła obrazek \"Achievement Get!\"", usage="achievement (tekst)", category="Fun", _default=True)
    def achievement(ctx):
        if not functions.has_permission(ctx):
            return handler.error_handler(ctx, "nopermission", ctx.command)

        ctx.args = " ".join(ctx.args)
        if not ctx.args:
            return handler.error_handler(ctx, "arguments", "achievement (tekst)")
        elif len(ctx.args) > 23:
            return handler.error_handler(ctx, "toolongtext", 23)

        ctx.args = ctx.args.replace(" ", "+").replace("ś", "s").replace("ę", "e").replace("ż", "z").replace("ź", "z").replace("ł", "l").replace("ó", "o").replace("ą", "a").replace("ć", "c").replace("Ś", "S").replace("Ę", "E").replace("Ż", "Z").replace("Ź", "Z").replace("Ł", "L").replace("Ó", "O").replace("Ą", "A").replace("Ć", "C")

        image = requests.get(f"https://minecraftskinstealer.com/achievement/{random.randint(1, 40)}/Achievement+Get%21/{ctx.args}").content

        discord.create_message(ctx.data["channel_id"], None, {
            "file": ("achievement.png", image, "multipart/form-data")
        })

    @gateway.command(description="Wysyła tekst w emotkach garfield", usage="garfield (tekst)", category="Fun", _default=True)
    def garfield(ctx):
        if not functions.has_permission(ctx):
            return handler.error_handler(ctx, "nopermission", ctx.command)

        ctx.args = (" ".join(ctx.args)).lower()
        if not ctx.args:
            return handler.error_handler(ctx, "arguments", "garfield (tekst)")
        elif len(ctx.args) > 100:
            return handler.error_handler(ctx, "toolongtext", 100)

        emotes = {
            "garfield_e": "800427649214054450",
            "garfield_z": "800427648898826263",
            "garfield_d": "800427649226899471",
            "garfield_r": "800427648681377803",
            "garfield_v": "800427648454361159",
            "garfield_c": "800427649037238303",
            "garfield_9": "800427648500105245",
            "garfield_l": "800427649239220284",
            "garfield_8": "800427648332857374",
            "garfield_2": "800427648378732544",
            "garfield_t": "800427648563544064",
            "garfield_u": "800427648664207400",
            "garfield_1": "800427648316080140",
            "garfield_3": "800427648437321728",
            "garfield_4": "800427648119603202",
            "garfield_h": "800427649175650354",
            "garfield_g": "800427649171718184",
            "garfield_f": "800427649214054460",
            "garfield_b": "800427648861077587",
            "garfield_a": "800427648983629846",
            "garfield_7": "800427648332988417",
            "garfield_6": "800427648446758922",
            "garfield_5": "800427648429588550",
            "garfield_i": "800427648810876969",
            "garfield_j": "800427649222443068",
            "garfield_k": "800427648861601824",
            "garfield_m": "800427649225719903",
            "garfield_n": "800427649235288096",
            "garfield_o": "800427649263468554",
            "garfield_p": "800427649012334614",
            "garfield_q": "800427648672202792",
            "garfield_s": "800427649180762162",
            "garfield_w": "800427648626196540",
            "garfield_x": "800427648463011881",
            "garfield_y": "800427649381826610",
            "garfield_0": "800427648508624926",
            " ": "800433791289917470"
        }

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
            if ("garfield_" + letter in emotes) or (letter in other):
                if letter in other:
                    letter = other[letter]
                letter = "garfield_" + letter
                text += f"<:{letter}:{emotes[letter]}>"
            elif letter in ["`", "\\"]:
                text += ""
            elif letter == " ":
                text += f"<:space:{emotes[' ']}>"
            else:
                text += letter

        discord.create_message(ctx.data["channel_id"], {
            "content": text
        })

    @gateway.command(description="Kalkulator", usage="calc (działanie matematyczne)", category="Fun", _default=True)
    def calc(ctx):
        if not functions.has_permission(ctx):
            return handler.error_handler(ctx, "nopermission", ctx.command)

        ctx.args = " ".join(ctx.args)
        allowed = "1234567890+-/*^() "

        if not ctx.args:
            return handler.error_handler(ctx, "arguments", "calc (działanie matematyczne)")

        for letter in ctx.args:
            if not letter in allowed:
                return handler.error_handler(ctx, "arguments", "calc (działanie matematyczne)")

        try:
            result = eval(ctx.args.replace("^", "**"))
        except:
            result = "błąd"

        discord.create_message(ctx.data["channel_id"], {
            "content": result
        })

    _characters = {
        "a": "\u200b",
        "b": "\u200b" * 2,
        "c": "\u200b" * 3,
        "d": "\u200b" * 4,
        "e": "\u200b" * 5,
        "f": "\u200b" * 6,
        "g": "\u200b" * 7,
        "h": "\u200b" * 8,
        "i": "\u200b" * 9,
        "j": "\u200b" * 10,
        "k": "\u200b" * 11,
        "l": "\u200b" * 12,
        "m": "\u200b" * 13,
        "n": "\u200b" * 14,
        "o": "\u200b" * 15,
        "p": "\u200b" * 16,
        "q": "\u200b" * 17,
        "r": "\u200b" * 18,
        "s": "\u200c",
        "t": "\u200c" * 2,
        "u": "\u200c" * 3,
        "v": "\u200c" * 4,
        "w": "\u200c" * 5,
        "x": "\u200c" * 6,
        "y": "\u200c" * 7,
        "z": "\u200c" * 8,
        "1": "\u200d",
        "2": "\u200d" * 2,
        "3": "\u200d" * 3,
        "4": "\u200d" * 4,
        "5": "\u200d" * 5,
        "6": "\u200d" * 6,
        "7": "\u200d" * 7,
        "8": "\u200d" * 8,
        "9": "\u200d" * 9,
        "0": "\u200d" * 10,
        "!": "\u200e",
        "@": "\u200e" * 2,
        "#": "\u200e" * 3,
        "%": "\u200e" * 4,
        "^": "\u200e" * 5,
        "&": "\u200e" * 6,
        "*": "\u200e" * 7,
        "(": "\u200e" * 8,
        ")": "\u200e" * 9,
        "-": "\u200e" * 10,
        "_": "\u200e" * 11,
        "=": "\u200e" * 12,
        "+": "\u200e" * 13,
        "[": "\u200e" * 14,
        "]": "\u200e" * 15,
        "{": "\u200e" * 16,
        "}": "\u200e" * 17,
        ";": "\u200e" * 18,
        "'": "\u200e" * 19,
        ":": "\u200e" * 20,
        "\"": "\u200e" * 21,
        ",": "\u200e" * 22,
        ".": "\u200e" * 23,
        "/": "\u200e" * 24,
        "<": "\u200e" * 25,
        ">": "\u200e" * 26,
        "?": "\u200e" * 27,
        "\\": "\u200e" * 28,
        "|": "\u200e" * 29,
        " ": "\u200e" * 30
    }

    @gateway.command(description="Ukrywa tekst w tekście", usage="encode (tekst wyświetlany) | (tekst ukryty)", category="Fun", _default=True)
    def encode(ctx):
        if not functions.has_permission(ctx):
            return handler.error_handler(ctx, "nopermission", ctx.command)

        ctx.args = " ".join(ctx.args).lower().split(" | ")
        if not len(ctx.args) == 2:
            return handler.error_handler(ctx, "arguments", "encode (tekst wyświetlany) | (tekst ukryty)")

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
            if char in _characters:
                text += _characters[char] + "\u200f"

        text += ctx.args[0][1:]

        discord.create_message(ctx.data["channel_id"], {
            "embed": {
                "title": "Skopiuj tekst poniżej i wpisz decode (wklej tu tekst) aby otrzymać ukryty tekst",
                "description": "```" + text + "```",
                "color": 0xe74c3c,
                "footer": {
                    "text": f"Wywołane przez {ctx.data['author']['id']}"
                }
            }
        })

    @gateway.command(description="Pokazuje ukryty tekst", usage="decode (tekst)", category="Fun", _default=True)
    def decode(ctx):
        if not functions.has_permission(ctx):
            return handler.error_handler(ctx, "nopermission", ctx.command)

        ctx.args = " ".join(ctx.args)
        if not ctx.args:
            return handler.error_handler(ctx, "arguments", "encode (tekst wyświetlany) | (tekst ukryty)")

        text = ""
        letter = ""
        chars = {value:key for key, value in _characters.items()}

        for char in ctx.args:
            if char in chars or char == "\u200f":
                if char == "\u200f":
                    text += chars[letter]
                    letter = ""
                else:
                    letter += char

        if not text:
            return discord.create_message(ctx.data["channel_id"], {
                "content": "W tej wiadomości nie ma ukrytego tekstu"
            })
        
        discord.create_message(ctx.data["channel_id"], {
            "embed": {
                "description": "```" + text + "```",
                "color": 0xe74c3c,
                "footer": {
                    "text": f"Wywołane przez {ctx.data['author']['id']}"
                }
            }
        })

    @gateway.command(description="\"nie widać mnie\" mem z poligonu", usage="cantseeme [tekst/osoba/obrazek/url z obrazkiem]", category="Fun", _default=True)
    def cantseeme(ctx):
        if not functions.has_permission(ctx):
            return handler.error_handler(ctx, "nopermission", ctx.command)

        formats = ("image/png", "image/jpeg", "image/gif", "image/webp")

        if (len(ctx.data["mentions"]) and len(ctx.args)) == 1:
            message_type = "image"
            content = requests.get(f"https://cdn.discordapp.com/avatars/{ctx.data['mentions'][0]['id']}/{ctx.data['mentions'][0]['avatar']}.png?size=2048").content
            open("image.png", "wb").write(content)

        elif len(ctx.data["attachments"]) == 1:
            req = requests.get(ctx.data["attachments"][0]["url"])
            message_type = "text"
            if req.headers["content-type"] in formats:
                message_type = "image"
                open("image.png", "wb").write(req.content)

        elif len(ctx.args) == 1 and ctx.args[0].startswith(("https://", "http://")):
            req = requests.get(ctx.args[0])
            message_type = "text"
            if req.headers["content-type"] in formats:
                message_type = "image"
                open("image.png", "wb").write(req.content)

        elif len(ctx.args) >= 1:
            message_type = "text"

        elif not ctx.args:
            message_type = "image"
            content = requests.get(f"https://cdn.discordapp.com/avatars/{ctx.data['author']['id']}/{ctx.data['author']['avatar']}.png?size=2048").content
            open("image.png", "wb").write(content)

        krzak = Image.open("krzak.png")
        image = Image.open("image.png")

        if message_type == "text":
            ctx.args = " ".join(ctx.args)
            center = [round(krzak.size[0] / 2) - 50, round(krzak.size[1] / 2) - 60]
            if len(ctx.args) > 15:
                i = ""
                for _ in range(3):
                    for char in range(15):
                        i += ctx.args[char]
                        center[0] -= 0.5
                    i += "\n"
                ctx.args = i

            draw = ImageDraw.Draw(krzak)
            font = ImageFont.truetype("arial.ttf", 30)

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
            
        krzak.save("cantseeme.png")

        discord.create_message(ctx.data["channel_id"], None, {
            "file": ("cantseeme.png", open("cantseeme.png", "rb"), "multipart/form-data")
        })
