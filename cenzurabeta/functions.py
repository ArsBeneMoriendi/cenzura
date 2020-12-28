import json
import lib.permissions as permissions

def read_json(file):
    with open("json/" + file + ".json", "r") as f:
        return json.load(f)

def write_json(file, data):
    with open("json/" + file + ".json", "w") as f:
        json.dump(data, f, indent=4)

def has_permission(ctx):
    guild = ctx.data["guild_id"]
    guilds = read_json("guilds")
    
    if not "permissions" in guilds[guild]:
        guilds[guild]["permissions"] = {}

    write_json("guilds", guilds)

    if permissions.has_permission(ctx, ctx.data["author"]["id"], "ADMINISTRATOR"):
        return True

    ctx.data["member"]["roles"].append(ctx.data["guild_id"])

    for role in ctx.data["member"]["roles"]:
        if role in guilds[guild]["permissions"] and ctx.command in guilds[guild]["permissions"][role] and guilds[guild]["permissions"][role][ctx.command]:
            return True
        else:
            if ctx.commands in ctx.default:
                return True

    return False