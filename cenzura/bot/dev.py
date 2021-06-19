import handler
import config
import ast
import traceback

def insert_returns(body):
    if isinstance(body[-1], ast.Expr):
        body[-1] = ast.Return(body[-1].value)
        ast.fix_missing_locations(body[-1])

    if isinstance(body[-1], ast.If):
        insert_returns(body[-1].body)
        insert_returns(body[-1].orelse)

    if isinstance(body[-1], ast.With):
        insert_returns(body[-1].body)

def load(bot, discord):
    def _env(option, key, value=None):
        if option in ("ADD", "REPLACE"):
            env[key] = value
        elif option in ("REMOVE", "REM"):
            del env[key]

        return option, key, value

    env = {
        "env": _env
    }

    @bot.command(description="Wywołuje skrypt", usage="eval (kod)", category="dev", _default=False)
    def _eval(ctx):
        if not ctx.data["author"]["id"] in config.owners:
            return handler.error_handler(ctx, "nopermission", ctx.command)

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
        except Exception:
            result = traceback.format_exc().splitlines()[-1]

        response = ctx.send(result)

        if not response.status_code == 200:
            ctx.send(f"```{response.json()}```")

    @bot.command(description="Przeładowuje moduł", usage="reload (moduł)", category="dev", _default=False)
    def reload(ctx):
        if not ctx.data["author"]["id"] in config.owners:
            return handler.error_handler(ctx, "nopermission", ctx.command)

        try:
            bot.register_module(ctx.args[0], bot, discord)
            result = f"Przeładowano `{ctx.args[0]}`"
        except:
            result = "```" + traceback.format_exc().splitlines()[-1] + "```"

        ctx.send(result)

    @bot.command(description="Aktualizuje statystyki", usage="updatestats", category="dev", _default=False)
    def updatestats(ctx):
        if not ctx.data["author"]["id"] in config.owners:
            return handler.error_handler(ctx, "nopermission", ctx.command)

        guilds = len(ctx.guilds)
        ctx.requests.post(f"https://top.gg/api/bots/{ctx.bot['id']}/stats", headers={"authorization": config.topgg}, json={"server_count": guilds})
        ctx.requests.post("https://api.dlist.top/v1/bots/stats", headers={"authorization": config.dlist}, json={"servers": guilds, "members": 0})

        ctx.send("Zaktualizowano statystyki")