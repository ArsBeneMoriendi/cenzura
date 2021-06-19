from lib import gateway
from lib import discord
from lib import intents
import config

bot = gateway.Bot(prefix=config.prefix, intents=intents.all_intents("GUILD_PRESENCES"))

modules = [
    "events",
    "help",
    "fun",
    "admin",
    "inne",
    "permissions_manager",
    "info",
    "dev"
]

bot.register_modules(modules, bot, discord)

@bot.event
def ready(ctx):
    bot.set_presence("\u200b", status="dnd")
    print("im ready")

bot.run(config.token)