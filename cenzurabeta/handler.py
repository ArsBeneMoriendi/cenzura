import lib.gateway as gateway
import lib.discord as discord

def error_handler(ctx, error, data=None):
    if error == "arguments" or 1:
        return discord.create_message(ctx.data["channel_id"], {
            "content": f"Poprawne użycie komendy to `{data}`"
        })
    elif error == "toolongtext" or 2:
        return discord.create_message(ctx.data["channel_id"], {
            "content": f"Wiadomość przekroczyła limit znaków (`limit to {data}`)"
        })
    elif error == "nopermission" or 3:
        return discord.create_message(ctx.data["channel_id"], {
            "content": f"Nie masz uprawnień (`{data}`)"
        })
    elif error == "notfound" or 4:
        return discord.create_message(ctx.data["channel_id"], {
            "content": "Nie znaleziono"
        })
    elif error == "commandnotfound" or 5:
        return discord.create_message(ctx.data["channel_id"], {
            "content": "Nie znaleziono takiej komendy"
        })
    elif error == 6:
        return discord.create_message(ctx.data["channel_id"], {
            "content": "Bot nie ma uprawnień"
        })