from lib import modules
import functions
import handler
from functions import *
from lib.permissions import PERMISSIONS
from lib.embed import Embed
from lib.errors import NoPermission, InvalidArgumentType
from lib.types import Member, Channel, Role

@modules.module
class Admin:
    def __init__(self, bot, discord):
        self.bot = bot
        self.discord = discord
        
    @modules.command(description="Wywala osobe z serwera", usage="kick (osoba) [powód]")
    def kick(self, ctx, member: Member, reason = "nie podano"):
        if not has_permission(ctx):
            raise NoPermission(f"{ctx.author.id} has no {ctx.command} permission", ctx.command)

        if reason == "nie podano":
            ctx.args[1:] = reason.split(" ")

        if ctx.author == member:
            return ctx.send("Nie możesz wyrzucić samego siebie")

        if ctx.author <= member:
            return ctx.send("Nie możesz wyrzucić osoby równej lub wyższej od ciebie")

        member.kick(" ".join(ctx.args[1:]))
        member.send(f"Zostałeś wyrzucony z serwera `{ctx.guild.name}` przez `{ctx.author.username}` z powodu `{' '.join(ctx.args[1:])}`")
        ctx.send(f"Wyrzucono użytkownika `{member.username}` z powodu `{' '.join(ctx.args[1:])}`")

    @modules.command(description="Banuje osobe na serwerze", usage="ban (osoba) [powód]")
    def ban(self, ctx, member: Member, reason = "nie podano"):
        if not has_permission(ctx):
            raise NoPermission(f"{ctx.author.id} has no {ctx.command} permission", ctx.command)

        if reason == "nie podano":
            ctx.args[1:] = reason.split(" ")

        if ctx.author == member:
            return ctx.send("Nie możesz zbanować samego siebie")

        if ctx.author <= member:
            return ctx.send("Nie możesz zbanować osoby równej lub wyższej od ciebie")

        member.ban(" ".join(ctx.args[1:]))
        member.send(f"Zostałeś zbanowany na serwerze `{ctx.guild.name}` przez `{ctx.author.username}` z powodu `{' '.join(ctx.args[1:])}`")
        ctx.send(f"Zbanowano użytkownika `{member.username}` z powodu `{' '.join(ctx.args[1:])}`")

    @modules.command(description="Usuwa wiadomości na kanale", usage="clear (2-99)")
    def clear(self, ctx, amount: between(2, 99)):
        if not has_permission(ctx):
            raise NoPermission(f"{ctx.author.id} has no {ctx.command} permission", ctx.command)

        amount += 1
        messages = [x["id"] for x in self.discord.get_messages(ctx.channel.id, amount)]
        ctx.channel.clear(messages)

        ctx.send("ok", reply=False)

    @modules.command(description="Pokazuje pomoc komendy set", usage="set", aliases=["ustaw"])
    def set(self, ctx, subcommand = None, arg: find_working(Channel, Role, str, Channel = lambda channel: channel.type == "GUILD_TEXT") = None, arg2 = None):
        if not has_permission(ctx):
            raise NoPermission(f"{ctx.author.id} has no {ctx.command} permission", ctx.command)

        help_embed = Embed(title="Komendy set:", description="> `set prefix (prefix)`, `set welcomemsg (kanał) (tekst)`, `set removewelcomemsg`, `set leavemsg (kanał) (tekst)`, `set removeleavemsg`, `set autorole (rola)`, `set removeautorole`, `set onbadwords`, `set offbadwords`, `set oninvites`, `set offinvites`", color=0xe74c3c)
        help_embed.set_footer(text="<> = nick osoby, [] = wzmianka, {} = licznik osób")

        if not subcommand:
            return ctx.send(embed=help_embed)

        guilds = read_json("guilds")

        if subcommand == "prefix":
            guilds[ctx.guild.id]["prefix"] = arg
            ctx.send(f"Ustawiono prefix na `{arg}`")

        elif subcommand == "welcomemsg":
            if not isinstance(arg, Channel) or not arg2:
                return ctx.send(embed=help_embed)

            guilds[ctx.guild.id]["welcomemsg"] = {}
            guilds[ctx.guild.id]["welcomemsg"]["channel_id"] = arg.id
            guilds[ctx.guild.id]["welcomemsg"]["text"] = " ".join(ctx.args[2:])

            ctx.send("Ustawiono wiadomość powitalną")

        elif subcommand == "removewelcomemsg":
            del guilds[ctx.guild.id]["welcomemsg"]
            ctx.send("Usunięto wiadomość powitalną")

        elif subcommand == "leavemsg":
            if not isinstance(arg, Channel) or not arg2:
                return ctx.send(embed=help_embed)

            guilds[ctx.guild.id]["leavemsg"] = {}
            guilds[ctx.guild.id]["leavemsg"]["channel_id"] = arg.id
            guilds[ctx.guild.id]["leavemsg"]["text"] = " ".join(ctx.args[2:])

            ctx.send("Ustawiono wiadomość pożegnalną")

        elif subcommand == "removeleavemsg":
            del guilds[ctx.guild.id]["leavemsg"]
            ctx.send("Usunięto wiadomość pożegnalną")

        elif subcommand == "autorole":
            if not isinstance(arg, Role):
                return ctx.send(embed=help_embed)

            guilds[ctx.guild.id]["autorole"] = arg.id
            ctx.send("Ustawiono autorole")

        elif subcommand == "removeautorole":
            del guilds[ctx.guild.id]["autorole"]
            ctx.send("Usunięto autorole")

        elif subcommand == "onbadwords":
            guilds[ctx.guild.id]["badwords"] = True
            ctx.send("Włączono brzydkie słowa na tym serwerze")

        elif subcommand == "offbadwords":
            del guilds[ctx.guild.id]["badwords"]
            ctx.send("Wyłączono brzydkie słowa na tym serwerze")

        elif subcommand == "oninvites":
            guilds[ctx.guild.id]["invites"] = True
            ctx.send("Włączono wysyłanie zaproszeń na tym serwerze")

        elif subcommand == "offinvites":
            del guilds[ctx.guild.id]["invites"]
            ctx.send("Wyłączono wysyłanie zaproszeń na tym serwerze")

        else:
            ctx.send(embed=help_embed)

        write_json("guilds", guilds)

    @modules.command(description="Mutuje użytkownika", usage="mute (osoba) [powód]")
    def mute(self, ctx, member: Member, reason = "nie podano"):
        if not has_permission(ctx):
            raise NoPermission(f"{ctx.author.id} has no {ctx.command} permission", ctx.command)

        if reason == "nie podano":
            ctx.args[1:] = reason.split(" ")

        if ctx.author == member:
            return ctx.send("Nie możesz zmutować samego siebie")

        if ctx.author <= member:
            return ctx.send("Nie możesz zmutować osoby równej lub wyższej od ciebie")

        guilds = read_json("guilds")

        if not "mute_role" in guilds[ctx.guild.id]:
            role = ctx.guild.create_role("muted").json()

            guilds[ctx.guild.id]["mute_role"] = role["id"]

            for _, channel in ctx.guild.channels.items():
                if channel.type == 0:
                    channel.edit_permissions(role["id"], {
                        "deny": PERMISSIONS["SEND_MESSAGES"],
                        "allow": PERMISSIONS["ADD_REACTIONS"],
                        "type": 0
                    })

                elif channel.type == 2:
                    channel.edit_permissions(role["id"], {
                        "deny": PERMISSIONS["SPEAK"],
                        "allow": PERMISSIONS["VIEW_CHANNEL"],
                        "type": 0
                    })

            write_json("guilds", guilds)

        member.add_role(guilds[ctx.guild.id]["mute_role"])
        member.send(f"Zostałeś zmutowany na serwerze `{ctx.guild.name}` przez `{ctx.author.username}` z powodu `{' '.join(ctx.args[1:])}`")
        ctx.send(f"Zmutowano użytkownika `{member.username}` z powodu `{' '.join(ctx.args[1:])}`")

    @modules.command(description="Odmutuje użytkownika", usage="unmute (osoba)")
    def unmute(self, ctx, member: Member):
        if not has_permission(ctx):
            raise NoPermission(f"{ctx.author.id} has no {ctx.command} permission", ctx.command)

        if ctx.author == member:
            return ctx.send("serio to sprawdzałeś?")

        if ctx.author <= member:
            return ctx.send("Nie możesz odmutować osoby równej lub wyższej od ciebie")

        guilds = read_json("guilds")

        member.remove_role(guilds[ctx.guild.id]["mute_role"])
        member.send(f"Zostałeś odmutowany na serwerze `{ctx.guild.name}` przez `{ctx.author.username}`")
        ctx.send("Odmutowano użytkownika")

    @modules.command(description="Daje ostrzeżenie", usage="warn (osoba) [powód]")
    def warn(self, ctx, member: Member, reason = "nie podano"):
        if not has_permission(ctx):
            raise NoPermission(f"{ctx.author.id} has no {ctx.command} permission", ctx.command)

        if reason == "nie podano":
            ctx.args[1:] = reason.split(" ")

        if ctx.author == member:
            return ctx.send("Nie możesz dać warna samemu sobie")

        if ctx.author <= member:
            return ctx.send("Nie możesz dać warna osobie równej lub wyższej od ciebie")

        guilds = read_json("guilds")

        if not "warns" in guilds[ctx.guild.id]:
            guilds[ctx.guild.id]["warns"] = {}

        if not member.id in guilds[ctx.guild.id]["warns"]:
            guilds[ctx.guild.id]["warns"][member.id] = []

        guilds[ctx.guild.id]["warns"][member.id].append(' '.join(ctx.args[1:]))

        if "warnsevent" in guilds[ctx.guild.id] and "kick" in guilds[ctx.guild.id]["warnsevent"] and guilds[ctx.guild.id]["warnsevent"]["kick"] == str(len(guilds[ctx.guild.id]["warns"][member.id])): 
            member.kick(" ".join(ctx.args[1:]))
            member.send(f"Zostałeś wyrzucony z serwera `{ctx.guild.name}` przez `{ctx.author.username}` z powodu `{' '.join(ctx.args[1:])}`")
            ctx.send(f"Wyrzucono użytkownika `{member.username}` z powodu `{' '.join(ctx.args[1:])}`")

        elif "warnsevent" in guilds[ctx.guild.id] and "ban" in guilds[ctx.guild.id]["warnsevent"] and guilds[ctx.guild.id]["warnsevent"]["ban"] == str(len(guilds[ctx.guild.id]["warns"][member.id])): 
            member.ban(" ".join(ctx.args[1:]))
            member.send(f"Zostałeś zbanowany na serwerze `{ctx.guild.name}` przez `{ctx.author.username}` z powodu `{' '.join(ctx.args[1:])}`")
            ctx.send(f"Zbanowano użytkownika `{ctx.data['mentions'][0]['username']}` z powodu `{' '.join(ctx.args[1:])}`")

        elif "warnsevent" in guilds[ctx.guild.id] and "mute" in guilds[ctx.guild.id]["warnsevent"] and guilds[ctx.guild.id]["warnsevent"]["mute"] == str(len(guilds[ctx.guild.id]["warns"][member.id])): 
            if not "mute_role" in guilds[ctx.guild.id]:
                role = ctx.guild.create_role("muted").json()

                guilds[ctx.guild.id]["mute_role"] = role["id"]

                for _, channel in ctx.guild.channels.items():
                    if channel.type == 0:
                        channel.edit_permissions(role["id"], {
                            "deny": PERMISSIONS["SEND_MESSAGES"],
                            "allow": PERMISSIONS["ADD_REACTIONS"],
                            "type": 0
                        })

                    elif channel.type == 2:
                        channel.edit_permissions(role["id"], {
                            "deny": PERMISSIONS["SPEAK"],
                            "allow": PERMISSIONS["VIEW_CHANNEL"],
                            "type": 0
                        })

                member.add_role(guilds[ctx.guild.id]["mute_role"])
                member.send(f"Zostałeś zmutowany na serwerze `{ctx.guild.name}` przez `{ctx.author.username}` z powodu `{' '.join(ctx.args[1:])}`")
                ctx.send("Zmutowano użytkownika")

        member.send(f"Dostałeś ostrzeżenie na serwerze `{ctx.guild.name}` przez `{ctx.author.username}` z powodu `{' '.join(ctx.args[1:])}`")
        ctx.send(f"Użytkownik `{member.username}` dostał ostrzeżenie z powodu `{' '.join(ctx.args[1:])}`")

        write_json("guilds", guilds)

    @modules.command(description="Pokazuje ostrzeżena", usage="warns (osoba)")
    def warns(self, ctx, member: Member):
        if not has_permission(ctx):
            raise NoPermission(f"{ctx.author.id} has no {ctx.command} permission", ctx.command)

        guilds = read_json("guilds")

        embed = Embed(title=f"Warny użytkownika {member.username}:", description="\n".join([f"{guilds[ctx.guild.id]['warns'][member.id].index(i)}. {i}" for i in guilds[ctx.guild.id]["warns"][member.id]]), color=0xe74c3c)
        ctx.send(embed=embed)

    @modules.command(description="Usuwa ostrzeżenie", usage="removewarn (osoba) (index)")
    def removewarn(self, ctx, member: Member, index: int):
        if not has_permission(ctx):
            raise NoPermission(f"{ctx.author.id} has no {ctx.command} permission", ctx.command)

        if ctx.author == member:
            return ctx.send("Nie możesz usunąć warna samemu siebie")

        if ctx.author <= member:
            return ctx.send("Nie możesz usunąć warna osobie równej lub wyższej od ciebie")

        guilds = read_json("guilds")

        del guilds[ctx.guild.id]["warns"][member.id][index]

        ctx.send("Usunięto ostrzeżenie")

        write_json("guilds", guilds)

    @modules.command(description="Usuwa ostrzeżenie", usage="clearwarns (osoba)")
    def clearwarns(self, ctx, member: Member):
        if not has_permission(ctx):
            raise NoPermission(f"{ctx.author.id} has no {ctx.command} permission", ctx.command)

        if ctx.author == member:
            return ctx.send("Nie możesz wyczyścic warnów samemu siebie")

        if ctx.author <= member:
            return ctx.send("Nie możesz wyczyscić warnów osobie równej lub wyższej od ciebie")

        guilds = read_json("guilds")

        del guilds[ctx.guild.id]["warns"][member.id]

        ctx.send("Wyczyszczono ostrzeżenia")

        write_json("guilds", guilds)

    @modules.command(description="Dodaje event na X warnów", usage="warnsevent (kick/ban/mute) (ilość)")
    def warnsevent(self, ctx, event: is_in("kick", "ban", "mute"), amount):
        if not has_permission(ctx):
            raise NoPermission(f"{ctx.author.id} has no {ctx.command} permission", ctx.command)

        guilds = read_json("guilds")

        if not "warnsevent" in guilds[ctx.guild.id]:
            guilds[ctx.guild.id]["warnsevent"] = {}

        guilds[ctx.guild.id]["warnsevent"][event] = amount

        ctx.send("Dodano event")

        write_json("guilds", guilds)

    @modules.command(description="Usuwa event na X warnów", usage="removewarnsevent (kick/ban/mute)")
    def removewarnsevent(self, ctx, event: is_in("kick", "ban", "mute")):
        if not has_permission(ctx):
            raise NoPermission(f"{ctx.author.id} has no {ctx.command} permission", ctx.command)

        guilds = read_json("guilds")

        del guilds[ctx.guild.id]["warnsevent"][event]

        ctx.send("Usunięto event")

        write_json("guilds", guilds)

    @modules.command(description="Dodaje kanał na którym będzie można przeklinać", usage="badwordsaddchannel (kanał)")
    def badwordsaddchannel(self, ctx, channel: find_working(Channel, Channel = lambda channel: channel.type == "GUILD_TEXT")):
        if not has_permission(ctx):
            raise NoPermission(f"{ctx.author.id} has no {ctx.command} permission", ctx.command)

        guilds = read_json("guilds")

        if not "badword_channels" in guilds[ctx.guild.id]:
            guilds[ctx.guild.id]["badword_channels"] = []

        guilds[ctx.guild.id]["badword_channels"].append(channel.id)

        ctx.send("Dodano kanał")

        write_json("guilds", guilds)

    @modules.command(description="Usuwa kanał na którym można przeklinać", usage="badwordsremovechannel (kanał)")
    def badwordsremovechannel(self, ctx, channel: find_working(Channel, Channel = lambda channel: channel.type == "GUILD_TEXT")):
        if not has_permission(ctx):
            raise NoPermission(f"{ctx.author.id} has no {ctx.command} permission", ctx.command)

        guilds = read_json("guilds")

        guilds[ctx.guild.id]["badword_channels"].remove(channel.id)

        ctx.send("Usunięto kanał")

        write_json("guilds", guilds)

    @modules.command(description="Dodaje kanał na którym będzie można wysyłać zaproszenia", usage="invitesaddchannel (kanał)")
    def invitesaddchannel(self, ctx, channel: find_working(Channel, Channel = lambda channel: channel.type == "GUILD_TEXT")):
        if not has_permission(ctx):
            raise NoPermission(f"{ctx.author.id} has no {ctx.command} permission", ctx.command)

        guilds = read_json("guilds")

        if not "invites_channels" in guilds[ctx.guild.id]:
            guilds[ctx.guild.id]["invites_channels"] = []

        guilds[ctx.guild.id]["invites_channels"].append(channel.id)

        ctx.send("Dodano kanał")

        write_json("guilds", guilds)

    @modules.command(description="Usuwa kanał na którym można wysyłać zaproszenia", usage="invitesremovechannel (kanał)")
    def invitesremovechannel(self, ctx, channel: find_working(Channel, Channel = lambda channel: channel.type == "GUILD_TEXT")):
        if not has_permission(ctx):
            raise NoPermission(f"{ctx.author.id} has no {ctx.command} permission", ctx.command)

        guilds = read_json("guilds")

        guilds[ctx.guild.id]["invites_channels"].remove(channel.id)

        ctx.send("Usunięto kanał")

        write_json("guilds", guilds)

    @modules.command(description="Dodaje kanał na którym będzie można przeklinać", usage="badwordsaddrole (rola)")
    def badwordsaddrole(self, ctx, role: Role):
        if not has_permission(ctx):
            raise NoPermission(f"{ctx.author.id} has no {ctx.command} permission", ctx.command)

        guilds = read_json("guilds")

        if not "badword_roles" in guilds[ctx.guild.id]:
            guilds[ctx.guild.id]["badword_roles"] = []

        guilds[ctx.guild.id]["badword_roles"].append(role.id)

        ctx.send("Dodano role")

        write_json("guilds", guilds)

    @modules.command(description="Usuwa role która może przeklinać", usage="badwordsremoverole (rola)")
    def badwordsremoverole(self, ctx, role: Role):
        if not has_permission(ctx):
            raise NoPermission(f"{ctx.author.id} has no {ctx.command} permission", ctx.command)

        guilds = read_json("guilds")

        guilds[ctx.guild.id]["badword_roles"].remove(role.id)

        ctx.send("Usunięto role")

        write_json("guilds", guilds)

    @modules.command(description="Dodaje role która będzie mogła wysyłać zaproszenia", usage="invitesaddrole (rola)")
    def invitesaddrole(self, ctx, role: Role):
        if not has_permission(ctx):
            raise NoPermission(f"{ctx.author.id} has no {ctx.command} permission", ctx.command)

        guilds = read_json("guilds")

        if not "invites_roles" in guilds[ctx.guild.id]:
            guilds[ctx.guild.id]["invites_roles"] = []

        guilds[ctx.guild.id]["invites_roles"].append(role.id)

        ctx.send("Dodano role")

        write_json("guilds", guilds)

    @modules.command(description="Usuwa role która może wysyłać zaproszenia", usage="invitesremoverole (rola)")
    def invitesremoverole(self, ctx, role: Role):
        if not has_permission(ctx):
            raise NoPermission(f"{ctx.author.id} has no {ctx.command} permission", ctx.command)

        guilds = read_json("guilds")

        guilds[ctx.guild.id]["invites_roles"].remove(role.id)

        ctx.send("Usunięto role")

        write_json("guilds", guilds)