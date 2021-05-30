import urllib.parse
import random
import json
import handler
from PIL import Image, ImageDraw, ImageFont, ImageOps
import os
import pyfiglet
import functions
import config
import time
from datetime import datetime
import arrays

interactions = []
results = {}

def load(bot, discord):
    @bot.command(description="Pokazuje ping bota", usage="ping", category="Fun", _default=True)
    def ping(ctx):
        if not functions.has_permission(ctx):
            return handler.error_handler(ctx, "nopermission", ctx.command)
            
        ctx.ping[ctx.data["channel_id"]] = {
            "datetime": datetime.now(),
            "ctx": ctx.data,
            "data": {
                "content": """```
       Ping!       Pong!
 0 🏓          |             0
/|   ---------------------  /|\\
/ \\   |                 |   / \\
```bot `{}ms`
gateway `{}ms`"""
            }
        }

        data = {
            "op": 1,
            "d": 251
        }

        data = json.dumps(data)
        ctx.ws.send(data)

    @bot.command(description="Wysyła link google", usage="google (zapytanie)", category="Fun", _default=True)
    def google(ctx):
        if not functions.has_permission(ctx):
            return handler.error_handler(ctx, "nopermission", ctx.command)

        ctx.args = " ".join(ctx.args)
        if not ctx.args:
            return handler.error_handler(ctx, "arguments", "google (zapytanie)")

        discord.create_message(ctx.data["channel_id"], {
            "content": f"https://google.com/search?q={urllib.parse.quote_plus(ctx.args)}"
        })

    @bot.command(description="Orzeł czy reszka", usage="coinflip", category="Fun", _default=True)
    def coinflip(ctx):
        if not functions.has_permission(ctx):
            return handler.error_handler(ctx, "nopermission", ctx.command)

        discord.create_message(ctx.data["channel_id"], {
            "content": random.choice(["Orzeł", "Reszka"])
        })

    @bot.command(description="Losuje liczbe", usage="rnumber (od) (do)", category="Fun", _default=True)
    def rnumber(ctx):
        if not functions.has_permission(ctx):
            return handler.error_handler(ctx, "nopermission", ctx.command)

        if not len(ctx.args) == 2:
            return handler.error_handler(ctx, "arguments", "rnumber (od) (do)")

        ctx.args = list(map(lambda x: int(x), ctx.args))

        discord.create_message(ctx.data["channel_id"], {
            "content": random.randint(ctx.args[0], ctx.args[1])
        })

    @bot.command(description="Losuje tekst z podanych", usage="rchoice (a) | (b) | [c] itd.", category="Fun", _default=True)
    def rchoice(ctx):
        if not functions.has_permission(ctx):
            return handler.error_handler(ctx, "nopermission", ctx.command)

        ctx.args = " ".join(ctx.args)
        ctx.args = ctx.args.split(" | ")

        if not len(ctx.args) >= 2:
            return handler.error_handler(ctx, "arguments", "rchoice (a) | (b) | [c] itd.")

        discord.create_message(ctx.data["channel_id"], {
            "content": random.choice(ctx.args)
        })

    @bot.command(description="Pokazuje avatar", usage="avatar [osoba]", category="Fun", _default=True)
    def avatar(ctx):
        if not functions.has_permission(ctx):
            return handler.error_handler(ctx, "nopermission", ctx.command)

        if not ctx.data["mentions"]:
            user = ctx.data["author"]["id"], ctx.data["author"]["avatar"]
        else:
            user = ctx.data["mentions"][0]["id"], ctx.data["mentions"][0]["avatar"]

        image = ctx.requests.get(f"https://cdn.discordapp.com/avatars/{user[0]}/{user[1]}.png?size=2048").content

        discord.create_message(ctx.data["channel_id"], None, {
            "file": ("avatar.png", image, "multipart/form-data")
        })

    @bot.command(description="Pokazuje w ilu procentach osoby sie kochają", usage="ship (osoba) [osoba]", category="Fun", _default=True)
    def ship(ctx):
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
            return handler.error_handler(ctx, "arguments", "ship (osoba) [osoba]")

        open("member1.png", "wb").write(ctx.requests.get(m_avatar).content)
        open("member2.png", "wb").write(ctx.requests.get(me_avatar).content)
        
        para = Image.open("para.png").convert("RGBA")
        member1 = Image.open("member1.png").convert("RGBA")
        member2 = Image.open("member2.png").convert("RGBA")

        member1 = ImageOps.fit(member1, (300, 300))
        member2 = ImageOps.fit(member2, (300, 300))
        
        para.paste(member1, (360, 250), member1)
        para.paste(member2, (890, 180), member2)
        
        para.save("ship.png")

        discord.create_message(ctx.data["channel_id"], {
            "content": f"**{m[2]}** + **{me[2]}** = **{m[2][:round(len(m[2]) / 2)].lower()}{me[2][round(len(me[2]) / 2):].lower()}**\nIch miłość jest równa **{random.randint(0, 100)}%**!"
        },
        {
            "file": ("ship.png", open("ship.png", "rb"), "multipart/form-data")
        })

    @bot.command(description="Odpowiada na pytanie", usage="8ball (pytanie)", category="Fun", _default=True)
    def _8ball(ctx):
        if not functions.has_permission(ctx):
            return handler.error_handler(ctx, "nopermission", ctx.command)

        if not ctx.args:
            return handler.error_handler(ctx, "arguments", "8ball (pytanie)")

        discord.create_message(ctx.data["channel_id"], {
            "content": random.choice("Tak, Nie, Możliwe że tak, Możliwe że nie, Możliwe lecz nie wiem, Raczej tak, Raczej nie, Oczywiście że tak, Oczywiście że nie, Na pewno tak, Na pewno nie, Jeszczee jak, Jak najbardziej".split(", "))
        })

    @bot.command(description="Pokazuje ikone serwera", usage="servericon", category="Fun", _default=True)
    def servericon(ctx):
        if not functions.has_permission(ctx):
            return handler.error_handler(ctx, "nopermission", ctx.command)

        guild = discord.get_guild(ctx.data["guild_id"])

        image = ctx.requests.get(f"https://cdn.discordapp.com/icons/{ctx.data['guild_id']}/{guild['icon']}.png?size=2048").content

        discord.create_message(ctx.data["channel_id"], None, {
            "file": ("servericon.png", image, "multipart/form-data")
        })

    @bot.command(description="Uderza osobe", usage="slap (osoba)", category="Fun", _default=True)
    def slap(ctx):
        if not functions.has_permission(ctx):
            return handler.error_handler(ctx, "nopermission", ctx.command)

        if not len(ctx.data["mentions"]) == 1:
            return handler.error_handler(ctx, "arguments", "slap (osoba)")

        image_url = ctx.requests.get("https://nekos.life/api/v2/img/slap").json()["url"]
        image = ctx.requests.get(image_url).content

        discord.create_message(ctx.data["channel_id"], {
            "content": f"**{ctx.data['author']['username']}** uderzył **{ctx.data['mentions'][0]['username']}**!"
        },
        {
            "file": ("slap.gif", image, "multipart/form-data")
        })

    @bot.command(description="Całuje osobe", usage="kiss (osoba)", category="Fun", _default=True)
    def kiss(ctx):
        if not functions.has_permission(ctx):
            return handler.error_handler(ctx, "nopermission", ctx.command)

        if not len(ctx.data["mentions"]) == 1:
            return handler.error_handler(ctx, "arguments", "kiss (osoba)")

        image_url = ctx.requests.get("https://nekos.life/api/kiss").json()["url"]
        image = ctx.requests.get(image_url).content

        discord.create_message(ctx.data["channel_id"], {
            "content": f"**{ctx.data['author']['username']}** pocałował **{ctx.data['mentions'][0]['username']}**!"
        },
        {
            "file": ("kiss.gif", image, "multipart/form-data")
        })

    @bot.command(description="Przytula osobe", usage="hug (osoba)", category="Fun", _default=True)
    def hug(ctx):
        if not functions.has_permission(ctx):
            return handler.error_handler(ctx, "nopermission", ctx.command)

        if not len(ctx.data["mentions"]) == 1:
            return handler.error_handler(ctx, "arguments", "hug (osoba)")

        image_url = ctx.requests.get("https://nekos.life/api/hug").json()["url"]
        image = ctx.requests.get(image_url).content

        discord.create_message(ctx.data["channel_id"], {
            "content": f"**{ctx.data['author']['username']}** przytulił **{ctx.data['mentions'][0]['username']}**!"
        },
        {
            "file": ("hug.gif", image, "multipart/form-data")
        })

    @bot.command(description="Pokazuje losowe zdjęcie kota", usage="cat", category="Fun", _default=True)
    def cat(ctx):
        if not functions.has_permission(ctx):
            return handler.error_handler(ctx, "nopermission", ctx.command)

        image_url = ctx.requests.get("https://some-random-api.ml/img/cat").json()["link"]
        image = ctx.requests.get(image_url).content

        discord.create_message(ctx.data["channel_id"], None, {
            "file": ("cat.png", image, "multipart/form-data")
        })

    @bot.command(description="Pokazuje losowe zdjęcie psa", usage="dog", category="Fun", _default=True)
    def dog(ctx):
        if not functions.has_permission(ctx):
            return handler.error_handler(ctx, "nopermission", ctx.command)

        image_url = ctx.requests.get("https://some-random-api.ml/img/dog").json()["link"]
        image = ctx.requests.get(image_url).content

        discord.create_message(ctx.data["channel_id"], None, {
            "file": ("dog.png", image, "multipart/form-data")
        })

    @bot.command(description="Pokazuje losowe zdjęcie pandy", usage="panda", category="Fun", _default=True)
    def panda(ctx):
        if not functions.has_permission(ctx):
            return handler.error_handler(ctx, "nopermission", ctx.command)

        image_url = ctx.requests.get("https://some-random-api.ml/img/panda").json()["link"]
        image = ctx.requests.get(image_url).content

        discord.create_message(ctx.data["channel_id"], None, {
            "file": ("panda.png", image, "multipart/form-data")
        })

    @bot.command(description="Generuje tekst w ascii", usage="ascii (tekst)", category="Fun", _default=True)
    def ascii(ctx):
        if not functions.has_permission(ctx):
            return handler.error_handler(ctx, "nopermission", ctx.command)

        if not ctx.args:
            return handler.error_handler(ctx, "arguments", "ascii (tekst)")

        discord.create_message(ctx.data["channel_id"], {
            "content": "```" + pyfiglet.Figlet().renderText(" ".join(ctx.args)) + "```"
        })

    @bot.command(description="Pokazuje w ilu procentach jest sie gejem", usage="howgay [osoba]", category="Fun", _default=True)
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

    @bot.command(description="Wysyła obrazek \"Achievement Get!\"", usage="achievement (tekst)", category="Fun", _default=True)
    def achievement(ctx):
        if not functions.has_permission(ctx):
            return handler.error_handler(ctx, "nopermission", ctx.command)

        ctx.args = " ".join(ctx.args)
        if not ctx.args:
            return handler.error_handler(ctx, "arguments", "achievement (tekst)")
        elif len(ctx.args) > 23:
            return handler.error_handler(ctx, "toolongtext", 23)

        ctx.args = ctx.args.replace(" ", "+").replace("ś", "s").replace("ę", "e").replace("ż", "z").replace("ź", "z").replace("ł", "l").replace("ó", "o").replace("ą", "a").replace("ć", "c").replace("Ś", "S").replace("Ę", "E").replace("Ż", "Z").replace("Ź", "Z").replace("Ł", "L").replace("Ó", "O").replace("Ą", "A").replace("Ć", "C")

        image = ctx.requests.get(f"https://minecraftskinstealer.com/achievement/{random.randint(1, 40)}/Achievement+Get%21/{ctx.args}").content

        discord.create_message(ctx.data["channel_id"], None, {
            "file": ("achievement.png", image, "multipart/form-data")
        })

    @bot.command(description="Wysyła tekst w emotkach garfield", usage="garfield (tekst)", category="Fun", _default=True)
    def garfield(ctx):
        if not functions.has_permission(ctx):
            return handler.error_handler(ctx, "nopermission", ctx.command)

        ctx.args = (" ".join(ctx.args)).lower()
        if not ctx.args:
            return handler.error_handler(ctx, "arguments", "garfield (tekst)")
        elif len(ctx.args) > 100:
            return handler.error_handler(ctx, "toolongtext", 100)

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

        discord.create_message(ctx.data["channel_id"], {
            "content": text
        })

    @bot.event
    def INTERACTION_CREATE(ctx):
        if (ctx.data["member"]["user"]["id"], ctx.data["channel_id"], ctx.data["message"]["id"]) in interactions:
            if not ctx.data["message"]["id"] in results:
                results[ctx.data["message"]["id"]] = ""

            custom_id = ctx.data["data"]["custom_id"]
            message_id = ctx.data["message"]["id"]

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
                    results[message_id] += "=" + str(eval(results[message_id]))
                except:
                    results[message_id] = ""
            elif custom_id == "add":
                results[message_id] += "+"
            else:
                results[message_id] += custom_id

            ctx.requests.post(f"https://discord.com/api/v8/interactions/{ctx.data['id']}/{ctx.data['token']}/callback", json={
                "type": 7,
                "data": {
                    "content": f"```{results[message_id] if results[message_id] else '0'}```"
                }
            })

    @bot.command(description="Kalkulator", usage="calc (działanie matematyczne)", category="Fun", _default=True)
    def calc(ctx):
        if not functions.has_permission(ctx):
            return handler.error_handler(ctx, "nopermission", ctx.command)

        msg = discord.create_message(ctx.data["channel_id"], {
            "content": "```0```",
            "components": [
                {
                    "type": 1,
                    "components": [
                        {
                            "type": 2,
                            "label": "x\u02b8",
                            "style": 2,
                            "custom_id": "power"
                        },
                        {
                            "type": 2,
                            "label": "%",
                            "style": 2,
                            "custom_id": "percent"
                        },
                        {
                            "type": 2,
                            "label": "<-",
                            "style": 2,
                            "custom_id": "backspace"
                        },
                        {
                            "type": 2,
                            "label": "C",
                            "style": 4,
                            "custom_id": "clear"
                        }
                    ]
                },
                {
                    "type": 1,
                    "components": [
                        {
                            "type": 2,
                            "label": "7",
                            "style": 2,
                            "custom_id": "7"
                        },
                        {
                            "type": 2,
                            "label": "8",
                            "style": 2,
                            "custom_id": "8"
                        },
                        {
                            "type": 2,
                            "label": "9",
                            "style": 2,
                            "custom_id": "9"
                        },
                        {
                            "type": 2,
                            "label": "/",
                            "style": 2,
                            "custom_id": "divide"
                        },
                        {
                            "type": 2,
                            "label": "(",
                            "style": 2,
                            "custom_id": "leftbracket"
                        }
                    ]
                },
                {
                    "type": 1,
                    "components": [
                        {
                            "type": 2,
                            "label": "4",
                            "style": 2,
                            "custom_id": "4"
                        },
                        {
                            "type": 2,
                            "label": "5",
                            "style": 2,
                            "custom_id": "5"
                        },
                        {
                            "type": 2,
                            "label": "6",
                            "style": 2,
                            "custom_id": "6"
                        },
                        {
                            "type": 2,
                            "label": "*",
                            "style": 2,
                            "custom_id": "multiply"
                        },
                        {
                            "type": 2,
                            "label": ")",
                            "style": 2,
                            "custom_id": "rightbracket"
                        }
                    ]
                },
                {
                    "type": 1,
                    "components": [
                        {
                            "type": 2,
                            "label": "1",
                            "style": 2,
                            "custom_id": "1"
                        },
                        {
                            "type": 2,
                            "label": "2",
                            "style": 2,
                            "custom_id": "2"
                        },
                        {
                            "type": 2,
                            "label": "3",
                            "style": 2,
                            "custom_id": "3"
                        },
                        {
                            "type": 2,
                            "label": "-",
                            "style": 2,
                            "custom_id": "minus"
                        }
                    ]
                },
                {
                    "type": 1,
                    "components": [
                        {
                            "type": 2,
                            "label": "0",
                            "style": 2,
                            "custom_id": "0"
                        },
                        {
                            "type": 2,
                            "label": ".",
                            "style": 2,
                            "custom_id": "dot"
                        },
                        {
                            "type": 2,
                            "label": "=",
                            "style": 1,
                            "custom_id": "equal"
                        },
                        {
                            "type": 2,
                            "label": "+",
                            "style": 2,
                            "custom_id": "add"
                        }
                    ]
                }
            ]
        })

        msg = msg.json()
        interactions.append((ctx.data["author"]["id"], ctx.data["channel_id"], msg["id"]))

    @bot.command(description="Ukrywa tekst w tekście", usage="encode (tekst wyświetlany) | (tekst ukryty)", category="Fun", _default=True)
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
            if char in arrays._characters:
                text += arrays._characters[char] + "\u200f"

        text += ctx.args[0][1:]

        discord.create_message(ctx.data["channel_id"], {
            "content": "`" + text + "`"
        })

    @bot.command(description="Pokazuje ukryty tekst", usage="decode (tekst)", category="Fun", _default=True)
    def decode(ctx):
        if not functions.has_permission(ctx):
            return handler.error_handler(ctx, "nopermission", ctx.command)

        ctx.args = " ".join(ctx.args)
        if not ctx.args:
            return handler.error_handler(ctx, "arguments", "encode (tekst wyświetlany) | (tekst ukryty)")

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
            return discord.create_message(ctx.data["channel_id"], {
                "content": "W tej wiadomości nie ma ukrytego tekstu"
            })
        
        discord.create_message(ctx.data["channel_id"], {
            "content": "`" + text + "`"
        })

    @bot.command(description="\"nie widać mnie\" mem z poligonu", usage="cantseeme [tekst/osoba/obrazek/url z obrazkiem]", category="Fun", _default=True)
    def cantseeme(ctx):
        if not functions.has_permission(ctx):
            return handler.error_handler(ctx, "nopermission", ctx.command)

        formats = ("image/png", "image/jpeg", "image/gif", "image/webp")

        if (len(ctx.data["mentions"]) and len(ctx.args)) == 1:
            message_type = "image"
            content = ctx.requests.get(f"https://cdn.discordapp.com/avatars/{ctx.data['mentions'][0]['id']}/{ctx.data['mentions'][0]['avatar']}.png?size=2048").content
            open("image.png", "wb").write(content)

        elif len(ctx.data["attachments"]) == 1:
            req = ctx.requests.get(ctx.data["attachments"][0]["url"])
            message_type = "text"
            if req.headers["content-type"] in formats:
                message_type = "image"
                open("image.png", "wb").write(req.content)

        elif len(ctx.args) == 1 and ctx.args[0].startswith(("https://", "http://")):
            req = ctx.requests.get(ctx.args[0])
            message_type = "text"
            if req.headers["content-type"] in formats:
                message_type = "image"
                open("image.png", "wb").write(req.content)

        elif len(ctx.args) >= 1:
            message_type = "text"

        elif not ctx.args:
            message_type = "image"
            content = ctx.requests.get(f"https://cdn.discordapp.com/avatars/{ctx.data['author']['id']}/{ctx.data['author']['avatar']}.png?size=2048").content
            open("image.png", "wb").write(content)

        krzak = Image.open("krzak.png")
        image = Image.open("image.png")

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

    @bot.command(description="Wysyła zatęczowany avatar", usage="gay [osoba]", category="Fun", _default=True)
    def gay(ctx):
        if not functions.has_permission(ctx):
            return handler.error_handler(ctx, "nopermission", ctx.command)

        if not ctx.data["mentions"]:
            user = ctx.data["author"]["id"], ctx.data["author"]["avatar"]
        else:
            user = ctx.data["mentions"][0]["id"], ctx.data["mentions"][0]["avatar"]

        content = ctx.requests.get(f"https://cdn.discordapp.com/avatars/{user[0]}/{user[1]}.png?size=2048").content
        open("image.png", "wb").write(content)

        image = Image.open("image.png").convert("RGBA")
        lgbt = Image.open("lgbt.png").convert("RGBA")
        
        image = ImageOps.fit(image, (512, 512))
        lgbt = ImageOps.fit(lgbt, (512, 512))

        mask = Image.new("L", (512, 512), 128)

        avatar = Image.composite(image, lgbt, mask)
        avatar.save("gay.png")

        discord.create_message(ctx.data["channel_id"], None, {
            "file": ("gay.png", open("gay.png", "rb"), "multipart/form-data")
        })

    @bot.command(description="Wysyła losowego mema z jbzd", usage="meme", category="Fun", _default=True)
    def meme(ctx):
        if not functions.has_permission(ctx):
            return handler.error_handler(ctx, "nopermission", ctx.command)

        channel = discord.get_channel(ctx.data["channel_id"])
        if not channel["nsfw"]:
            return handler.error_handler(ctx, "nsfw")

        url = ctx.requests.get("https://cenzurabot.pl/api/memes/jbzd").json()
        
        discord.create_message(ctx.data["channel_id"], {
            "content": url["meme"]
        })
