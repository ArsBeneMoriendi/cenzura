import json
from lib.ctx import ctx

def read_json(file):
    with open("json/" + file + ".json", "r") as f:
        return json.load(f)

def write_json(file, data):
    with open("json/" + file + ".json", "w") as f:
        json.dump(data, f, indent=4)

def has_permission(ctx):
    guilds = read_json("guilds")
    
    if not "permissions" in guilds[ctx.guild.id]:
        guilds[ctx.guild.id]["permissions"] = {}
        write_json("guilds", guilds)

    if ctx.author.has_permission("ADMINISTRATOR"):
        return True

    for role in ctx.author.roles:
        if role.id in guilds[ctx.guild.id]["permissions"] and ctx.command in guilds[ctx.guild.id]["permissions"][role.id]:
            return guilds[ctx.guild.id]["permissions"][role.id][ctx.command]
        else:
            if "default" in ctx.commands[ctx.command] and ctx.commands[ctx.command]["default"] == True:
                return True

    return False

def find_working(*types, **keys):
    def func(arg):
        no_one = False
        for _type in types:
            try:
                arg = _type(arg)
                if arg.__class__.__name__ in keys:
                    if not keys[arg.__class__.__name__](arg):
                        raise Exception()
                no_one = False
                break
            except:
                no_one = True
                continue

        if no_one:
            raise Exception()

        return arg

    return func

def between(_from, to):
    def func(arg: int):
        if int(arg) < _from or int(arg) > to:
            raise Exception()

        return int(arg)

    return func

def is_in(*args):
    def func(arg):
        if not arg.upper() in [x.upper() for x in args]:
            raise Exception()

        return arg

    return func

def get_int(user, user2):
    return round(((int(user.id) + int(user2.id) / int(user.created_at.timestamp()) + int(user2.created_at.timestamp())) % 10001) / 100)
