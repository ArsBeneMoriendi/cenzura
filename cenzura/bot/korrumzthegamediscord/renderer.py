from .multiplayer import PlayerMe
from PIL import Image, ImageDraw, ImageFont
import random, threading, io, base64
from datetime import datetime
import requests

class Renderer:
    def __init__(self, discord, guild, channel, message_id, embed):
        self.discord = discord
        self.guild = guild
        self.channel = channel
        self.message_id = message_id

        self.embed = embed

        self.player: PlayerMe = None
        self.image = Image.new("RGB", (1920, 1080), (32, 32, 32))
        self.draw = ImageDraw.Draw(self.image)

        self.img = io.BytesIO()

    def update(self, _id, token):
        for p in self.player.players + [self.player]:
            self.image.paste(Image.open(f"korrumzthegamediscord/assets/players/player{p.image_number}.png"), (p.x, p.y))
            font = ImageFont.truetype("fonts/arial.ttf", 15)
            self.draw.text((p.x, p.y - 75 / 3), p.username, (255, 255, 255), font=font)

        for b in self.player.bugs:
            self.image.paste(Image.open(f"korrumzthegamediscord/assets/bugs/bug{b.image_number}.png"), (b.x, b.y))

        self.image.save(self.img, format="JPEG")

        code = requests.post("https://cenzurabot.com/ktg", files={"file": ("unknown.jpeg", self.img.getvalue())}).json()["code"]
        self.embed.title = "Pull requesty"
        self.embed.description = "\n".join([f"{player.username if not self.player.username == player.username else player.username + ' (ty)'} {player.pull_requests}" for player in sorted(self.player.players + [self.player], reverse=True, key=lambda player: player.pull_requests)])
        self.embed.set_image(url=f"https://cenzurabot.com/ktg/{code}")
        self.embed.set_thumbnail(url=f"https://korrumzthegame.cf/images/player{self.player.image_number}.png")
        self.discord.interaction_response(7, _id, token, embed=self.embed)

        self.image = Image.new("RGB", (1920, 1080), (32, 32, 32))
        self.draw = ImageDraw.Draw(self.image)

        self.img = io.BytesIO()

    def start(self, username, image_number: int):
        self.player = PlayerMe(self.update, username, random.randint(0, 1920), random.randint(0, 1080), 0, image_number)
        threading.Thread(target=self.player.run).start()

        return self