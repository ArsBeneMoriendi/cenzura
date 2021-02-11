import functions
import handler
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageFilter
import requests
import re

def load(gateway, discord):
    @gateway.command(description="Pokazuje liste ostatnich usuniętych wiadomości", usage="snipe", category="Inne", _default=True)
    def snipe(ctx):
        if not functions.has_permission(ctx):
            return handler.error_handler(ctx, "nopermission", ctx.command)

        if not hasattr(ctx, "snipe"):
            return discord.create_message(ctx.data["channel_id"], {
                "content": "Nie udało sie złapać żadnej usuniętej wiadomości"
            })

        snipe = ctx.snipe[ctx.data["guild_id"]] if len(ctx.snipe[ctx.data["guild_id"]]) < 10 else [ctx.snipe[ctx.data["guild_id"]][::-1][_] for _ in range(10)][::-1]

        discord.create_message(ctx.data["channel_id"], {
            "embed": {
                "title": "Lista ostatnich usuniętych wiadomości:",
                "description": "\n".join([f"<#{message['channel_id']}> <@{message['author']['id']}>: {message['content']}" for message in snipe]),
                "color": 0xe74c3c,
                "footer": {
                    "text": f"Wywołane przez {ctx.data['author']['id']}"
                }
            }
        })

    @gateway.command(description="Lista komend todo", usage="todo", category="Inne", _default=True)
    def todo(ctx):
        if not ctx.args:
            return discord.create_message(ctx.data["channel_id"], {
                "embed": {
                    "title": "Komendy todo:",
                    "description": "> `todo add (tekst)`, `todo view [osoba]`, `todo remove (id)`, `todo clear`",
                    "color": 0xe74c3c
                }
            })

        user = ctx.data["author"]["id"]
        users = functions.read_json("users")

        if not user in users:
            users[user] = {}

        if not "todo" in users[user]:
            users[user]["todo"] = []

        if ctx.args[0] == "add":
            ctx.args = " ".join(ctx.args[1:])
            if len(ctx.args) > 100:
                return handler.error_handler(ctx, "toolongtext", 100)

            users[user]["todo"].append(ctx.args)
            
            discord.create_message(ctx.data["channel_id"], {
                "content": "Dodano do todo"
            })
        
        elif ctx.args[0] == "view":
            if len(ctx.data["mentions"]) == 1:
                user = ctx.data["mentions"][0]["id"]
            
            user = discord.get_user(user)

            discord.create_message(ctx.data["channel_id"], {
                "embed": {
                    "title": f"Todo użytkownika {user['username']}:",
                    "description": "\n".join([f"{users[user['id']]['todo'].index(i)}. {i}" for i in users[user["id"]]["todo"]]),
                    "color": 0xe74c3c,
                    "footer": {
                        "text": f"Wywołane przez {ctx.data['author']['id']}"
                    }
                }
            })

        elif ctx.args[0] == "remove":
            if not len(ctx.args) == 2:
                return handler.error_handler(ctx, "arguments", "todo remove (id)")

            del users[user]["todo"][int(ctx.args[1])]

            discord.create_message(ctx.data["channel_id"], {
                "content": "Usunięto z todo"
            })

        elif ctx.args[0] == "clear":
            del users[user]["todo"]

            discord.create_message(ctx.data["channel_id"], {
                "content": "Wyczyszczono todo"
            })

        functions.write_json("users", users)

    @gateway.command(description="Własne komendy", usage="cmd", category="Inne", _default=False)
    def cmd(ctx):
        if not functions.has_permission(ctx):
            return handler.error_handler(ctx, "nopermission", ctx.command)\

        guild = ctx.data["guild_id"]
        guilds = functions.read_json("guilds")

        if not "cmd" in guilds[guild]:
            guilds[guild]["cmd"] = {}

        if not ctx.args:
            return discord.create_message(ctx.data["channel_id"], {
                "embed": {
                    "title": "Komendy cmd:",
                    "description": "> `cmd add (komenda) (tekst)`, `cmd remove (komenda)`, `cmd info (komenda)`, `cmd list`",
                    "color": 0xe74c3c,
                    "footer": {
                        "text": "<> = nazwa użytkownika, [] = wzmianka"
                    }
                }
            })

        if ctx.args[0] == "add":
            if not len(ctx.args) >= 3:
                return handler.error_handler(ctx, "arguments", "cmd add (nazwa komendy) (tekst)")

            guilds[guild]["cmd"][ctx.args[1]] = {}
            guilds[guild]["cmd"][ctx.args[1]]["author"] = ctx.data["author"]
            guilds[guild]["cmd"][ctx.args[1]]["text"] = ctx.args[2]

            discord.create_message(ctx.data["channel_id"], {
                "content": "Dodano komende"
            })

        elif ctx.args[0] == "remove":
            if not len(ctx.args) == 2:
                return handler.error_handler(ctx, "arguments", "cmd remove (nazwa komendy)")

            del guilds[guild]["cmd"][ctx.args[1]]

            discord.create_message(ctx.data["channel_id"], {
                "content": "Usunięto komende"
            })

        elif ctx.args[0] == "info":
            if not len(ctx.args) == 2:
                return handler.error_handler(ctx, "arguments", "cmd info (nazwa komendy)")

            discord.create_message(ctx.data["channel_id"], {
                "embed": {
                    "title": f"Informacje o {ctx.args[1]}:",
                    "color": 0xe74c3c,
                    "fields": [
                        {
                            "name": "Autor:",
                            "value": f"{guilds[guild]['cmd'][ctx.args[1]]['author']['username']}#{guilds[guild]['cmd'][ctx.args[1]]['author']['discriminator']} ({guilds[guild]['cmd'][ctx.args[1]]['author']['id']})",
                            "inline": False
                        },
                        {
                            "name": "Tekst w komendzie:",
                            "value": guilds[guild]["cmd"][ctx.args[1]]["text"],
                            "inline": False
                        }
                    ]
                }
            })

        elif ctx.args[0] == "list":
            discord.create_message(ctx.data["channel_id"], {
                "embed": {
                    "title": f"Lista komend ({len(guilds[guild]['cmd'])}):",
                    "description": "\n".join([x for x in guilds[guild]["cmd"]]),
                    "color": 0xe74c3c
                }
            })

        functions.write_json("guilds", guilds)

    @gateway.command(description="Profile", usage="profile", category="Inne", _default=True)
    def profile(ctx):
        if not ctx.args:
            return discord.create_message(ctx.data["channel_id"], {
                "embed": {
                    "title": "Komendy profile:",
                    "description": "> `profile view [osoba]`, `profile set`, `profile remove`",
                    "color": 0xe74c3c
                }
            })

        user = ctx.data["author"]["id"]
        users = functions.read_json("users")

        if not "profile" in users[user]:
            users[user]["profile"] = {}
            functions.write_json("users", users)

        if ctx.args[0] == "view":
            if not ctx.data["mentions"]:
                user = ctx.data["author"]
            else:
                user = ctx.data["mentions"][0]
                if not "profile" in users[user["id"]]:
                    users[user["id"]]["profile"] = {}
                    functions.write_json("users", users)

            name = "nie podano" if not "name" in users[user["id"]]["profile"] else users[user["id"]]["profile"]["name"]
            gender = "nie podano" if not "gender" in users[user["id"]]["profile"] else users[user["id"]]["profile"]["gender"]
            age = "nie podano" if not "age" in users[user["id"]]["profile"] else users[user["id"]]["profile"]["age"]
            orientation = "nie podano" if not "orientation" in users[user["id"]]["profile"] else users[user["id"]]["profile"]["orientation"]
            description = "nie podano" if not "description" in users[user["id"]]["profile"] else users[user["id"]]["profile"]["description"]
            color = "0;0;0" if not "color" in users[user["id"]]["profile"] else users[user["id"]]["profile"]["color"]

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

            for char in polish_chars:
                name = name.replace(char, polish_chars[char])
                gender = gender.replace(char, polish_chars[char])
                age = age.replace(char, polish_chars[char])
                orientation = orientation.replace(char, polish_chars[char])
                description = description.replace(char, polish_chars[char])

            new_description = ""

            if len(description) > 20:
                x = 0
                for i in description:
                    if x == 24:
                        new_description += "\n"
                        x = 0

                    new_description += i
                    x += 1

                description = new_description

            avatar = requests.get(f"https://cdn.discordapp.com/avatars/{user['id']}/{user['avatar']}.png?size=512").content
            open("image.png", "wb").write(avatar)
                    
            image = Image.new("RGBA", (512, 512), tuple(map(lambda x: int(x), color.split(";"))))
            avatar = Image.open("image.png").convert("RGBA")
            cenzura = Image.open("cenzura.png").convert("RGBA")
            avatar.thumbnail((75, 75))
            cenzura.thumbnail((30, 30))

            image = image.filter(ImageFilter.GaussianBlur(12))

            username = user["username"] + "#" + user["discriminator"]
            image.paste(avatar, (10, 10), avatar)

            size = 40
            for char in username:
                size -= 0.5

            draw = ImageDraw.Draw(image)
            username_font = ImageFont.truetype("Poppins-Bold.ttf", round(size))
            description_font = ImageFont.truetype("Poppins-Bold.ttf", 30)
            invoked_font = ImageFont.truetype("Poppins-Bold.ttf", 20)

            draw.text((100, 14), username, font=username_font, fill="black")
            draw.text((99, 15), username, font=username_font)

            draw.text((10, 99), f"Imie: {name}\nPlec: {gender}\nWiek: {age}\nOrientacja: {orientation}\nOpis: {description}", font=description_font, fill="black")
            draw.text((9, 100), f"Imie: {name}\nPlec: {gender}\nWiek: {age}\nOrientacja: {orientation}\nOpis: {description}", font=description_font)
            
            draw.text((50, image.size[1] - 35), "Wywołane przez " + ctx.data["author"]["id"], font=invoked_font, fill="black")
            draw.text((49, image.size[1] - 34), "Wywołane przez " + ctx.data["author"]["id"], font=invoked_font)
            image.paste(cenzura, (10, image.size[1] - 35), cenzura)

            image.save("profile.png")

            discord.create_message(ctx.data["channel_id"], None, {
                "file": ("profile.png", open("profile.png", "rb"), "multipart/form-data")
            })
        
        elif ctx.args[0] == "set":
            if not ctx.args[1:]:
                return discord.create_message(ctx.data["channel_id"], {
                    "embed": {
                        "title": "Komendy profile set:",
                        "description": "> `profile set name (imie)`, `profile set gender (m/k)`, `profile set age (wiek)`, `profile set orientation (hetero/bi/homo)`, `profile set description (opis)`, `profile set color (hex/rgb)`",
                        "color": 0xe74c3c
                    }
                })

            if ctx.args[1] == "name":
                if not len(ctx.args) == 3:
                    return handler.error_handler(ctx, "arguments", "profile set name (imie)")

                if not len(ctx.args[2]) < 10:
                    return handler.error_handler(ctx, "toolongtext", 10)

                users[user]["profile"]["name"] = ctx.args[2]

                discord.create_message(ctx.data["channel_id"], {
                    "content": "Ustawiono imie"
                })

            elif ctx.args[1] == "gender":
                if not len(ctx.args) == 3:
                    return handler.error_handler(ctx, "arguments", "profile set gender (m/k)")

                male = ["M", "MEZCZYZNA"]
                female = ["K", "KOBIETA"]
                available = male + female

                if ctx.args[2].upper() in available:
                    if ctx.args[2].upper() in male:
                        users[user]["profile"]["gender"] = "mężczyzna"
                    elif ctx.args[2].upper() in female:
                        users[user]["profile"]["gender"] = "kobieta"
                else:
                    return handler.error_handler(ctx, "arguments", "profile set gender (m/k)")

                discord.create_message(ctx.data["channel_id"], {
                    "content": "Ustawiono płeć"
                })

            elif ctx.args[1] == "age":
                if not len(ctx.args) == 3:
                    return handler.error_handler(ctx, "arguments", "profile set age (wiek)")

                try:
                    if int(ctx.args[2]) > 100:
                        return discord.create_message(ctx.data["channel_id"], {
                            "content": "Za dużo"
                        })
                    elif int(ctx.args[2]) < 13:
                        return discord.create_message(ctx.data["channel_id"], {
                            "content": "Za mało"
                        })
                except:
                    return handler.error_handler(ctx, "arguments", "profile set age (wiek)")

                users[user]["profile"]["age"] = ctx.args[2]

                discord.create_message(ctx.data["channel_id"], {
                    "content": "Ustawiono wiek"
                })

            elif ctx.args[1] == "orientation":
                if not len(ctx.args) == 3:
                    return handler.error_handler(ctx, "arguments", "profile set orientation (hetero/bi/homo)")

                available = ["HETERO", "BI", "HOMO"]

                if ctx.args[2].upper() in available:
                    users[user]["profile"]["orientation"] = ctx.args[2].lower()
                else:
                    return handler.error_handler(ctx, "arguments", "profile set orientation (hetero/bi/homo)")

                discord.create_message(ctx.data["channel_id"], {
                    "content": "Ustawiono orientacje"
                })

            elif ctx.args[1] == "description":
                if len(" ".join(ctx.args[2:])) > 100:
                    return handler.error_handler(ctx, "toolongtext", 300)

                users[user]["profile"]["description"] = " ".join(ctx.args[2:])

                discord.create_message(ctx.data["channel_id"], {
                    "content": "Ustawiono opis"
                })

            elif ctx.args[1] == "color":
                if re.search(r"^#(?:[0-9a-fA-F]{3}){1,2}$", ctx.args[2]):
                    color = ";".join(tuple(str(int(ctx.args[2][1:][i:i+2], 16)) for i in (0, 2, 4)))
                elif len(ctx.args[2:]) == 3 and (not False in ((x.isdigit() and int(x) <= 255) for x in ctx.args[2:])):
                    color = ";".join(ctx.args[2:])
                else:
                    return handler.error_handler(ctx, "arguments", "profile set color (hex/rgb)")

                users[user]["profile"]["color"] = color

                discord.create_message(ctx.data["channel_id"], {
                    "content": "Ustawiono kolor"
                })

        elif ctx.args[0] == "remove":
            if not len(ctx.args) <= 3:
                return discord.create_message(ctx.data["channel_id"], {
                    "embed": {
                        "title": "Komendy profile remove:",
                        "description": "> `profile remove name`, `profile remove gender`, `profile remove age`, `profile remove orientation`, `profile remove description`, `profile remove color`",
                        "color": 0xe74c3c
                    }
                })

            if ctx.args[1] == "name":
                del users[user]["profile"]["name"]

                discord.create_message(ctx.data["channel_id"], {
                    "content": "Usunięto imie z twojego profilu"
                })

            elif ctx.args[1] == "gender":
                del users[user]["profile"]["gender"]

                discord.create_message(ctx.data["channel_id"], {
                    "content": "Usunięto płeć z twojego profilu"
                })

            elif ctx.args[1] == "age":
                del users[user]["profile"]["age"]

                discord.create_message(ctx.data["channel_id"], {
                    "content": "Usunięto wiek z twojego profilu"
                })

            elif ctx.args[1] == "orientation":
                del users[user]["profile"]["orientation"]

                discord.create_message(ctx.data["channel_id"], {
                    "content": "Usunięto orientacje z twojego profilu"
                })

            elif ctx.args[1] == "description":
                del users[user]["profile"]["description"]

                discord.create_message(ctx.data["channel_id"], {
                    "content": "Usunięto opis z twojego profilu"
                })

            elif ctx.args[1] == "color":
                del users[user]["profile"]["color"]

                discord.create_message(ctx.data["channel_id"], {
                    "content": "Usunięto kolor z twojego profilu"
                })

        functions.write_json("users", users)
