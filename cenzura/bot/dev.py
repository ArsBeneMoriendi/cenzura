import config
import ast
import traceback
from lib.errors import NoPermission
from lib.types import Member
from lib.discord import send
from inspect import signature, _empty

def load(bot, discord):
    def insert_returns(body):
        if isinstance(body[-1], ast.Expr):
            body[-1] = ast.Return(body[-1].value)
            ast.fix_missing_locations(body[-1])

        if isinstance(body[-1], ast.If):
            insert_returns(body[-1].body)
            insert_returns(body[-1].orelse)

        if isinstance(body[-1], ast.With):
            insert_returns(body[-1].body)

    def _env(option, key, value=None):
        if option in ("ADD", "REPLACE"):
            env[key] = value
        elif option in ("REMOVE", "REM"):
            del env[key]

        return option, key, value

    env = {
        "env": _env
    }

    @bot.command(description="Wywołuje skrypt", usage="eval (kod)", category="dev")
    def _eval(ctx, code):
        if not ctx.author.id in config.owners:
            raise NoPermission(f"{ctx.author.id} has no {ctx.command} permission", ctx.command)

        ctx.args = " ".join(ctx.args)

        code = "\n".join(f"    {x}" for x in ctx.args.splitlines())
        body = f"def elo():\n{code}"

        parsed = ast.parse(body)
        body = parsed.body[0].body

        insert_returns(body)

        env2 = {
            "ctx": ctx,
            "bot": bot,
            "discord": discord
        }

        env.update(env2)

        exec(compile(parsed, filename="siema", mode="exec"), env)

        try:
            result = eval("elo()", env)
        except:
            result = traceback.format_exc()

        response = ctx.send(f"```{result}```")

        if not response.status_code == 200:
            ctx.send(f"```{response.json()}```")

    @bot.command(description="Przeładowuje moduł", usage="reload (moduł)", category="dev")
    def reload(ctx, cog):
        if not ctx.author.id in config.owners:
            raise NoPermission(f"{ctx.author.id} has no {ctx.command} permission", ctx.command)

        bot.register_modules(discord, cog)
        result = f"Przeładowano `{cog}`"

        ctx.send(result)

    @bot.command(description="Włącza debugowanie", usage="debug", category="dev")
    def debug(ctx):
        if not ctx.author.id in config.owners:
            raise NoPermission(f"{ctx.author.id} has no {ctx.command} permission", ctx.command)

        if not hasattr(ctx, "debug"):
            ctx.debug = False

        ctx.debug = not ctx.debug

        ctx.send(("Włączono" if ctx.debug else "Wyłączono") + " debugowanie")

    @bot.command(description="Wywołuje komende za kogoś", usage="su (osoba) (komenda) [argumenty]", category="dev")
    def su(ctx, user: Member, command, args = None):
        if not ctx.author.id in config.owners:
            raise NoPermission(f"{ctx.author.id} has no {ctx.command} permission", ctx.command)

        args = ctx.args[2:]
        func = ctx.commands[command]["function"]

        class su_ctx(ctx):
            def __init__(self, send, author: Member, command, args):
                self.author = author
                self.command = command
                self.args = args
                self.send = lambda *args, **kwargs: send(self.data["channel_id"], *args, **kwargs)

        needed_args = dict(list(signature(func).parameters.items())[1:])
        parsed_args = []

        for needed_arg in needed_args:
            arg = needed_args[needed_arg]
            if arg.annotation == _empty:
                annotation = lambda x: str(x)
            else:
                annotation = arg.annotation

            index = list(needed_args).index(needed_arg)
            if index < len(args):
                try:
                    parsed_arg = annotation(args[index])
                except:
                    raise InvalidArgumentType(f"type {annotation} is not valid for {needed_arg} argument", ctx.commands[command], list(needed_args), needed_arg)
                parsed_args.append(parsed_arg)
            else:
                if arg.default == _empty:
                    raise NoArgument(f"{needed_arg} was not specified", ctx.commands[command], list(needed_args), needed_arg)

        func(su_ctx(send, user, command, args), *parsed_args)

    @bot.command(description="Aktualizuje statystyki", usage="updatestats", category="dev")
    def updatestats(ctx):
        if not ctx.author.id in config.owners:
            raise NoPermission(f"{ctx.author.id} has no {ctx.command} permission", ctx.command)

        guilds = len(ctx.guilds)
        ctx.requests.post(f"https://top.gg/api/bots/{ctx.bot.id}/stats", headers={"authorization": config.topgg}, json={"server_count": guilds})
        ctx.requests.post("https://api.dlist.top/v1/bots/stats", headers={"authorization": config.dlist}, json={"servers": guilds, "members": 0})

        ctx.send("Zaktualizowano statystyki")