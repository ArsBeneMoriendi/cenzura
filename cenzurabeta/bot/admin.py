import functions
import handler
import functions
import lib.permissions as permissions

def load(gateway, discord):
    @gateway.command(description="Wywala osobe z serwera", usage="kick (osoba) [powód]", category="Admin", _default=False)
    def kick(ctx):
        if not functions.has_permission(ctx):
            return handler.error_handler(ctx, "nopermission", ctx.command)

        if not len(ctx.data["mentions"]) == 1:
            return handler.error_handler(ctx, "arguments", "kick (osoba) [powód]")

        if len(ctx.args) >= 2:
            ctx.args = " ".join(ctx.args)
            reason = ctx.args
        else:
            reason = "nie podano powodu"

        status = discord.remove_guild_member(ctx.data["guild_id"], ctx.data["mentions"][0]["id"])
        
        if not status.status_code == 204:
            return handler.error_handler(ctx, 6)

        discord.create_message(ctx.data["channel_id"], {
            "content": f"Wyrzucono użytkownika `{ctx.data['mentions'][0]['username']}` z powodu `{reason}`".replace("@", "@\u200b")
        })

    @gateway.command(description="Banuje osobe na serwerze", usage="ban (osoba) [powód]", category="Admin", _default=False)
    def ban(ctx):
        if not functions.has_permission(ctx):
            return handler.error_handler(ctx, "nopermission", ctx.command)

        if not len(ctx.data["mentions"]) == 1:
            return handler.error_handler(ctx, "arguments", "ban (osoba) [powód]")

        if len(ctx.args) >= 2:
            ctx.args = " ".join(ctx.args)
            reason = ctx.args
        else:
            reason = "nie podano powodu"

        status = discord.create_guild_ban(ctx.data["guild_id"], ctx.data["mentions"][0]["id"], reason)
        
        if not status.status_code == 204:
            return handler.error_handler(ctx, 6)

        discord.create_message(ctx.data["channel_id"], {
            "content": f"Zbanowano użytkownika `{ctx.data['mentions'][0]['username']}` z powodu `{reason}`".replace("@", "@\u200b")
        })

    @gateway.command(description="Usuwa wiadomości na kanale", usage="clear (ilość wiadomości 1-99)", category="Admin", _default=False)
    def clear(ctx):
        if not functions.has_permission(ctx):
            return handler.error_handler(ctx, "nopermission", ctx.command)

        if not len(ctx.args) == 1 or int(ctx.args[0]) >= 100:
            return handler.error_handler(ctx, "arguments", "clear (ilość wiadomości 1-99)")

        ctx.args[0] = int(ctx.args[0]) + 1

        messages = list(map(lambda x: x["id"], discord.get_messages(ctx.data["channel_id"], ctx.args[0])))
        bulk_delete = discord.bulk_delete_messages(ctx.data["channel_id"], {
            "messages": messages
        })

        discord.create_message(ctx.data["channel_id"], {
            "content": f"Usunięto `{ctx.args[0]}` wiadomości"
        })

    @gateway.command(description="Pokazuje informacje o użytkowniku", usage="userinfo [osoba]", category="Admin", _default=True)
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
                    }
                ],
                "thumbnail": {
                    "url": f"http://cdn.discordapp.com/avatars/{user['user']['id']}/{user['user']['avatar']}.png?size=2048"
                }
            }
        })

    @gateway.command(description="Pokazuje informacje o serwerze", usage="serverinfo", category="Admin", _default=True)
    def serverinfo(ctx):
        if not functions.has_permission(ctx):
            return handler.error_handler(ctx, "nopermission", ctx.command)

        guild = discord.get_guild(ctx.data["guild_id"])
        members = discord.list_guild_members(ctx.data["guild_id"])
        channels = discord.get_guild_channels(ctx.data["guild_id"])

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
                        "value": len(members),
                        "inline": False
                    },
                    {
                        "name": "Ilość kanałów:",
                        "value": len(channels),
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
                    }
                ],
                "thumbnail": {
                    "url": f"https://cdn.discordapp.com/icons/{ctx.data['guild_id']}/{guild['icon']}.png?size=2048"
                }
            }
        })

    @gateway.command(description="Pokazuje pomoc komendy set", usage="set", category="Admin", _default=False)
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

    @gateway.command(description="Mutuje użytkownika", usage="mute (osoba)", category="Admin", _default=False)
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

    @gateway.command(description="Odmutuje użytkownika", usage="unmute (osoba)", category="Admin", _default=False)
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