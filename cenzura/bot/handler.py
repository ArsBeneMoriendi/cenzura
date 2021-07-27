from lib import modules
from lib.embed import Embed
from lib.errors import *
import traceback
import config

@modules.module
class Handler:
    def __init__(self, bot, discord):
        self.bot = bot
        self.discord = discord
        self.debug = False

    @modules.event
    def on_error(self, ctx, error):
        if self.debug == True:
            result = traceback.format_exc()
            return ctx.send(f"```{result}```")

        if isinstance(error, NoArgument):
            usage = error.command["usage"]
            needed_arg = usage.split()[1:][error.needed_args.index(error.needed_arg)]

            result = f"```{usage}\n{' ' * usage.index(needed_arg)}{'^' * (len(needed_arg))}\n\nNie podałeś tego argumentu```"
            return ctx.send(result)

        elif isinstance(error, InvalidArgumentType):
            usage = error.command["usage"]
            needed_arg = usage.split()[1:][error.needed_args.index(error.needed_arg)]

            result = f"```{usage}\n{' ' * usage.index(needed_arg)}{'^' * (len(needed_arg))}\n\nTu podałeś zły argument```"
            return ctx.send(result)

        elif isinstance(error, CommandNotFound):
            return ctx.send("Nie znaleziono takiej komendy")

        elif isinstance(error, NoPermission):
            return ctx.send(f"Nie masz uprawnień (`{error.permission}`)")

        elif isinstance(error, Forbidden):
            return ctx.send("Bot nie ma uprawnień")

        elif isinstance(error, (NotFound, KeyError, IndexError)):
            return ctx.send("Nie znaleziono")
            
        elif isinstance(error, UnexpectedError):
            return ctx.send("Wystąpił nieoczekiwany błąd")

        else:
            embed = Embed(title="Wystąpił nieoczekiwany błąd...", description=f"Wejdź na [serwer support](https://discord.gg/tDQURnVtGC) i zgłoś go.\n```{traceback.format_exc().splitlines()[-1]}```", color=0xe74c3c)
            return ctx.send(embed=embed)

    @modules.command(description="Włącza debugowanie", usage="debug")
    def debug(self, ctx):
        if not self.author.id in config.owners:
            raise NoPermission(f"{ctx.author.id} has no {ctx.command} permission", ctx.command)

        if not hasattr(self, "debug"):
            self.debug = False

        self.debug = not self.debug

        ctx.send(("Włączono" if self.debug else "Wyłączono") + " debugowanie")