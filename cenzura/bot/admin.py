from lib import modules
from lib.ctx import ctx
import functions
import handler
from functions import *
from lib.permissions import PERMISSIONS
from lib.embed import Embed
from lib.errors import NoPermission, InvalidArgumentType
from lib.types import Member, Channel, Role

@modules.module
class Admin(ctx):
    def __init__(self, bot, discord):
        self.bot = bot
        self.discord = discord
        
    @modules.command(description="Wywala osobe z serwera", usage="kick (osoba) [powód]")
    def kick(self, member: Member, reason = "nie podano"):
        if not has_permission(self):
            raise NoPermission(f"{self.author.id} has no {self.command} permission", self.command)

        if reason == "nie podano":
            self.args[1:] = reason.split(" ")

        if self.author == member:
            return self.send("Nie możesz wyrzucić samego siebie")

        if self.author <= member:
            return self.send("Nie możesz wyrzucić osoby równej lub wyższej od ciebie")

        member.kick(' '.join(self.args[1:]))
        self.send(f"Wyrzucono użytkownika `{member.username}` z powodu `{' '.join(self.args[1:])}`")

    @modules.command(description="Banuje osobe na serwerze", usage="ban (osoba) [powód]")
    def ban(self, member: Member, reason = "nie podano"):
        if not has_permission(self):
            raise NoPermission(f"{self.author.id} has no {self.command} permission", self.command)

        if reason == "nie podano":
            self.args[1:] = reason.split(" ")

        if self.author == member:
            return self.send("Nie możesz zbanować samego siebie")

        if self.author <= member:
            return self.send("Nie możesz zbanować osoby równej lub wyższej od ciebie")

        member.ban(' '.join(self.args[1:]))
        self.send(f"Zbanowano użytkownika `{member.username}` z powodu `{' '.join(self.args[1:])}`")

    @modules.command(description="Usuwa wiadomości na kanale", usage="clear (2-99)")
    def clear(self, amount: between(2, 99)):
        if not has_permission(self):
            raise NoPermission(f"{self.author.id} has no {self.command} permission", self.command)

        amount += 1
        messages = [x["id"] for x in discord.get_messages(self.channel.id, amount)]
        self.channel.clear(messages)

    @modules.command(description="Pokazuje pomoc komendy set", usage="set")
    def _set(self, subcommand = None, arg: find_working(Channel, Role, str, Channel = lambda channel: channel.type == "GUILD_TEXT") = None, arg2 = None):
        if not has_permission(self):
            raise NoPermission(f"{self.author.id} has no {self.command} permission", self.command)

        help_embed = Embed(title="Komendy set:", description="> `set prefix (prefix)`, `set welcomemsg (kanał) (tekst)`, `set removewelcomemsg`, `set leavemsg (kanał) (tekst)`, `set removeleavemsg`, `set autorole (rola)`, `set removeautorole`, `set onbadwords`, `set offbadwords`, `set oninvites`, `set offinvites`", color=0xe74c3c)
        help_embed.set_footer(text="<> = nick osoby, [] = wzmianka, {} = licznik osób")

        if not subcommand:
            return self.send(embed=help_embed)

        guilds = read_json("guilds")

        if subcommand == "prefix":
            guilds[self.guild.id]["prefix"] = arg
            self.send(f"Ustawiono prefix na `{arg}`")

        elif subcommand == "welcomemsg":
            if not isinstance(arg, Channel) or not arg2:
                return self.send(embed=help_embed)

            guilds[self.guild.id]["welcomemsg"] = {}
            guilds[self.guild.id]["welcomemsg"]["channel_id"] = arg.id
            guilds[self.guild.id]["welcomemsg"]["text"] = " ".join(self.args[2:])

            self.send("Ustawiono wiadomość powitalną")

        elif subcommand == "removewelcomemsg":
            del guilds[self.guild.id]["welcomemsg"]
            self.send("Usunięto wiadomość powitalną")

        elif subcommand == "leavemsg":
            if not isinstance(arg, Channel) or not arg2:
                return self.send(embed=help_embed)

            guilds[self.guild.id]["leavemsg"] = {}
            guilds[self.guild.id]["leavemsg"]["channel_id"] = arg.id
            guilds[self.guild.id]["leavemsg"]["text"] = " ".join(self.args[2:])

            self.send("Ustawiono wiadomość pożegnalną")

        elif subcommand == "removeleavemsg":
            del guilds[self.guild.id]["leavemsg"]
            self.send("Usunięto wiadomość pożegnalną")

        elif subcommand == "autorole":
            if not isinstance(arg, Role):
                return self.send(embed=help_embed)

            guilds[self.guild.id]["autorole"] = arg.id
            self.send("Ustawiono autorole")

        elif subcommand == "removeautorole":
            del guilds[self.guild.id]["autorole"]
            self.send("Usunięto autorole")

        elif subcommand == "onbadwords":
            guilds[self.guild.id]["badwords"] = True
            self.send("Włączono brzydkie słowa na tym serwerze")

        elif subcommand == "offbadwords":
            del guilds[self.guild.id]["badwords"]
            self.send("Wyłączono brzydkie słowa na tym serwerze")

        elif subcommand == "oninvites":
            guilds[self.guild.id]["invites"] = True
            self.send("Włączono wysyłanie zaproszeń na tym serwerze")

        elif subcommand == "offinvites":
            del guilds[self.guild.id]["invites"]
            self.send("Wyłączono wysyłanie zaproszeń na tym serwerze")

        else:
            self.send(embed=help_embed)

        write_json("guilds", guilds)

    @modules.command(description="Mutuje użytkownika", usage="mute (osoba) [powód]")
    def mute(self, member: Member, reason = "nie podano"):
        if not has_permission(self):
            raise NoPermission(f"{self.author.id} has no {self.command} permission", self.command)

        if reason == "nie podano":
            self.args[1:] = reason.split(" ")

        if self.author == member:
            return self.send("Nie możesz zmutować samego siebie")

        if self.author <= member:
            return self.send("Nie możesz zmutować osoby równej lub wyższej od ciebie")

        guilds = read_json("guilds")

        if not "mute_role" in guilds[self.guild.id]:
            role = self.guild.create_role("muted").json()

            guilds[self.guild.id]["mute_role"] = role["id"]

            for _, channel in self.guild.channels.items():
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

        member.add_role(guilds[self.guild.id]["mute_role"])
        self.send(f"Zmutowano użytkownika `{member.username}` z powodu `{' '.join(self.args[1:])}`")

    @modules.command(description="Odmutuje użytkownika", usage="unmute (osoba)")
    def unmute(self, member: Member):
        if not has_permission(self):
            raise NoPermission(f"{self.author.id} has no {self.command} permission", self.command)

        if self.author == member:
            return self.send("serio to sprawdzałeś?")

        if self.author <= member:
            return self.send("Nie możesz odmutować osoby równej lub wyższej od ciebie")

        guilds = read_json("guilds")

        member.remove_role(guilds[self.guild.id]["mute_role"])
        self.send("Odmutowano użytkownika")

    @modules.command(description="Daje ostrzeżenie", usage="warn (osoba) [powód]")
    def warn(self, member: Member, reason = "nie podano"):
        if not has_permission(self):
            raise NoPermission(f"{self.author.id} has no {self.command} permission", self.command)

        if reason == "nie podano":
            self.args[1:] = reason.split(" ")

        if self.author == member:
            return self.send("Nie możesz dać warna samemu sobie")

        if self.author <= member:
            return self.send("Nie możesz dać warna osobie równej lub wyższej od ciebie")

        guilds = read_json("guilds")

        if not "warns" in guilds[self.guild.id]:
            guilds[self.guild.id]["warns"] = {}

        if not member.id in guilds[self.guild.id]["warns"]:
            guilds[self.guild.id]["warns"][member.id] = []

        guilds[self.guild.id]["warns"][member.id].append(' '.join(self.args[1:]))

        if "warnsevent" in guilds[self.guild.id] and "kick" in guilds[self.guild.id]["warnsevent"] and guilds[self.guild.id]["warnsevent"]["kick"] == str(len(guilds[self.guild.id]["warns"][member.id])): 
            member.kick(' '.join(self.args[1:]))
            self.send(f"Wyrzucono użytkownika `{member.username}` z powodu `{' '.join(self.args[1:])}`")

        elif "warnsevent" in guilds[self.guild.id] and "ban" in guilds[self.guild.id]["warnsevent"] and guilds[self.guild.id]["warnsevent"]["ban"] == str(len(guilds[self.guild.id]["warns"][member.id])): 
            member.ban(' '.join(self.args[1:]))
            self.send(f"Zbanowano użytkownika `{self.data['mentions'][0]['username']}` z powodu `{' '.join(self.args[1:])}`")

        elif "warnsevent" in guilds[self.guild.id] and "mute" in guilds[self.guild.id]["warnsevent"] and guilds[self.guild.id]["warnsevent"]["mute"] == str(len(guilds[self.guild.id]["warns"][member.id])): 
            if not "mute_role" in guilds[self.guild.id]:
                role = self.guild.create_role("muted").json()

                guilds[self.guild.id]["mute_role"] = role["id"]

                for _, channel in self.guild.channels.items():
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

                member.add_role(guilds[self.guild.id]["mute_role"])
                self.send("Zmutowano użytkownika")

        self.send(f"Użytkownik `{member.username}` dostał ostrzeżenie z powodu `{' '.join(self.args[1:])}`")

        write_json("guilds", guilds)

    @modules.command(description="Pokazuje ostrzeżena", usage="warns (osoba)")
    def warns(self, member: Member):
        if not has_permission(self):
            raise NoPermission(f"{self.author.id} has no {self.command} permission", self.command)

        guilds = read_json("guilds")

        embed = Embed(title=f"Warny użytkownika {member.username}:", description="\n".join([f"{guilds[self.guild.id]['warns'][member.id].index(i)}. {i}" for i in guilds[self.guild.id]["warns"][member.id]]), color=0xe74c3c)
        self.send(embed=embed)

    @modules.command(description="Usuwa ostrzeżenie", usage="removewarn (osoba) (index)")
    def removewarn(self, member: Member, index: int):
        if not has_permission(self):
            raise NoPermission(f"{self.author.id} has no {self.command} permission", self.command)

        if self.author == member:
            return self.send("Nie możesz usunąć warna samemu siebie")

        if self.author <= member:
            return self.send("Nie możesz usunąć warna osobie równej lub wyższej od ciebie")

        guilds = read_json("guilds")

        del guilds[self.guild.id]["warns"][member.id][index]

        self.send("Usunięto ostrzeżenie")

        write_json("guilds", guilds)

    @modules.command(description="Usuwa ostrzeżenie", usage="clearwarns (osoba)")
    def clearwarns(self, member: Member):
        if not has_permission(self):
            raise NoPermission(f"{self.author.id} has no {self.command} permission", self.command)

        if self.author == member:
            return self.send("Nie możesz wyczyścic warnów samemu siebie")

        if self.author <= member:
            return self.send("Nie możesz wyczyscić warnów osobie równej lub wyższej od ciebie")

        guilds = read_json("guilds")

        del guilds[self.guild.id]["warns"][member.id]

        self.send("Wyczyszczono ostrzeżenia")

        write_json("guilds", guilds)

    @modules.command(description="Dodaje event na X warnów", usage="warnsevent (kick/ban/mute) (ilość)")
    def warnsevent(self, event: is_in("kick", "ban", "mute"), amount):
        if not has_permission(self):
            raise NoPermission(f"{self.author.id} has no {self.command} permission", self.command)

        guilds = read_json("guilds")

        if not "warnsevent" in guilds[self.guild.id]:
            guilds[self.guild.id]["warnsevent"] = {}

        guilds[self.guild.id]["warnsevent"][event] = amount

        self.send("Dodano event")

        write_json("guilds", guilds)

    @modules.command(description="Usuwa event na X warnów", usage="removewarnsevent (kick/ban/mute)")
    def removewarnsevent(self, event: is_in("kick", "ban", "mute")):
        if not has_permission(self):
            raise NoPermission(f"{self.author.id} has no {self.command} permission", self.command)

        guilds = read_json("guilds")

        del guilds[self.guild.id]["warnsevent"][event]

        self.send("Usunięto event")

        write_json("guilds", guilds)

    @modules.command(description="Dodaje kanał na którym będzie można przeklinać", usage="badwordsaddchannel (kanał)")
    def badwordsaddchannel(self, channel: find_working(Channel, Channel = lambda channel: channel.type == "GUILD_TEXT")):
        if not has_permission(self):
            raise NoPermission(f"{self.author.id} has no {self.command} permission", self.command)

        guilds = read_json("guilds")

        if not "badword_channels" in guilds[self.guild.id]:
            guilds[self.guild.id]["badword_channels"] = []

        guilds[self.guild.id]["badword_channels"].append(channel.id)

        self.send("Dodano kanał")

        write_json("guilds", guilds)

    @modules.command(description="Usuwa kanał na którym można przeklinać", usage="badwordsremovechannel (kanał)")
    def badwordsremovechannel(self, channel: find_working(Channel, Channel = lambda channel: channel.type == "GUILD_TEXT")):
        if not has_permission(self):
            raise NoPermission(f"{self.author.id} has no {self.command} permission", self.command)

        guilds = read_json("guilds")

        guilds[self.guild.id]["badword_channels"].remove(channel.id)

        self.send("Usunięto kanał")

        write_json("guilds", guilds)

    @modules.command(description="Dodaje kanał na którym będzie można wysyłać zaproszenia", usage="invitesaddchannel (kanał)")
    def invitesaddchannel(self, channel: find_working(Channel, Channel = lambda channel: channel.type == "GUILD_TEXT")):
        if not has_permission(self):
            raise NoPermission(f"{self.author.id} has no {self.command} permission", self.command)

        guilds = read_json("guilds")

        if not "invites_channels" in guilds[self.guild.id]:
            guilds[self.guild.id]["invites_channels"] = []

        guilds[self.guild.id]["invites_channels"].append(channel.id)

        self.send("Dodano kanał")

        write_json("guilds", guilds)

    @modules.command(description="Usuwa kanał na którym można wysyłać zaproszenia", usage="invitesremovechannel (kanał)")
    def invitesremovechannel(self, channel: find_working(Channel, Channel = lambda channel: channel.type == "GUILD_TEXT")):
        if not has_permission(self):
            raise NoPermission(f"{self.author.id} has no {self.command} permission", self.command)

        guilds = read_json("guilds")

        guilds[self.guild.id]["invites_channels"].remove(channel.id)

        self.send("Usunięto kanał")

        write_json("guilds", guilds)

    @modules.command(description="Dodaje kanał na którym będzie można przeklinać", usage="badwordsaddrole (rola)")
    def badwordsaddrole(self, role: Role):
        if not has_permission(self):
            raise NoPermission(f"{self.author.id} has no {self.command} permission", self.command)

        guilds = read_json("guilds")

        if not "badword_roles" in guilds[self.guild.id]:
            guilds[self.guild.id]["badword_roles"] = []

        guilds[self.guild.id]["badword_roles"].append(role.id)

        self.send("Dodano role")

        write_json("guilds", guilds)

    @modules.command(description="Usuwa role która może przeklinać", usage="badwordsremoverole (rola)")
    def badwordsremoverole(self, role: Role):
        if not has_permission(self):
            raise NoPermission(f"{self.author.id} has no {self.command} permission", self.command)

        guilds = read_json("guilds")

        guilds[self.guild.id]["badword_roles"].remove(role.id)

        self.send("Usunięto role")

        write_json("guilds", guilds)

    @modules.command(description="Dodaje role która będzie mogła wysyłać zaproszenia", usage="invitesaddrole (rola)")
    def invitesaddrole(self, role: Role):
        if not has_permission(self):
            raise NoPermission(f"{self.author.id} has no {self.command} permission", self.command)

        guilds = read_json("guilds")

        if not "invites_roles" in guilds[self.guild.id]:
            guilds[self.guild.id]["invites_roles"] = []

        guilds[self.guild.id]["invites_roles"].append(role.id)

        self.send("Dodano role")

        write_json("guilds", guilds)

    @modules.command(description="Usuwa role która może wysyłać zaproszenia", usage="invitesremoverole (rola)")
    def invitesremoverole(self, role: Role):
        if not has_permission(self):
            raise NoPermission(f"{self.author.id} has no {self.command} permission", self.command)

        guilds = read_json("guilds")

        guilds[self.guild.id]["invites_roles"].remove(role.id)

        self.send("Usunięto role")

        write_json("guilds", guilds)