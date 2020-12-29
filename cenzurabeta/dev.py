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

def load(gateway, discord):
    @gateway.command(description="Wywołuje skrypt", usage="eval (kod)", category="dev", _default=False)
    def _eval(ctx):
        if not ctx.data["author"]["id"] in config.owners:
            return handler.error_handler(ctx, "nopermission", ctx.command)

        ctx.args = " ".join(ctx.args)

        code = "\n".join(f"    {x}" for x in ctx.args.splitlines())
        body = f"def _eval_():\n{code}"

        parsed = ast.parse(body)
        body = parsed.body[0].body

        insert_returns(body)

        env = {
            "ctx": ctx,
            "gateway": gateway,
            "discord": discord
        }

        exec(compile(parsed, filename="siema", mode="exec"), env)

        try:
            result = eval("_eval_()", env)
        except Exception as e:
            result = traceback.format_exc()

        discord.create_message(ctx.data["channel_id"], {
            "content": f"```{result}```"
        })

    @gateway.command(description="Zatrzymuje cały proces", usage="stop", category="dev", _default=False)
    def stop(ctx):
        if not ctx.data["author"]["id"] in config.owners:
            return handler.error_handler(ctx, "nopermission", ctx.command)

        discord.create_message(ctx.data["channel_id"], {
            "content": "Zatrzymywanie bota..."
        })

        ctx.running = False
        ctx.ws.close()
