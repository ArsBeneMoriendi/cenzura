from lib import gateway, discord, intents, modules
import config

bot = gateway.Bot(prefix=config.prefix, intents=intents.all_intents("GUILD_PRESENCES"))
modules.load_modules(bot, discord, "handler", "events", "help", "fun", "admin", "other", "permissions_manager", "info", "dev")

@modules.event
def ready(ctx):
    bot.set_presence("\u200b", status="dnd")
    print("im ready")

bot.run(config.token)