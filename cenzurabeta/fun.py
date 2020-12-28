import urllib.parse
import requests
import random
import json
import handler
from PIL import Image
import os
import pyfiglet
import functions

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