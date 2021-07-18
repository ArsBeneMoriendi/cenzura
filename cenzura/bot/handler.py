from lib.embed import Embed
from lib.errors import *
import traceback

def load(bot, discord):
    @bot.event
    def on_error(ctx, error):
        if hasattr(ctx, "debug") and ctx.debug == True:
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