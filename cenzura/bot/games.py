from lib import modules
from lib.errors import NoPermission
from lib.embed import Embed
from lib.components import *
from functions import has_permission, find_working
import random
from korrumzthegamediscord import Renderer

@modules.module
class Gry:
    def __init__(self, bot, discord):
        self.bot = bot
        self.discord = discord
        self.players = {}

    @modules.command(description="https://korrumzthegame.cf", usage="korrumzthegame [nazwa] [id_obrazka_1-20]", aliases=["ktg"], default=True)
    def korrumzthegame(self, ctx, username: find_working(int, str) = None, image_number: int = None):
        if not has_permission(ctx):
            raise NoPermission(f"{ctx.author.id} has no {ctx.command} permission", ctx.command)

        if ("korrumzthegame", ctx.author.id) in self.players:
            session = self.players[("korrumzthegame", ctx.author.id)]
            return ctx.send(f"Pierw musisz zamknąć poprzednią sesje (https://discord.com/channels/{session.guild.id}/{session.channel.id}/{session.message_id})")

        if isinstance(username, int) and not image_number:
            image_number = username
            username = ctx.author.username

        if username == None:
            username = ctx.author.username

        if image_number == None:
            image_number = random.randint(1, 20)

        embed = Embed(title="Naciśnij w jakis przycisk aby zaktualizować graczy/bugi", color=0xe74c3c)

        components = Components(
            Row(
                Button(style=Styles.Gray, custom_id="left up", emoji={"id": None, "name": "\N{NORTH WEST ARROW}"}),
                Button(style=Styles.Gray, custom_id="up", emoji={"id": None, "name": "\N{UPWARDS BLACK ARROW}"}),
                Button(style=Styles.Gray, custom_id="right up", emoji={"id": None, "name": "\N{NORTH EAST ARROW}"})
            ),
            Row(
                Button(style=Styles.Gray, custom_id="left", emoji={"id": None, "name": "\N{LEFTWARDS BLACK ARROW}"}),
                Button(style=Styles.Red, custom_id="close", emoji={"id": None, "name": "\N{CROSS MARK}"}),
                Button(style=Styles.Gray, custom_id="right", emoji={"id": None, "name": "\N{BLACK RIGHTWARDS ARROW}"})
            ),
            Row(
                Button(style=Styles.Gray, custom_id="left down", emoji={"id": None, "name": "\N{SOUTH WEST ARROW}"}),
                Button(style=Styles.Gray, custom_id="down", emoji={"id": None, "name": "\N{DOWNWARDS BLACK ARROW}"}),
                Button(style=Styles.Gray, custom_id="right down", emoji={"id": None, "name": "\N{SOUTH EAST ARROW}"})
            )
        )

        msg = ctx.send(embed=embed, components=components).json()

        if not hasattr(ctx, "interactions"):
            ctx.interactions = []

        ctx.interactions.append(("korrumzthegame", ctx.author.id, ctx.channel.id, msg["id"]))
        self.players[("korrumzthegame", ctx.author.id)] = Renderer(self.discord, ctx.guild, ctx.channel, msg["id"], embed).start(username, image_number)