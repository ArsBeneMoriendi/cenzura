import functions
import handler
import functions
import lib.permissions as permissions
import lib.flags as flags
from datetime import datetime

def load(bot, discord):
    @bot.command(description="Wywala osobe z serwera", usage="kick (osoba) [powód]", category="Admin", _default=False)
    def kick(ctx):
        if not functions.has_permission(ctx):
            return handler.error_handler(ctx, "nopermission", ctx.command)

        if not len(ctx.data["mentions"]) == 1:
            return handler.error_handler(ctx, "arguments", "kick (osoba) [powód]")

        if len(ctx.args) >= 2:
            ctx.args = " ".join(ctx.args[1:])
            reason = ctx.args
        else:
            reason = "nie podano powodu"

        status = discord.remove_guild_member(ctx.data["guild_id"], ctx.data["mentions"][0]["id"])
        
        if not status.status_code == 204:
            return handler.error_handler(ctx, 6)

        discord.create_message(ctx.data["channel_id"], {
            "content": f"Wyrzucono użytkownika `{ctx.data['mentions'][0]['username']}` z powodu `{reason}`".replace("@", "@\u200b")
        })

    @bot.command(description="Banuje osobe na serwerze", usage="ban (osoba) [powód]", category="Admin", _default=False)
    def ban(ctx):
        if not functions.has_permission(ctx):
            return handler.error_handler(ctx, "nopermission", ctx.command)

        if not len(ctx.data["mentions"]) == 1:
            return handler.error_handler(ctx, "arguments", "ban (osoba) [powód]")

        if len(ctx.args) >= 2:
            ctx.args = " ".join(ctx.args[1:])
            reason = ctx.args
        else:
            reason = "nie podano powodu"

        status = discord.create_guild_ban(ctx.data["guild_id"], ctx.data["mentions"][0]["id"], reason)
        
        if not status.status_code == 204:
            return handler.error_handler(ctx, 6)

        discord.create_message(ctx.data["channel_id"], {
            "content": f"Zbanowano użytkownika `{ctx.data['mentions'][0]['username']}` z powodu `{reason}`".replace("@", "@\u200b")
        })

    @bot.command(description="Usuwa wiadomości na kanale", usage="clear (ilość wiadomości 1-99) [osoba]", category="Admin", _default=False)
    def clear(ctx):
        if not functions.has_permission(ctx):
            return handler.error_handler(ctx, "nopermission", ctx.command)

        try:
            ctx.args[0] = int(ctx.args[0]) + 1
        except:
            return handler.error_handler(ctx, "arguments", "clear (ilość wiadomości 1-99) [osoba]")

        if not len(ctx.args) <= 1 and int(ctx.args[0]) > 100:
            return handler.error_handler(ctx, "arguments", "clear (ilość wiadomości 1-99) [osoba]")

        messages = list(map(lambda x: x["id"], discord.get_messages(ctx.data["channel_id"], ctx.args[0])))

        if len(ctx.data["mentions"]) == 1:
            x = []
            ctx.args[0] = int(ctx.args[0]) - 1
            for message in messages:
                message = discord.get_message(ctx.data["channel_id"], message)
                if "author" in message and message["author"]["id"] == ctx.data["mentions"][0]["id"]:
                    x.append(message["id"])

            messages = x
            message = f"Usunięto `{ctx.args[0]}` wiadomości użytkownika `{ctx.data['mentions'][0]['username']}`"
        else:
            message = f"Usunięto `{ctx.args[0]}` wiadomości"

        bulk_delete = discord.bulk_delete_messages(ctx.data["channel_id"], {
            "messages": messages
        })

        if not bulk_delete.status_code == 204:
            return handler.error_handler(ctx, 8)

        discord.create_message(ctx.data["channel_id"], {
            "content": message
        })

    @bot.command(description="Pokazuje informacje o użytkowniku", usage="userinfo [osoba]", category="Admin", _default=True)
    def userinfo(ctx):
        if not functions.has_permission(ctx):
            return handler.error_handler(ctx, "nopermission", ctx.command)

        if not len(ctx.data["mentions"]) == 1:
            user = discord.get_guild_member(ctx.data["guild_id"], ctx.data["author"]["id"])
        else:
            user = discord.get_guild_member(ctx.data["guild_id"], ctx.data["mentions"][0]["id"])
            
        user["joined_at"] = user["joined_at"].split("T")

        roles = discord.get_guild(ctx.data["guild_id"])["roles"]
        roles = [role["name"] for role in roles if role["id"] in user["roles"]]

        discord.create_message(ctx.data["channel_id"], {
            "embed": {
                "title": f"Informacje o {user['user']['username']}{' (BOT)' if 'bot' in user['user'] else ''}:",
                "color": 0xe74c3c,
                "fields": [
                    {
                        "name": "ID:",
                        "value": user["user"]["id"],
                        "inline": False
                    },
                    {
                        "name": "Nick z tagiem:",
                        "value": user["user"]["username"] + "#" + user["user"]["discriminator"],
                        "inline": False
                    },
                    {
                        "name": "Role:",
                        "value": ", ".join(roles),
                        "inline": False
                    },
                    {
                        "name": "Dołączył na serwer:",
                        "value": user["joined_at"][0] + " " + user["joined_at"][1].split(".")[0],
                        "inline": False
                    },
                    {
                        "name": "Utworzył konto:",
                        "value": str(datetime.fromtimestamp(((int(ctx.data["author"]["id"]) >> 22) + 1420070400000) / 1000)).split(".")[0],
                        "inline": False
                    },
                    {
                        "name": "Odznaki:",
                        "value": ", ".join(flags.user_flags(user["user"]["public_flags"])),
                        "inline": False
                    }
                ],
                "thumbnail": {
                    "url": f"http://cdn.discordapp.com/avatars/{user['user']['id']}/{user['user']['avatar']}.png?size=2048"
                }
            }
        })

    @bot.command(description="Pokazuje informacje o serwerze", usage="serverinfo", category="Admin", _default=True)
    def serverinfo(ctx):
        if not functions.has_permission(ctx):
            return handler.error_handler(ctx, "nopermission", ctx.command)

        guild = ctx.guilds[ctx.data["guild_id"]]

        discord.create_message(ctx.data["channel_id"], {
            "embed": {
                "title": f"Informacje o {guild['name']}:",
                "color": 0xe74c3c,
                "fields": [
                    {
                        "name": "Właściciel:",
                        "value": f"<@{guild['owner_id']}> ({guild['owner_id']})",
                        "inline": False
                    },
                    {
                        "name": "ID:",
                        "value": ctx.data["guild_id"],
                        "inline": False
                    },
                    {
                        "name": "Ilość osób:",
                        "value": guild["member_count"],
                        "inline": False
                    },
                    {
                        "name": "Ilość kanałów:",
                        "value": len(guild["channels"]),
                        "inline": False
                    },
                    {
                        "name": "Ilość ról:",
                        "value": len(guild["roles"]),
                        "inline": False
                    },
                    {
                        "name": "Ilość emotek:",
                        "value": len(guild["emojis"]),
                        "inline": False
                    },
                    {
                        "name": "Został stworzony:",
                        "value": str(datetime.fromtimestamp(((int(ctx.data["guild_id"]) >> 22) + 1420070400000) / 1000)).split(".")[0],
                        "inline": False
                    },
                    {
                        "name": "Boosty:",
                        "value": f"{guild['premium_subscription_count']} boosty / {guild['premium_tier']} poziom",
                        "inline": False
                    }
                ],
                "thumbnail": {
                    "url": f"https://cdn.discordapp.com/icons/{ctx.data['guild_id']}/{guild['icon']}.png?size=2048"
                }
            }
        })

    @bot.command(description="Pokazuje pomoc komendy set", usage="set", category="Admin", _default=False)
    def _set(ctx):
        if not functions.has_permission(ctx):
            return handler.error_handler(ctx, "nopermission", ctx.command)

        if not ctx.args:
            return discord.create_message(ctx.data["channel_id"], {
                "embed": {
                    "title": "Komendy set:",
                    "description": "> `set prefix (prefix)`, `set welcomemsg (kanał) (tekst)`, `set offwelcomemsg`, `set leavemsg (kanał) (tekst)`, `set offleavemsg`, `set autorole (rola)`, `set offautorole`, `set onbadwords`, `set offbadwords`, `set oninvites`, `set offinvites`",
                    "color": 0xe74c3c,
                    "footer": {
                        "text": "<> = nick osoby, [] = wzmianka, {} = licznik osób"
                    }
                }
            })

        guild = ctx.data["guild_id"]
        guilds = functions.read_json("guilds")

        if ctx.args[0] == "prefix":
            if not len(ctx.args) == 2:
                return handler.error_handler(ctx, "arguments", "set prefix (prefix)")

            guilds[guild]["prefix"] = ctx.args[1]

            discord.create_message(ctx.data["channel_id"], {
                "content": f"Ustawiono prefix na `{ctx.args[1]}`"
            })

        elif ctx.args[0] == "welcomemsg":
            if not len(ctx.args) >= 2:
                return handler.error_handler(ctx, "arguments", "set welcomemsg (kanał) (tekst)")

            guilds[guild]["welcomemsg"] = {}
            guilds[guild]["welcomemsg"]["channel_id"] = ctx.args[1].replace("<", "").replace("#", "").replace(">", "")
            guilds[guild]["welcomemsg"]["text"] = " ".join(ctx.args[2:])

            discord.create_message(ctx.data["channel_id"], {
                "content": "Ustawiono wiadomość powitalną"
            })

        elif ctx.args[0] == "offwelcomemsg":
            del guilds[guild]["welcomemsg"]

            discord.create_message(ctx.data["channel_id"], {
                "content": "Usunięto wiadomość powitalną"
            })

        elif ctx.args[0] == "leavemsg":
            if not len(ctx.args) >= 2:
                return handler.error_handler(ctx, "arguments", "set leavemsg (kanał) (tekst)")

            guilds[guild]["leavemsg"] = {}
            guilds[guild]["leavemsg"]["channel_id"] = ctx.args[1].replace("<", "").replace("#", "").replace(">", "")
            guilds[guild]["leavemsg"]["text"] = " ".join(ctx.args[2:])

            discord.create_message(ctx.data["channel_id"], {
                "content": "Ustawiono wiadomość pożegnalną"
            })

        elif ctx.args[0] == "offleavemsg":
            del guilds[guild]["leavemsg"]
            
            discord.create_message(ctx.data["channel_id"], {
                "content": "Usunięto wiadomość pożegnalną"
            })

        elif ctx.args[0] == "autorole":
            if not len(ctx.data["mention_roles"]) == 1:
                return handler.error_handler(ctx, "arguments", "set autorole (rola)")

            guilds[guild]["autorole"] = ctx.data["mention_roles"][0]

            discord.create_message(ctx.data["channel_id"], {
                "content": "Ustawiono autorole"
            })

        elif ctx.args[0] == "offautorole":
            del guilds[guild]["autorole"]
            
            discord.create_message(ctx.data["channel_id"], {
                "content": "Usunięto autorole"
            })

        elif ctx.args[0] == "onbadwords":
            guilds[guild]["badwords"] = True

            discord.create_message(ctx.data["channel_id"], {
                "content": "Włączono brzydkie słowa na tym serwerze"
            })

        elif ctx.args[0] == "offbadwords":
            del guilds[guild]["badwords"]

            discord.create_message(ctx.data["channel_id"], {
                "content": "Wyłączono brzydkie słowa na tym serwerze"
            })

        elif ctx.args[0] == "oninvites":
            guilds[guild]["invites"] = True

            discord.create_message(ctx.data["channel_id"], {
                "content": "Włączono wysyłanie zaproszeń na tym serwerze"
            })

        elif ctx.args[0] == "offinvites":
            del guilds[guild]["invites"]

            discord.create_message(ctx.data["channel_id"], {
                "content": "Wyłączono wysyłanie zaproszeń na tym serwerze"
            })

        functions.write_json("guilds", guilds)

    @bot.command(description="Mutuje użytkownika", usage="mute (osoba)", category="Admin", _default=False)
    def mute(ctx):
        if not functions.has_permission(ctx):
            return handler.error_handler(ctx, "nopermission", ctx.command)
        
        if not len(ctx.args) == 1:
            return handler.error_handler(ctx, "arguments", "mute (osoba)")

        guild = ctx.data["guild_id"]
        guilds = functions.read_json("guilds")

        if not "mute_role" in guilds[guild]:
            role = discord.create_guild_role(guild, {
                "name": "muted"
            }).json()

            guilds[guild]["mute_role"] = role["id"]
            
            channels = discord.get_guild_channels(guild)
            for channel in channels:
                if channel["type"] == 0:
                    a = discord.edit_channel_permissions(channel["id"], role["id"], {
                        "deny": permissions.permissions["SEND_MESSAGES"],
                        "allow": permissions.permissions["ADD_REACTIONS"],
                        "type": 0
                    })
                elif channel["type"] == 2:
                    discord.edit_channel_permissions(channel["id"], role["id"], {
                        "deny": permissions.permissions["SPEAK"],
                        "allow": permissions.permissions["VIEW_CHANNEL"],
                        "type": 0
                    })

            functions.write_json("guilds", guilds)

        status = discord.add_guild_member_role(guild, ctx.data["mentions"][0]["id"], guilds[guild]["mute_role"])

        if not status.status_code == 204:
            return handler.error_handler(ctx, 6)

        discord.create_message(ctx.data["channel_id"], {
            "content": "Zmutowano użytkownika"
        })

    @bot.command(description="Odmutuje użytkownika", usage="unmute (osoba)", category="Admin", _default=False)
    def unmute(ctx):
        if not functions.has_permission(ctx):
            return handler.error_handler(ctx, "nopermission", ctx.command)
        
        if not len(ctx.args) == 1:
            return handler.error_handler(ctx, "arguments", "unmute (osoba)")

        guild = ctx.data["guild_id"]
        guilds = functions.read_json("guilds")

        if not "mute_role" in guilds[guild]:
            return handler.error_handler(ctx, "notfound")

        status = discord.remove_guild_member_role(guild, ctx.data["mentions"][0]["id"], guilds[guild]["mute_role"])

        if not status.status_code == 204:
            return handler.error_handler(ctx, 6)

        discord.create_message(ctx.data["channel_id"], {
            "content": "Odmutowano użytkownika"
        })

    @bot.command(description="Daje ostrzeżenie", usage="warn (osoba) [powód]", category="Admin", _default=False)
    def warn(ctx):
        if not functions.has_permission(ctx):
            return handler.error_handler(ctx, "nopermission", ctx.command)

        if not len(ctx.data["mentions"]) == 1:
            return handler.error_handler(ctx, "arguments", "warn (osoba) [powód]")

        if len(ctx.args) >= 2:
            ctx.args = " ".join(ctx.args[1:])
            reason = ctx.args
        else:
            reason = "nie podano powodu"

        guild = ctx.data["guild_id"]
        guilds = functions.read_json("guilds")

        if not "warns" in guilds[guild]:
            guilds[guild]["warns"] = {}

        if not ctx.data["mentions"][0]["id"] in guilds[guild]["warns"]:
            guilds[guild]["warns"][ctx.data["mentions"][0]["id"]] = []

        guilds[guild]["warns"][ctx.data["mentions"][0]["id"]].append(reason)

        if "warnsevent" in guilds[guild] and "kick" in guilds[guild]["warnsevent"] and guilds[guild]["warnsevent"]["kick"] == str(len(guilds[guild]["warns"][ctx.data["mentions"][0]["id"]])): 
            status = discord.remove_guild_member(ctx.data["guild_id"], ctx.data["mentions"][0]["id"])
            if not status.status_code == 204:
                return handler.error_handler(ctx, 6)

            discord.create_message(ctx.data["channel_id"], {
                "content": f"Wyrzucono użytkownika `{ctx.data['mentions'][0]['username']}`"
            })

        elif "warnsevent" in guilds[guild] and "ban" in guilds[guild]["warnsevent"] and guilds[guild]["warnsevent"]["ban"] == str(len(guilds[guild]["warns"][ctx.data["mentions"][0]["id"]])): 
            status = discord.create_guild_ban(ctx.data["guild_id"], ctx.data["mentions"][0]["id"], reason)
            if not status.status_code == 204:
                return handler.error_handler(ctx, 6)

            discord.create_message(ctx.data["channel_id"], {
                "content": f"Zbanowano użytkownika `{ctx.data['mentions'][0]['username']}`"
            })

        elif "warnsevent" in guilds[guild] and "mute" in guilds[guild]["warnsevent"] and guilds[guild]["warnsevent"]["mute"] == str(len(guilds[guild]["warns"][ctx.data["mentions"][0]["id"]])): 
            if not "mute_role" in guilds[guild]:
                role = discord.create_guild_role(guild, {
                    "name": "muted"
                }).json()

                guilds[guild]["mute_role"] = role["id"]
                
                channels = discord.get_guild_channels(guild)
                for channel in channels:
                    if channel["type"] == 0:
                        a = discord.edit_channel_permissions(channel["id"], role["id"], {
                            "deny": permissions.permissions["SEND_MESSAGES"],
                            "allow": permissions.permissions["ADD_REACTIONS"],
                            "type": 0
                        })
                    elif channel["type"] == 2:
                        discord.edit_channel_permissions(channel["id"], role["id"], {
                            "deny": permissions.permissions["SPEAK"],
                            "allow": permissions.permissions["VIEW_CHANNEL"],
                            "type": 0
                        })

                status = discord.add_guild_member_role(guild, ctx.data["mentions"][0]["id"], guilds[guild]["mute_role"])

                if not status.status_code == 204:
                    return handler.error_handler(ctx, 6)

                discord.create_message(ctx.data["channel_id"], {
                    "content": "Zmutowano użytkownika"
                })

        discord.create_message(ctx.data["channel_id"], {
            "content": f"Użytkownik `{ctx.data['mentions'][0]['username']}` dostał ostrzeżenie z powodu `{reason}`".replace("@", "@\u200b")
        })

        functions.write_json("guilds", guilds)

    @bot.command(description="Pokazuje ostrzeżena", usage="warns (osoba)", category="Admin", _default=False)
    def warns(ctx):
        if not functions.has_permission(ctx):
            return handler.error_handler(ctx, "nopermission", ctx.command)

        if not len(ctx.data["mentions"]) == 1:
            return handler.error_handler(ctx, "arguments", "warns (osoba)")

        guild = ctx.data["guild_id"]
        guilds = functions.read_json("guilds")

        if not "warns" in guilds[guild] or not ctx.data["mentions"][0]["id"] in guilds[guild]["warns"]:
            return handler.error_handler(ctx, "notfound")

        discord.create_message(ctx.data["channel_id"], {
            "embed": {
                "title": f"Warny użytkownika {ctx.data['mentions'][0]['username']}:",
                "description": "\n".join([f"{guilds[guild]['warns'][ctx.data['mentions'][0]['id']].index(i)}. {i}" for i in guilds[guild]["warns"][ctx.data["mentions"][0]["id"]]]),
                "color": 0xe74c3c
            }
        })

    @bot.command(description="Usuwa ostrzeżenie", usage="removewarn (osoba) (id)", category="Admin", _default=False)
    def removewarn(ctx):
        if not functions.has_permission(ctx):
            return handler.error_handler(ctx, "nopermission", ctx.command)

        if not len(ctx.args) == 2:
            return handler.error_handler(ctx, "arguments", "removewarn (osoba) (id)")

        guild = ctx.data["guild_id"]
        guilds = functions.read_json("guilds")

        if not "warns" in guilds[guild] or not ctx.data["mentions"][0]["id"] in guilds[guild]["warns"]:
            return handler.error_handler(ctx, "notfound")

        del guilds[guild]["warns"][ctx.data["mentions"][0]["id"]][int(ctx.args[1])]

        discord.create_message(ctx.data["channel_id"], {
            "content": "Usunięto ostrzeżenie"
        })

        functions.write_json("guilds", guilds)

    @bot.command(description="Usuwa ostrzeżenie", usage="clearwarns (osoba)", category="Admin", _default=False)
    def clearwarns(ctx):
        if not functions.has_permission(ctx):
            return handler.error_handler(ctx, "nopermission", ctx.command)

        if not len(ctx.args) == 1:
            return handler.error_handler(ctx, "arguments", "clearwarns (osoba)")

        guild = ctx.data["guild_id"]
        guilds = functions.read_json("guilds")

        if not "warns" in guilds[guild] or not ctx.data["mentions"][0]["id"] in guilds[guild]["warns"]:
            return handler.error_handler(ctx, "notfound")

        del guilds[guild]["warns"][ctx.data["mentions"][0]["id"]]

        discord.create_message(ctx.data["channel_id"], {
            "content": "Wyczyszczono ostrzeżenia"
        })

        functions.write_json("guilds", guilds)

    @bot.command(description="Dodaje event na X warnów", usage="warnsevent (kick/ban/mute) (ilość warnów)", category="Admin", _default=False)
    def warnsevent(ctx):
        if not functions.has_permission(ctx):
            return handler.error_handler(ctx, "nopermission", ctx.command)

        if not len(ctx.args) == 2 or ctx.args[0] not in ["kick", "ban", "mute"]:
            return handler.error_handler(ctx, "arguments", "warnsevent (kick/ban/mute) (ilość warnów)")

        guild = ctx.data["guild_id"]
        guilds = functions.read_json("guilds")

        if not "warnsevent" in guilds[guild]:
            guilds[guild]["warnsevent"] = {}

        guilds[guild]["warnsevent"][ctx.args[0]] = str(ctx.args[1])

        discord.create_message(ctx.data["channel_id"], {
            "content": "Dodano event"
        })

        functions.write_json("guilds", guilds)

    @bot.command(description="Usuwa event na X warnów", usage="removewarnsevent (kick/ban/mute)", category="Admin", _default=False)
    def removewarnsevent(ctx):
        if not functions.has_permission(ctx):
            return handler.error_handler(ctx, "nopermission", ctx.command)

        if not len(ctx.args) == 1 or ctx.args[0] not in ["kick", "ban", "mute"]:
            return handler.error_handler(ctx, "arguments", "warnsevent (kick/ban/mute)")

        guild = ctx.data["guild_id"]
        guilds = functions.read_json("guilds")

        del guilds[guild]["warnsevent"][ctx.args[0]]

        discord.create_message(ctx.data["channel_id"], {
            "content": "Usunięto event"
        })

        functions.write_json("guilds", guilds)