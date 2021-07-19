from functions import *
from PIL import Image, ImageDraw, ImageFont
import re
from lib.embed import Embed
from lib.errors import NoPermission, Forbidden
from lib.types import User, Member

def load(bot, discord):
    @bot.command(description="Pokazuje liste ostatnich usuniętych wiadomości", usage="snipe", category="Inne", default=True)
    def snipe(ctx):
        if not has_permission(ctx):
            raise NoPermission(f"{ctx.author.id} has no {ctx.command} permission", ctx.command)

        if not hasattr(ctx, "snipe"):
            return ctx.send("Nie udało sie złapać żadnej usuniętej wiadomości")

        snipe = ctx.snipe[ctx.guild.id] if len(ctx.snipe[ctx.guild.id]) < 10 else [ctx.snipe[ctx.guild.id][::-1][_] for _ in range(10)][::-1]

        embed = Embed(title="Lista ostatnich usuniętych wiadomości:", description="\n".join([f"{message['channel'].mention} {message['author'].mention}: {message['content']}" for message in snipe]), color=0xe74c3c)
        ctx.send(embed=embed)

    @bot.command(description="Lista komend todo", usage="todo", category="Inne", default=True)
    def todo(ctx, subcommand = None, arg: find_working(User, int, str) = None):
        help_embed = Embed(title="Komendy todo:", description="> `todo add (tekst)`, `todo view [osoba]`, `todo remove (id)`, `todo clear`", color=0xe74c3c)
        
        if not subcommand:
            return ctx.send(embed=help_embed)

        users = read_json("users")

        if not ctx.author.id in users:
            users[ctx.author.id] = {}

        if not "todo" in users[ctx.author.id]:
            users[ctx.author.id]["todo"] = []

        if subcommand == "add":
            if not arg:
                return ctx.send(embed=help_embed)

            ctx.args = " ".join(ctx.args[1:])
            if len(ctx.args) > 100:
                return ctx.send("Tekst jest za długi (maksymalna długość to 100)")

            users[ctx.author.id]["todo"].append(ctx.args)
            
            ctx.send("Dodano do todo")

        elif subcommand == "view":
            arg = arg or ctx.author
            if not isinstance(arg, (Member, User)):
                embed = Embed(title="Komendy todo:", description="> `todo add (tekst)`, `todo view [osoba]`, `todo remove (id)`, `todo clear`", color=0xe74c3c)
                return ctx.send(embed=embed)

            embed = Embed(title=f"Todo użytkownika {arg.username}:", description="\n".join([f"{users[arg.id]['todo'].index(i)}. {i}" for i in users[arg.id]["todo"]]), color=0xe74c3c)
            ctx.send(embed=embed)

        elif subcommand == "remove":
            if arg == None:
                return ctx.send(embed=help_embed)

            del users[ctx.author.id]["todo"][arg]
            ctx.send("Usunięto z todo")

        elif subcommand == "clear":
            del users[ctx.author.id]["todo"]
            ctx.send("Wyczyszczono todo")

        write_json("users", users)

    @bot.command(description="Własne komendy", usage="cmd", category="Inne")
    def cmd(ctx, subcommand = None, arg = None, arg2 = None):
        if not has_permission(ctx):
            raise NoPermission(f"{ctx.author.id} has no {ctx.command} permission", ctx.command)

        help_embed = Embed(title="Komendy cmd:", description="> `cmd add (komenda) (tekst)`, `cmd remove (komenda)`, `cmd info (komenda)`, `cmd list`", color=0xe74c3c)
        help_embed.set_footer(text="<> = nazwa użytkownika, [] = wzmianka")

        if not subcommand:
            return ctx.send(embed=help_embed)

        guilds = read_json("guilds")

        if not "cmd" in guilds[ctx.guild.id]:
            guilds[ctx.guild.id]["cmd"] = {}

        if subcommand == "add":
            if not arg2:
                return ctx.send(embed=help_embed)

            guilds[ctx.guild.id]["cmd"][arg] = {}
            guilds[ctx.guild.id]["cmd"][arg]["author_id"] = ctx.author.id
            guilds[ctx.guild.id]["cmd"][arg]["text"] = arg2

            ctx.send("Dodano komende")

        elif subcommand == "remove":
            if not arg:
                return ctx.send(embed=help_embed)

            del guilds[ctx.guild.id]["cmd"][arg]
            ctx.send("Usunięto komende")

        elif subcommand == "info":
            if not arg:
                return ctx.send(embed=help_embed)

            user = User(guilds[ctx.guild.id]["cmd"][arg]["author_id"])

            embed = Embed(title=f"Informacje o {arg}:", color=0xe74c3c)
            embed.add_field(name="Autor:", value=f"{user.user} ({user.id})")
            embed.add_field(name="Tekst w komendzie:", value=guilds[ctx.guild.id]["cmd"][arg]["text"])

            ctx.send(embed=embed)

        elif subcommand == "list":
            embed = Embed(title=f"Lista komend ({len(guilds[ctx.guild.id]['cmd'])}):", description="\n".join([x for x in guilds[ctx.guild.id]["cmd"]]), color=0xe74c3c)
            ctx.send(embed=embed)

        else:
            return ctx.send(embed=help_embed)

        write_json("guilds", guilds)

    @bot.command(description="Profile", usage="profile", category="Inne", default=True)
    def profile(ctx, subcommand = None, arg: find_working(User, str) = None, arg2: find_working(between(13, 100), str) = None):
        if not subcommand:
            embed = Embed(title="Komendy profile:", description="> `profile view [osoba]`, `profile set`, `profile remove`", color=0xe74c3c)
            return ctx.send(embed=embed)

        users = read_json("users")

        if not "profile" in users[ctx.author.id]:
            users[ctx.author.id]["profile"] = {}
            write_json("users", users)

        if subcommand == "view":
            arg = arg or ctx.author
            if not isinstance(arg, (Member, User)):
                embed = Embed(title="Komendy profile:", description="> `profile view [osoba]`, `profile set`, `profile remove`", color=0xe74c3c)
                return ctx.send(embed=embed)

            if not "profile" in users[arg.id]:
                users[arg.id]["profile"] = {}
                write_json("users", users)

            name = "nie podano" if not "name" in users[arg.id]["profile"] else users[arg.id]["profile"]["name"]
            gender = "" if not "gender" in users[arg.id]["profile"] else users[arg.id]["profile"]["gender"]
            age = "nie podano" if not "age" in users[arg.id]["profile"] else users[arg.id]["profile"]["age"]
            description = "nie podano" if not "description" in users[arg.id]["profile"] else users[arg.id]["profile"]["description"]
            color = "0;0;0" if not "color" in users[arg.id]["profile"] else users[arg.id]["profile"]["color"]

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

            avatar = ctx.requests.get(arg.avatar_url).content
            open("images/image.png", "wb").write(avatar)
                    
            image = Image.new("RGBA", (512, 512), (0, 0, 0))
            color = Image.new("RGBA", (512, 160), tuple(map(lambda x: int(x), color.split(";"))))
            avatar = Image.open("images/image.png").convert("RGBA")
            prostokaty = Image.open("images/prostokaty.png").convert("RGBA")

            avatar.thumbnail((125, 125))
            prostokaty.thumbnail((512, 512))

            image.paste(color, (0, 0), color)
            image.paste(prostokaty, (0, 0), prostokaty)
            image.paste(avatar, (10, 10), avatar)

            size = 50
            for char in arg.user:
                size -= 1

            draw = ImageDraw.Draw(image)
            username_font = ImageFont.truetype("fonts/Poppins-Bold.ttf", round(size))
            gender_font = ImageFont.truetype("fonts/Poppins-Bold.ttf", 20)
            text1_font = ImageFont.truetype("fonts/Poppins-Bold.ttf", 15)
            text2_font = ImageFont.truetype("fonts/Poppins-Bold.ttf", 20)
            invoked_font = ImageFont.truetype("fonts/Poppins-Bold.ttf", 20)

            draw.text((150, 40), gender, font=gender_font, fill="black")
            draw.text((149, 41), gender, font=gender_font)

            draw.text((150, 54), arg.user, font=username_font, fill="black")
            draw.text((149, 55), arg.user, font=username_font)

            draw.text((40, 190), "Imie:", font=text1_font)
            draw.text((275, 190), "Wiek:", font=text1_font)
            draw.text((40, 293), "Opis:", font=text1_font)

            draw.text((40, 215), name, font=text2_font)
            draw.text((275, 215), age, font=text2_font)
            draw.text((40, 318), description, font=text2_font)

            image.save("images/profile.png")

            ctx.send(files=[("profile.png", open("images/profile.png", "rb"))])
        
        elif subcommand == "set":
            if not arg2:
                embed = Embed(title="Komendy profile set:", description="> `profile set name (imie)`, `profile set gender (m/k)`, `profile set age (13-100)`, `profile set description (opis)`, `profile set color (#hex/rgb)`", color=0xe74c3c)
                return ctx.send(embed=embed)

            if arg == "name":
                if len(arg2) > 10:
                    return ctx.send("Tekst jest za długi (maksymalna długość to 10)")

                users[ctx.author.id]["profile"]["name"] = arg2

                ctx.send("Ustawiono imie")

            elif arg == "gender":
                male = ["M", "MEZCZYZNA"]
                female = ["K", "KOBIETA"]
                available = male + female

                if not arg2.upper() in available:
                    embed = Embed(title="Komendy profile set:", description="> `profile set name (imie)`, `profile set gender (m/k)`, `profile set age (13-100)`, `profile set description (opis)`, `profile set color (#hex/rgb)`", color=0xe74c3c)
                    return ctx.send(embed=embed)

                if arg2.upper() in male:
                    users[ctx.author.id]["profile"]["gender"] = "mężczyzna"
                elif arg2.upper() in female:
                    users[ctx.author.id]["profile"]["gender"] = "kobieta"

                ctx.send("Ustawiono płeć")

            elif arg == "age":
                if not isinstance(arg2, int):
                    embed = Embed(title="Komendy profile set:", description="> `profile set name (imie)`, `profile set gender (m/k)`, `profile set age (13-100)`, `profile set description (opis)`, `profile set color (#hex/rgb)`", color=0xe74c3c)
                    return ctx.send(embed=embed)

                users[ctx.author.id]["profile"]["age"] = str(arg2)

                ctx.send("Ustawiono wiek")

            elif arg == "description":
                if len(" ".join(ctx.args[2:])) > 150:
                    return ctx.send("Tekst jest za długi (maksymalna długość to 150)")

                users[ctx.author.id]["profile"]["description"] = " ".join(ctx.args[2:])

                ctx.send("Ustawiono opis")

            elif arg == "color":
                if re.search(r"^#(?:[0-9a-fA-F]{3}){1,2}$", arg2):
                    color = ";".join(tuple(str(int(ctx.args[2][1:][i:i+2], 16)) for i in (0, 2, 4)))
                elif len(ctx.args[2:]) == 3 and (not False in ((x.isdigit() and int(x) <= 255) for x in ctx.args[2:])):
                    color = ";".join(ctx.args[2:])
                else:
                    embed = Embed(title="Komendy profile set:", description="> `profile set name (imie)`, `profile set gender (m/k)`, `profile set age (13-100)`, `profile set description (opis)`, `profile set color (#hex/rgb)`", color=0xe74c3c)
                    return ctx.send(embed=embed)

                users[ctx.author.id]["profile"]["color"] = color

                ctx.send("Ustawiono kolor")

            else:
                embed = Embed(title="Komendy profile set:", description="> `profile set name (imie)`, `profile set gender (m/k)`, `profile set age (13-100)`, `profile set description (opis)`, `profile set color (#hex/rgb)`", color=0xe74c3c)
                return ctx.send(embed=embed)

        elif subcommand == "remove":
            if not arg:
                embed = Embed(title="Komendy profile remove:", description="> `profile remove name`, `profile remove gender`, `profile remove age`, `profile remove description`, `profile remove color`", color=0xe74c3c)
                return ctx.send(embed=embed)

            if arg == "name":
                del users[ctx.author.id]["profile"]["name"]
                ctx.send("Usunięto imie z twojego profilu")

            elif arg == "gender":
                del users[ctx.author.id]["profile"]["gender"]
                ctx.send("Usunięto płeć z twojego profilu")

            elif arg == "age":
                del users[ctx.author.id]["profile"]["age"]
                ctx.send("Usunięto wiek z twojego profilu")

            elif arg == "description":
                del users[ctx.author.id]["profile"]["description"]
                ctx.send("Usunięto opis z twojego profilu")

            elif arg == "color":
                del users[ctx.author.id]["profile"]["color"]
                ctx.send("Usunięto kolor z twojego profilu")

            else:
                embed = Embed(title="Komendy profile remove:", description="> `profile remove name`, `profile remove gender`, `profile remove age`, `profile remove description`, `profile remove color`", color=0xe74c3c)
                return ctx.send(embed=embed)

        else:
            embed = Embed(title="Komendy profile:", description="> `profile view [osoba]`, `profile set`, `profile remove`", color=0xe74c3c)
            return ctx.send(embed=embed)

        write_json("users", users)
