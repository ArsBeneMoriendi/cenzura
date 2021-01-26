import lib.gateway as gateway
import lib.discord as discord

def error_handler(ctx, error, data=None):
    if error == "error":
        return discord.create_message(ctx.data["channel_id"], {
            "embed": {
                "title": "Wystąpił nieoczekiwany błąd...",
                "description": "Wejdź na serwer support i zgłoś go.\n```" + data + "```",
                "color": 0xe74c3c,
                "footer": {
                    "text": f"Wywołane przez {ctx.data['author']['id']}"
                }
            }
        })
    elif error == "arguments":
        return discord.create_message(ctx.data["channel_id"], {
            "content": f"Poprawne użycie komendy to `{data}`"
        })
    elif error == "toolongtext":
        return discord.create_message(ctx.data["channel_id"], {
            "content": f"Wiadomość przekroczyła limit znaków (`limit to {data}`)"
        })
    elif error == "nopermission":
        return discord.create_message(ctx.data["channel_id"], {
            "content": f"Nie masz uprawnień (`{data}`)"
        })
    elif error == "notfound":
        return discord.create_message(ctx.data["channel_id"], {
            "content": "Nie znaleziono"
        })
    elif error == "commandnotfound":
        return discord.create_message(ctx.data["channel_id"], {
            "content": "Nie znaleziono takiej komendy"
        })
    elif error == 6:
        return discord.create_message(ctx.data["channel_id"], {
            "content": "Bot nie ma uprawnień"
        })
