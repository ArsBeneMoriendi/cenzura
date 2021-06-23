from lib import gateway, discord, intents
import config

bot = gateway.Bot(prefix=config.prefix, intents=intents.all_intents("GUILD_PRESENCES"))
bot.register_modules(discord, "events", "help", "fun", "admin", "inne", "permissions_manager", "info", "dev")

@bot.event
def ready(ctx):
    bot.set_presence("\u200b", status="dnd")
    print("im ready")

bot.run(config.token)