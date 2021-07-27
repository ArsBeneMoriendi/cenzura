from lib import modules
from lib.ctx import ctx
import config
import ast
import traceback
from lib.errors import NoPermission
from lib.types import Member
from lib.discord import send
from inspect import signature, _empty

@modules.module
class Dev(ctx):
    def __init__(self, bot, discord):
        self.bot = bot
        self.discord = discord

    def insert_returns(self, body):
        if isinstance(body[-1], ast.Expr):
            body[-1] = ast.Return(body[-1].value)
            ast.fix_missing_locations(body[-1])

        if isinstance(body[-1], ast.If):
            insert_returns(body[-1].body)
            insert_returns(body[-1].orelse)

        if isinstance(body[-1], ast.With):
            insert_returns(body[-1].body)

    @modules.command(description="Wywołuje skrypt", usage="eval (kod)")
    def _eval(self, code):
        if not self.author.id in config.owners:
            raise NoPermission(f"{self.author.id} has no {self.command} permission", self.command)

        ctx.args = " ".join(self.args)
        
        code = "\n".join(f"    {x}" for x in ctx.args.splitlines())
        body = f"def elo():\n{code}"

        parsed = ast.parse(body)
        body = parsed.body[0].body

        self.insert_returns(body)

        env = {
            "ctx": ctx,
            "bot": self.bot,
            "discord": self.discord
        }

        exec(compile(parsed, filename="siema", mode="exec"), env)

        try:
            result = eval("elo()", env)
        except:
            result = traceback.format_exc()

        response = self.send(f"```{result}```")

        if not response.status_code == 200:
            self.send(f"```{response.json()}```")

    @modules.command(description="Przeładowuje moduł", usage="reload (moduł)")
    def reload(self, module):
        if not self.author.id in config.owners:
            raise NoPermission(f"{self.author.id} has no {self.command} permission", self.command)

        modules.reload(module)
        self.send(f"Przeładowano `{module}`")

    @modules.command(description="Wywołuje komende za kogoś", usage="su (osoba) (komenda) [argumenty]")
    def su(self, user: Member, command, args = None):
        if not self.author.id in config.owners:
            raise NoPermission(f"{self.author.id} has no {self.command} permission", self.command)

        args = self.args[2:]
        func = self.commands[command]["function"]

        class su_self(ctx):
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
                    raise InvalidArgumentType(f"type {annotation} is not valid for {needed_arg} argument", self.commands[command], list(needed_args), needed_arg)
                parsed_args.append(parsed_arg)
            else:
                if arg.default == _empty:
                    raise NoArgument(f"{needed_arg} was not specified", self.commands[command], list(needed_args), needed_arg)

        func(su_self(send, user, command, args), *parsed_args)

    @modules.command(description="Aktualizuje statystyki", usage="updatestats")
    def updatestats(self):
        if not self.author.id in config.owners:
            raise NoPermission(f"{self.author.id} has no {self.command} permission", self.command)

        guilds = len(self.guilds)
        self.requests.post(f"https://top.gg/api/bots/{self.bot_user.id}/stats", headers={"authorization": config.topgg}, json={"server_count": guilds})
        self.requests.post("https://api.dlist.top/v1/bots/stats", headers={"authorization": config.dlist}, json={"servers": guilds, "members": 0})

        self.send("Zaktualizowano statystyki")