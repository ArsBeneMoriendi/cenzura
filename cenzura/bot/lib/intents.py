intents_list = {
    "GUILDS": 1 << 0,
    "GUILD_MEMBERS": 1 << 1,
    "GUILD_BANS": 1 << 2,
    "GUILD_EMOJIS": 1 << 3,
    "GUILD_INTEGRATIONS ": 1 << 4,
    "GUILD_WEBHOOKS": 1 << 5,
    "GUILD_INVITES ": 1 << 6,
    "GUILD_VOICE_STATES ": 1 << 7,
    "GUILD_PRESENCES": 1 << 8,
    "GUILD_MESSAGES": 1 << 9,
    "GUILD_MESSAGE_REACTIONS": 1 << 10,
    "GUILD_MESSAGE_TYPING": 1 << 11,
    "DIRECT_MESSAGES": 1 << 12,
    "DIRECT_MESSAGE_REACTIONS ": 1 << 13,
    "DIRECT_MESSAGE_TYPING": 1 << 14
}

def default():
    return all_intents("GUILD_MEMBERS", "GUILD_PRESENCES")

def get(*args):
    intents = 0

    for intent in intents_list:
        if intent in args:
            intents |= intents_list[intent]

    return intents

def all_intents(*args):
    intents = 0

    for intent in intents_list:
        if not intent in args:
            intents |= intents_list[intent]

    return intents