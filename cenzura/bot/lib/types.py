from .ctx import ctx
from .discord import *
import re
from .errors import UnexpectedError, Forbidden
from .permissions import PERMISSIONS
from .flags import FLAGS
from typing import List
from datetime import datetime

class Guild:
    def __init__(self, arg: dict):
        self._guild = arg

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {' '.join(['{}={!r}'.format(k, v) for k,v in self._guild.items()])}>"

    def __str__(self) -> str:
        return f"<{self.__class__.__name__} {' '.join(['{}={!r}'.format(k, v) for k,v in self._guild.items()])}>"

    @property
    def name(self) -> str:
        return self._guild["name"]

    @property
    def id(self) -> str:
        return self._guild["id"]

    @property
    def icon(self) -> str:
        return self._guild["icon"]

    @property
    def icon_url(self) -> str:
        return f"https://cdn.discordapp.com/icons/{self.id}/{self.icon}.png?size=2048"

    @property
    def description(self) -> str:
        return self._guild["description"]

    @property
    def channels(self) -> list:
        return self._guild["channels"]

    @property
    def banner(self) -> str:
        return self._guild["banner"]

    @property
    def banner_url(self) -> str:
        return f"https://cdn.discordapp.com/banners/{self.id}/{self.banner}.png?size=2048"

    @property
    def vanity_url(self) -> str:
        return self._guild["vanity_url_code"]

    @property
    def member_count(self) -> int:
        return self._guild["member_count"]

    @property
    def emojis(self) -> list:
        return self._guild["emojis"]

    @property
    def owner_id(self) -> str:
        return self._guild["owner_id"]

    @property
    def owner(self):
        return Member(self.owner_id)

    @property
    def boosts(self) -> int:
        return self._guild["premium_subscription_count"]

    @property
    def level(self) -> int:
        return self._guild["premium_tier"]

    @property
    def roles(self) -> list:
        return self._guild["roles"]

    @property
    def created_at(self) -> datetime:
        return datetime.fromtimestamp(int(((int(self.id) >> 22) + 1420070400000) / 1000))

    def create_role(self, name) -> dict:
        status = create_guild_role(self.id, {"name": name})

        if status.status_code == 403:
            raise Forbidden()

        return status

class Channel(ctx):
    def __init__(self, arg):
        if isinstance(arg, dict):
            self._channel = arg
            return

        self._arg = arg
        self._id = re.search("\d+", self._arg).group()
        self._channel = self.guild.channels[self._id]._channel

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {' '.join(['{}={!r}'.format(k, v) for k,v in self._channel.items()])}>"

    def __str__(self) -> str:
        return f"<{self.__class__.__name__} {' '.join(['{}={!r}'.format(k, v) for k,v in self._channel.items()])}>"

    def __eq__(self, channel) -> bool:
        return self.id == channel.id

    def __ne__(self, channel) -> bool:
        return self.id != channel.id

    @property
    def type(self) -> str:
        types = {
            0: "GUILD_TEXT",
            1: "DM",
            2: "GUILD_VOICE",
            3: "GROUP_DM",
            4: "GUILD_CATEGORY",
            5: "GUILD_NEWS",
            6: "GUILD_STORE",
            10: "GUILD_NEWS_THREAD",
            11: "GUILD_PUBLIC_THREAD",
            12: "GUILD_PRIVATE_THREAD",
            13: "GUILD_STAGE_VOICE"
        }

        return types[self._channel["type"]]

    @property
    def id(self) -> str:
        return self._channel["id"]

    @property
    def name(self) -> str:
        return self._channel["name"]

    @property
    def position(self) -> int:
        return self._channel["position"]

    @property
    def topic(self):
        return self._channel["topic"]

    @property
    def permission_overwrites(self) -> List[dict]:
        return self._channel["permission_overwrites"]

    @property
    def nsfw(self) -> bool:
        return self._channel["nsfw"]

    @property
    def ratelimit(self) -> int:
        return self._channel["rate_limit_per_user"]

    @property
    def mention(self) -> str:
        return f"<#{self.id}>"

    def clear(self, messages: list):
        status = bulk_delete_messages(self.channel.id, {"messages": messages})

        if status.status_code == 403:
            raise Forbidden()

        return status

    def edit_permissions(self, role, data) -> dict:
        status = edit_channel_permissions(self.id, role, data)

        if status.status_code == 403:
            raise Forbidden()

        return status

class Role(ctx):
    def __init__(self, arg):
        if isinstance(arg, dict):
            self._role = arg
            return

        self._arg = arg
        self._id = re.search("\d+", self._arg).group()
        self._role = self.guild.roles[self._id]._role

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {' '.join(['{}={!r}'.format(k, v) for k,v in self._role.items()])}>"

    def __str__(self) -> str:
        return f"<{self.__class__.__name__} {' '.join(['{}={!r}'.format(k, v) for k,v in self._role.items()])}>"

    def __eq__(self, role) -> bool:
        return self.id == role.id

    def __ne__(self, role) -> bool:
        return self.id != role.id

    def __gt__(self, role) -> bool:
        return self.position > role.position

    def __lt__(self, role) -> bool:
        return self.position < role.position

    def __ge__(self, role) -> bool:
        return self.position >= role.position

    def __le__(self, role) -> bool:
        return self.position <= role.position

    @property
    def name(self) -> str:
        return self._role["name"]

    @property
    def id(self) -> str:
        return self._role["id"]

    @property
    def permissions(self) -> list:
        permissions = []
        for permission in PERMISSIONS:
            if int(self._role["permissions"]) & PERMISSIONS[permission] == 8:
                permissions.append("ADMINISTRATOR")
            elif int(self._role["permissions"]) & PERMISSIONS[permission] == PERMISSIONS[permission]:
                permissions.append(permission)
        return permissions

    @property
    def position(self) -> int:
        return self._role["position"]

    @property
    def color(self) -> int:
        return self._role["color"]

    @property
    def mentionable(self) -> bool:
        return self._role["mentionable"]

    @property
    def managed(self) -> bool:
        return self._role["managed"]

    @property
    def hoist(self) -> bool:
        return self._role["hoist"]

    @property
    def mention(self) -> str:
        return f"<@&{self.id}>"

class User(ctx):
    def __init__(self, arg):
        if isinstance(arg, dict):
            self._user = arg
            return

        self._arg = arg
        self._id = re.search("\d+", self._arg).group()
        self._user = None

        if self.data["mentions"]:
            for user in self.data["mentions"]:
                if user["id"] == self._id:
                    self._user = user
                    del self._user["member"]

        if not self._user:
            user = get_user(self._id)
            if "code" in user:
                raise InvalidUser()

            self._user = user

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {' '.join(['{}={!r}'.format(k, v) for k,v in self._user.items()])}>"

    def __str__(self) -> str:
        return f"<{self.__class__.__name__} {' '.join(['{}={!r}'.format(k, v) for k,v in self._user.items()])}>"

    def __eq__(self, user) -> bool:
        return self.id == user.id

    def __ne__(self, user) -> bool:
        return self.id != user.id

    @property
    def username(self) -> str:
        return self._user["username"]

    @property
    def discriminator(self) -> str:
        return self._user["discriminator"]

    @property
    def id(self) -> str:
        return self._user["id"]

    @property
    def user(self) -> str:
        return self.username + "#" + self.discriminator

    @property
    def avatar(self) -> str:
        return self._user["avatar"]

    @property
    def avatar_url(self) -> str:
        if not self.avatar:
            return "https://discord.com/assets/6f26ddd1bf59740c536d2274bb834a05.png"

        return f"https://cdn.discordapp.com/avatars/{self.id}/{self.avatar}.png?size=2048"

    @property
    def bot(self) -> bool:
        return True if "bot" in self._user else False

    @property
    def public_flags(self) -> list:
        flags = []
        for flag in FLAGS:
            if self._user["public_flags"] & FLAGS[flag] == FLAGS[flag]:
                flags.append(flag)

        return flags

    @property
    def mention(self) -> str:
        return f"<@{self.id}>"

    @property
    def created_at(self) -> datetime:
        return datetime.fromtimestamp(int(((int(self.id) >> 22) + 1420070400000) / 1000))

class Member(ctx):
    def __init__(self, arg):
        if isinstance(arg, dict):
            self._member = arg
            return
            
        self._arg = arg
        self._id = re.search("\d+", self._arg).group()
        self._member = None

        if self.data["mentions"]:
            for member in self.data["mentions"]:
                if member["id"] == self._id:
                    self._member = member

        if not self._member:
            member = get_guild_member(self.guild.id, self._id)
            if "code" in member:
                raise InvalidMember()

            self._member = member["user"]
            self._member["member"] = member
            del self._member["member"]["user"]

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {' '.join(['{}={!r}'.format(k, v) for k,v in self._member.items()])}>"

    def __str__(self) -> str:
        return f"<{self.__class__.__name__} {' '.join(['{}={!r}'.format(k, v) for k,v in self._member.items()])}>"

    def __eq__(self, member) -> bool:
        return self.id == member.id

    def __ne__(self, member) -> bool:
        return self.id == member.id

    def __gt__(self, member) -> bool:
        if self.id == self.guild.owner_id:
            return True

        return self.roles[0] > member.roles[0]

    def __lt__(self, member) -> bool:
        if self.id == self.guild.owner_id:
            return False

        return self.roles[0] < member.roles[0]

    def __ge__(self, member) -> bool:
        if self.id == self.guild.owner_id:
            return True

        return self.roles[0] >= member.roles[0]

    def __le__(self, member) -> bool:
        if self.id == self.guild.owner_id:
            return False

        return self.roles[0] <= member.roles[0]

    @property
    def username(self) -> str:
        return self._member["username"]

    @property
    def discriminator(self) -> str:
        return self._member["discriminator"]

    @property
    def id(self) -> str:
        return self._member["id"]

    @property
    def user(self) -> str:
        return self.username + "#" + self.discriminator

    @property
    def avatar(self) -> str:
        return self._member["avatar"]

    @property
    def avatar_url(self) -> str:
        if not self.avatar:
            return "https://discord.com/assets/6f26ddd1bf59740c536d2274bb834a05.png"

        return f"https://cdn.discordapp.com/avatars/{self.id}/{self.avatar}.png?size=2048"

    @property
    def bot(self) -> bool:
        return True if "bot" in self._member else False

    @property
    def public_flags(self) -> list:
        flags = []
        for flag in FLAGS:
            if self._member["public_flags"] & FLAGS[flag] == FLAGS[flag]:
                flags.append(flag)

        return flags

    @property
    def roles(self) -> List[Role]:
        roles = []
        for role in self._member["member"]["roles"]:
            roles.append(self.guild.roles[role])
        roles.append(self.guild.roles[self.guild.id])
        roles.sort(key=lambda role: role.position, reverse=True)
        return roles

    @property
    def premium_since(self):
        return self._member["member"]["premium_since"]

    @property
    def nick(self) -> str:
        return self._member["member"]["nick"]

    @property
    def joined_at(self) -> datetime:
        return datetime.strptime(self._member["member"]["joined_at"].split(".")[0], "%Y-%m-%dT%H:%M:%S")

    @property
    def created_at(self) -> datetime:
        return datetime.fromtimestamp(int(((int(self.id) >> 22) + 1420070400000) / 1000))

    @property
    def mention(self) -> str:
        return f"<@!{self.id}>"

    def kick(self, reason = None) -> dict:
        status = remove_guild_member(self.guild.id, self.id, reason)

        if status.status_code == 403:
            raise Forbidden()

        return status

    def ban(self, reason = None, delete_message_days = 0) -> dict:
        status = create_guild_ban(self.guild.id, self.id, reason, delete_message_days)
        
        if status.status_code == 403:
            raise Forbidden()

        return status

    def add_role(self, role) -> dict:
        status = add_guild_member_role(self.guild.id, self.id, role)
        
        if status.status_code == 403:
            raise Forbidden()

        return status

    def remove_role(self, role) -> dict:
        status = remove_guild_member_role(self.guild.id, self.id, role)
        
        if status.status_code == 403:
            raise Forbidden()

        return status

    def has_permission(self, permission: str) -> bool:
        if self.id == self.guild.owner_id:
            return True

        for role in self.roles:
            if permission in role.permissions:
                return True

        return False