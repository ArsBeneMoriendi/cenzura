import functions
import handler
from PIL import Image, ImageDraw, ImageFont
import re
from lib.embed import Embed

def load(bot, discord):
    @bot.command(description="Pokazuje liste ostatnich usuniętych wiadomości", usage="snipe", category="Inne", default=True)
    def snipe(ctx):
        if not functions.has_permission(ctx):
            return handler.error_handler(ctx, "nopermission", ctx.command)

        if not hasattr(ctx, "snipe"):
            return ctx.send("Nie udało sie złapać żadnej usuniętej wiadomości")

        snipe = ctx.snipe[ctx.data["guild_id"]] if len(ctx.snipe[ctx.data["guild_id"]]) < 10 else [ctx.snipe[ctx.data["guild_id"]][::-1][_] for _ in range(10)][::-1]

        embed = Embed(title="Lista ostatnich usuniętych wiadomości:", description="\n".join([f"<#{message['channel_id']}> <@{message['author']['id']}>: {message['content']}" for message in snipe]), color=0xe74c3c)
        ctx.send(embed=embed)

    @bot.command(description="Lista komend todo", usage="todo", category="Inne", default=True)
    def todo(ctx):
        if not ctx.args:
            embed = Embed(title="Komendy todo:", description="> `todo add (tekst)`, `todo view [osoba]`, `todo remove (id)`, `todo clear`", color=0xe74c3c)
            return ctx.send(embed=embed)

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
            
            ctx.send("Dodano do todo")

        elif ctx.args[0] == "view":
            if len(ctx.data["mentions"]) == 1:
                user = ctx.data["mentions"][0]["id"]
            
            user = discord.get_user(user)

            embed = Embed(title=f"Todo użytkownika {user['username']}:", description="\n".join([f"{users[user['id']]['todo'].index(i)}. {i}" for i in users[user["id"]]["todo"]]), color=0xe74c3c)
            ctx.send(embed=embed)

        elif ctx.args[0] == "remove":
            if not len(ctx.args) == 2:
                return handler.error_handler(ctx, "arguments", "todo remove (id)")

            del users[user]["todo"][int(ctx.args[1])]
            ctx.send("Usunięto z todo")

        elif ctx.args[0] == "clear":
            del users[user]["todo"]
            ctx.send("Wyczyszczono todo")

        functions.write_json("users", users)

    @bot.command(description="Własne komendy", usage="cmd", category="Inne")
    def cmd(ctx):
        if not functions.has_permission(ctx):
            return handler.error_handler(ctx, "nopermission", ctx.command)

        guild = ctx.data["guild_id"]
        guilds = functions.read_json("guilds")

        if not "cmd" in guilds[guild]:
            guilds[guild]["cmd"] = {}

        if not ctx.args:
            embed = Embed(title="Komendy cmd:", description="> `cmd add (komenda) (tekst)`, `cmd remove (komenda)`, `cmd info (komenda)`, `cmd list`", color=0xe74c3c)
            embed.set_footer(text="<> = nazwa użytkownika, [] = wzmianka")

            return ctx.send(embed=embed)

        if ctx.args[0] == "add":
            if not len(ctx.args) >= 3:
                return handler.error_handler(ctx, "arguments", "cmd add (nazwa komendy) (tekst)")

            guilds[guild]["cmd"][ctx.args[1]] = {}
            guilds[guild]["cmd"][ctx.args[1]]["author"] = ctx.data["author"]
            guilds[guild]["cmd"][ctx.args[1]]["text"] = ctx.args[2]

            ctx.send("Dodano komende")

        elif ctx.args[0] == "remove":
            if not len(ctx.args) == 2:
                return handler.error_handler(ctx, "arguments", "cmd remove (nazwa komendy)")

            del guilds[guild]["cmd"][ctx.args[1]]
            ctx.send("Usunięto komende")

        elif ctx.args[0] == "info":
            if not len(ctx.args) == 2:
                return handler.error_handler(ctx, "arguments", "cmd info (nazwa komendy)")

            embed = Embed(title=f"Informacje o {ctx.args[1]}:", color=0xe74c3c)
            embed.add_field(name="Autor:", value=f"{guilds[guild]['cmd'][ctx.args[1]]['author']['username']}#{guilds[guild]['cmd'][ctx.args[1]]['author']['discriminator']} ({guilds[guild]['cmd'][ctx.args[1]]['author']['id']})")
            embed.add_field(name="Tekst w komendzie:", value=guilds[guild]["cmd"][ctx.args[1]]["text"])

            ctx.send(embed=embed)

        elif ctx.args[0] == "list":
            embed = Embed(title=f"Lista komend ({len(guilds[guild]['cmd'])}):", description="\n".join([x for x in guilds[guild]["cmd"]]), color=0xe74c3c)
            ctx.send(embed=embed)

        else:
            embed = Embed(title="Komendy cmd:", description="> `cmd add (komenda) (tekst)`, `cmd remove (komenda)`, `cmd info (komenda)`, `cmd list`", color=0xe74c3c)
            embed.set_footer(text="<> = nazwa użytkownika, [] = wzmianka")

            return ctx.send(embed=embed)

        functions.write_json("guilds", guilds)

    @bot.command(description="Profile", usage="profile", category="Inne", default=True)
    def profile(ctx):
        if not ctx.args:
            embed = Embed(title="Komendy profile:", description="> `profile view [osoba]`, `profile set`, `profile remove`", color=0xe74c3c)
            return ctx.send(embed=embed)

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
            gender = "" if not "gender" in users[user["id"]]["profile"] else users[user["id"]]["profile"]["gender"]
            age = "nie podano" if not "age" in users[user["id"]]["profile"] else users[user["id"]]["profile"]["age"]
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
                description = description.replace(char, polish_chars[char])

            new_description = ""

            if len(description) >= 40:
                x = 0
                for i in description:
                    if x == 30:
                        new_description += "\n"
                        x = 0

                    new_description += i
                    x += 1

                description = new_description

            avatar = ctx.requests.get(f"https://cdn.discordapp.com/avatars/{user['id']}/{user['avatar']}.png?size=512").content
            open("images/image.png", "wb").write(avatar)
                    
            image = Image.new("RGBA", (512, 512), (0, 0, 0))
            color = Image.new("RGBA", (512, 160), tuple(map(lambda x: int(x), color.split(";"))))
            avatar = Image.open("images/image.png").convert("RGBA")
            prostokaty = Image.open("images/prostokaty.png").convert("RGBA")

            avatar.thumbnail((125, 125))
            prostokaty.thumbnail((512, 512))

            username = user["username"] + "#" + user["discriminator"]
            image.paste(color, (0, 0), color)
            image.paste(prostokaty, (0, 0), prostokaty)
            image.paste(avatar, (10, 10), avatar)

            size = 50
            for char in username:
                size -= 1

            draw = ImageDraw.Draw(image)
            username_font = ImageFont.truetype("fonts/Poppins-Bold.ttf", round(size))
            gender_font = ImageFont.truetype("fonts/Poppins-Bold.ttf", 20)
            text1_font = ImageFont.truetype("fonts/Poppins-Bold.ttf", 15)
            text2_font = ImageFont.truetype("fonts/Poppins-Bold.ttf", 20)
            invoked_font = ImageFont.truetype("fonts/Poppins-Bold.ttf", 20)

            draw.text((150, 40), gender, font=gender_font, fill="black")
            draw.text((149, 41), gender, font=gender_font)

            draw.text((150, 54), username, font=username_font, fill="black")
            draw.text((149, 55), username, font=username_font)

            draw.text((40, 190), "Imie:", font=text1_font)
            draw.text((275, 190), "Wiek:", font=text1_font)
            draw.text((40, 293), "Opis:", font=text1_font)

            draw.text((40, 215), name, font=text2_font)
            draw.text((275, 215), age, font=text2_font)
            draw.text((40, 318), description, font=text2_font)

            image.save("images/profile.png")

            ctx.send(files=[("profile.png", open("images/profile.png", "rb"))])
        
        elif ctx.args[0] == "set":
            if not ctx.args[1:]:
                embed = Embed(title="Komendy profile set:", description="> `profile set name (imie)`, `profile set gender (m/k)`, `profile set age (wiek)`, `profile set description (opis)`, `profile set color (#hex/rgb)`", color=0xe74c3c)
                return ctx.send(embed=embed)

            if ctx.args[1] == "name":
                if not len(ctx.args) == 3:
                    return handler.error_handler(ctx, "arguments", "profile set name (imie)")

                if not len(ctx.args[2]) < 10:
                    return handler.error_handler(ctx, "toolongtext", 10)

                users[user]["profile"]["name"] = ctx.args[2]

                ctx.send("Ustawiono imie")

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

                ctx.send("Ustawiono płeć")

            elif ctx.args[1] == "age":
                if not len(ctx.args) == 3:
                    return handler.error_handler(ctx, "arguments", "profile set age (wiek)")

                try:
                    if int(ctx.args[2]) > 100:
                        return ctx.send("Za dużo")
                    elif int(ctx.args[2]) < 13:
                        return ctx.send("Za mało")
                except:
                    return handler.error_handler(ctx, "arguments", "profile set age (wiek)")

                users[user]["profile"]["age"] = ctx.args[2]

                ctx.send("Ustawiono wiek")

            elif ctx.args[1] == "description":
                if len(" ".join(ctx.args[2:])) > 150:
                    return handler.error_handler(ctx, "toolongtext", 150)

                users[user]["profile"]["description"] = " ".join(ctx.args[2:])

                ctx.send("Ustawiono opis")

            elif ctx.args[1] == "color":
                if re.search(r"^#(?:[0-9a-fA-F]{3}){1,2}$", ctx.args[2]):
                    color = ";".join(tuple(str(int(ctx.args[2][1:][i:i+2], 16)) for i in (0, 2, 4)))
                elif len(ctx.args[2:]) == 3 and (not False in ((x.isdigit() and int(x) <= 255) for x in ctx.args[2:])):
                    color = ";".join(ctx.args[2:])
                else:
                    return handler.error_handler(ctx, "arguments", "profile set color (hex/rgb)")

                users[user]["profile"]["color"] = color

                ctx.send("Ustawiono kolor")

            else:
                embed = Embed(title="Komendy profile set:", description="> `profile set name (imie)`, `profile set gender (m/k)`, `profile set age (wiek)`, `profile set description (opis)`, `profile set color (#hex/rgb)`", color=0xe74c3c)
                return ctx.send(embed=embed)

        elif ctx.args[0] == "remove":
            if not ctx.args[1:]:
                embed = Embed(title="Komendy profile remove:", description="> `profile remove name`, `profile remove gender`, `profile remove age`, `profile remove description`, `profile remove color`", color=0xe74c3c)
                return ctx.send(embed=embed)

            if ctx.args[1] == "name":
                del users[user]["profile"]["name"]
                ctx.send("Usunięto imie z twojego profilu")

            elif ctx.args[1] == "gender":
                del users[user]["profile"]["gender"]
                ctx.send("Usunięto płeć z twojego profilu")

            elif ctx.args[1] == "age":
                del users[user]["profile"]["age"]
                ctx.send("Usunięto wiek z twojego profilu")

            elif ctx.args[1] == "description":
                del users[user]["profile"]["description"]
                ctx.send("Usunięto opis z twojego profilu")

            elif ctx.args[1] == "color":
                del users[user]["profile"]["color"]
                ctx.send("Usunięto kolor z twojego profilu")

            else:
                embed = Embed(title="Komendy profile remove:", description="> `profile remove name`, `profile remove gender`, `profile remove age`, `profile remove description`, `profile remove color`", color=0xe74c3c)
                return ctx.send(embed=embed)

        else:
            embed = Embed(title="Komendy profile:", description="> `profile view [osoba]`, `profile set`, `profile remove`", color=0xe74c3c)
            return ctx.send(embed=embed)

        functions.write_json("users", users)
