from .ctx import ctx
import requests
import config
import threading
import time
import json
from .embed import Embed
from .components import Components

session = requests.Session()

url = "https://discord.com/api/v9"
headers = {"authorization": f"Bot {config.token}"}

ratelimit = []

def dupa(resp, endpoint):
    time.sleep(resp["retry_after"])
    ratelimit.remove(endpoint)

def request(method, endpoint, data=None, files=None):
    if (url + endpoint) in ratelimit: return

    try:
        if files:
            resp = session.request(method, url + endpoint, headers=headers, data=data, files=files)
        else:
            resp = session.request(method, url + endpoint, headers=headers, json=data)

        if resp.status_code == 429:
            ratelimit.append(endpoint)
            threading.Thread(target=dupa, args=(resp.json(), endpoint)).start()
        
        return resp
    except:
        return

def get_channel(channel):
    return request("GET", "/channels/" + channel).json()

def modify_channel(channel, data):
    return request("PATCH", "/channels/" + channel, data)

def get_messages(channel, limit = 100):
    return request("GET", "/channels/" + channel + f"/messages?limit={limit}").json()

def get_message(channel, message):
    return request("GET", "/channels/" + channel + "/messages/" + message).json()

def send(channel, content = None, *, embed: Embed = None, components: Components = None, other_data: dict = None, files: list = None, reply = True, mentions: list = []):
    data = {}

    if reply and not files:
        data["allowed_mentions"] = {
            "parse": mentions,
            "users": [],
            "replied_user": False
        }

        data["message_reference"] = {
            "guild_id": ctx.data["guild_id"],
            "channel_id": ctx.data["channel_id"],
            "message_id": ctx.data["id"]
        }

    if content:
        data["content"] = content

    if embed:
        data["embed"] = embed.__dict__

    if components:
        data.update(components.__dict__)
    
    if other_data:
        data.update(other_data)

    return request("POST", "/channels/" + channel + "/messages", data, files)

def edit_message(channel, message, content = None, *, embed: Embed = None, other_data: dict = None):
    data = {}

    data["allowed_mentions"] = {
        "parse": ["users", "roles", "everyone"],
        "users": [],
        "replied_user": False
    }

    if content:
        data["content"] = content

    if embed:
        data["embed"] = embed.__dict__
    
    if other_data:
        data.update(other_data)

    return request("PATCH", "/channels/" + channel + "/messages/" + message, data)

def delete_message(channel, message):
    return request("DELETE", "/channels/" + channel + "/messages/" + message)

def bulk_delete_messages(channel, data):
    return request("POST", "/channels/" + channel + "/messages/bulk-delete", data)

def edit_channel_permissions(channel, overwrite, data):
    return request("PUT", "/channels/" + channel + "/permissions/" + overwrite, data)

def get_channel_invites(channel):
    return request("GET", "/channels/" + channel + "/invites").json()

def create_channel_invite(channel, data):
    return request("POST", "/channels/" + channel + "/invites", data)

def delete_channel_permission(channel, overwrite):
    return request("DELETE", "/channel/" + channel + "/permissions/" + overwrite)

def list_guild_emojis(guild):
    return request("GET", "/guilds/" + guild + "/emojis").json()

def get_guild_emoji(guild, emoji):
    return request("GET", "/guilds/" + guild + "/emojis" + emoji).json()

def delete_guild_emoji(guild, emoji):
    return request("DELETE", "/guilds/" + guild + "/emojis/" + emoji)

def create_guild(data):
    return request("POST", "/guilds", data)

def get_guild(guild):
    return request("GET", "/guilds/" + guild).json()

def modify_guild(guild, data):
    return request("PATCH", "/guilds/" + guild, data)

def get_guild_channels(guild):
    return request("GET", "/guilds/" + guild + "/channels").json()

def create_guild_channel(guild, data):
    return request("POST", "/guilds/" + guild + "/channels", data)

def modify_guild_channel_positions(guild, data):
    return request("PATCH", "/guilds/" + guild + "/channels", data)

def get_guild_member(guild, user):
    return request("GET", "/guilds/" + guild + "/members/" + user).json()

def list_guild_members(guild, limit = 1000, after = 0):
    return request("GET", "/guilds/" + guild + f"/members?limit={limit}&after={after}").json()

def modify_guild_member(guild, user, data):
    return request("PATCH", "/guilds/" + guild + "/members/" + user, data)

def add_guild_member_role(guild, user, role):
    return request("PUT", "/guilds/" + guild + "/members/" + user + "/roles/" + role)

def remove_guild_member_role(guild, user, role):
    return request("DELETE", "/guilds/" + guild + "/members/" + user + "/roles/" + role)

def remove_guild_member(guild, user, reason = None):
    return request("DELETE", "/guilds/" + guild + "/members/" + user + (("?reason=" + reason) if reason else ""))

def create_guild_ban(guild, user, reason=None, delete_message_days=0):
    return request("PUT", "/guilds/" + guild + "/bans/" + user + f"?delete_message_days={delete_message_days}{'&reason=' + reason if reason else ''}")

def get_guild_roles(guild):
    return request("GET", "/guilds/" + guild + "/roles").json()

def create_guild_role(guild, data):
    return request("POST", "/guilds/" + guild + "/roles", data)

def modify_guild_role_positions(guild, data):
    return request("PATCH", "/guilds/" + guild + "/roles", data)

def modify_guild_role(guild, role, data):
    return request("PATCH", "/guilds/" + guild + "/roles/" + role, data)

def delete_guild_role(guild, role):
    return request("DELETE", "/guilds/" + guild + "/roles" + role)

def get_current_user():
    return request("GET", "/users/@me").json()

def get_user(user):
    return request("GET", "/users/" + user).json()

def modify_current_user(data):
    return request("PATCH", "/users/@me", data)

def leave_guild(guild):
    return request("DELETE", "/users/@me/guilds/" + guild)