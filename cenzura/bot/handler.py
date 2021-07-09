from lib import discord
from lib.embed import Embed

def error_handler(ctx, error, data=None):
    if error == "error":
        embed = Embed(title="Wystąpił nieoczekiwany błąd...", description="Wejdź na [serwer support](https://discord.gg/tDQURnVtGC) i zgłoś go.\n```" + data + "```", color=0xe74c3c)
        return ctx.send(embed=embed)

    elif error == "arguments":
        return ctx.send(f"Poprawne użycie komendy to `{data}`")

    elif error == "toolongtext":
        return ctx.send(f"Wiadomość przekroczyła limit znaków (`limit to {data}`)")

    elif error == "nopermission":
        return ctx.send(f"Nie masz uprawnień (`{data}`)")

    elif error == "notfound":
        return ctx.send("Nie znaleziono")

    elif error == "commandnotfound":
        return ctx.send("Nie znaleziono takiej komendy")

    elif error == 6:
        return ctx.send("Bot nie ma uprawnień")

    elif error == "nsfw":
        return ctx.send("Kanał musi być nsfw")
        
    elif error == 8:
        return ctx.send("Wystąpił nieoczekiwany błąd")