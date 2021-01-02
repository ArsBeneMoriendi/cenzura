import lib.permissions as permissions
import functions

badwords_list = ["CHUJ","CHUJA", "CHUJEK", "CHUJU", "CHUJEM", "CHUJNIA",
"CHUJOWY", "CHUJOWA", "CHUJOWE", "CIPA", "CIPĘ", "CIPE", "CIPĄ",
"CIPIE", "DOJEBAĆ","DOJEBAC", "DOJEBIE", "DOJEBAŁ", "DOJEBAL",
"DOJEBAŁA", "DOJEBALA", "DOJEBAŁEM", "DOJEBALEM", "DOJEBAŁAM",
"DOJEBALAM", "DOJEBIĘ", "DOJEBIE", "DOPIEPRZAĆ", "DOPIEPRZAC",
"DOPIERDALAĆ", "DOPIERDALAC", "DOPIERDALA", "DOPIERDALAŁ",
"DOPIERDALAL", "DOPIERDALAŁA", "DOPIERDALALA", "DOPIERDOLI",
"DOPIERDOLIŁ", "DOPIERDOLIL", "DOPIERDOLĘ", "DOPIERDOLE", "DOPIERDOLI",
"DOPIERDALAJĄCY", "DOPIERDALAJACY", "DOPIERDOLIĆ", "DOPIERDOLIC",
"DUPA", "DUPIE", "DUPĄ", "DUPCIA", "DUPECZKA", "DUPY", "DUPE", "HUJ",
"HUJEK", "HUJNIA", "HUJA", "HUJE", "HUJEM", "HUJU", "JEBAĆ", "JEBAC",
"JEBAŁ", "JEBAL", "JEBIE", "JEBIĄ", "JEBIA", "JEBAK", "JEBAKA", "JEBAL",
"JEBAŁ", "JEBANY", "JEBANE", "JEBANKA", "JEBANKO", "JEBANKIEM",
"JEBANYMI", "JEBANA", "JEBANYM", "JEBANEJ", "JEBANĄ", "JEBANA",
"JEBANI", "JEBANYCH", "JEBANYMI", "JEBCIE", "JEBIĄCY", "JEBIACY",
"JEBIĄCA", "JEBIACA", "JEBIĄCEGO", "JEBIACEGO", "JEBIĄCEJ", "JEBIACEJ",
"JEBIA", "JEBIĄ", "JEBIE", "JEBIĘ", "JEBLIWY", "JEBNĄĆ", "JEBNAC",
"JEBNĄC", "JEBNAĆ", "JEBNĄŁ", "JEBNAL", "JEBNĄ", "JEBNA", "JEBNĘŁA",
"JEBNELA", "JEBNIE", "JEBNIJ", "JEBUT", "KOORWA", "KÓRWA", "KURESTWO",
"KUREW", "KUREWSKI", "KUREWSKA", "KUREWSKIEJ", "KUREWSKĄ", "KUREWSKA",
"KUREWSKO", "KUREWSTWO", "KURWA", "KURWAA", "KURWAMI", "KURWĄ", "KURWE",
"KURWĘ", "KURWIE", "KURWISKA", "KURWO", "KURWY", "KURWACH", "KURWAMI",
"KUREWSKI", "KURWIARZ", "KURWIĄCY", "KURWICA", "KURWIĆ", "KURWIC",
"KURWIDOŁEK", "KURWIK", "KURWIKI", "KURWISZCZE", "KURWISZON",
"KURWISZONA", "KURWISZONEM", "KURWISZONY", "KUTAS", "KUTASA", "KUTASIE",
"KUTASEM", "KUTASY", "KUTASÓW", "KUTASOW", "KUTASACH", "KUTASAMI",
"MATKOJEBCA", "MATKOJEBCY", "MATKOJEBCĄ", "MATKOJEBCA", "MATKOJEBCAMI",
"MATKOJEBCACH", "NABARŁOŻYĆ", "NAJEBAĆ", "NAJEBAC", "NAJEBAŁ",
"NAJEBAL", "NAJEBAŁA", "NAJEBALA", "NAJEBANE", "NAJEBANY", "NAJEBANĄ",
"NAJEBANA", "NAJEBIE", "NAJEBIĄ", "NAJEBIA", "NAOPIERDALAĆ",
"NAOPIERDALAC", "NAOPIERDALAŁ", "NAOPIERDALAL", "NAOPIERDALAŁA",
"NAOPIERDALALA", "NAOPIERDALAŁA", "NAPIERDALAĆ", "NAPIERDALAC",
"NAPIERDALAJĄCY", "NAPIERDALAJACY", "NAPIERDOLIĆ", "NAPIERDOLIC",
"NAWPIERDALAĆ", "NAWPIERDALAC", "NAWPIERDALAŁ", "NAWPIERDALAL",
"NAWPIERDALAŁA", "NAWPIERDALALA", "OBSRYWAĆ", "OBSRYWAC", "OBSRYWAJĄCY",
"OBSRYWAJACY", "ODPIEPRZAĆ", "ODPIEPRZAC", "ODPIEPRZY", "ODPIEPRZYŁ",
"ODPIEPRZYL", "ODPIEPRZYŁA", "ODPIEPRZYLA", "ODPIERDALAĆ",
"ODPIERDALAC", "ODPIERDOL", "ODPIERDOLIŁ", "ODPIERDOLIL",
"ODPIERDOLIŁA", "ODPIERDOLILA", "ODPIERDOLI", "ODPIERDALAJĄCY",
"ODPIERDALAJACY", "ODPIERDALAJĄCA", "ODPIERDALAJACA", "ODPIERDOLIĆ",
"ODPIERDOLIC", "ODPIERDOLI", "ODPIERDOLIŁ", "OPIEPRZAJĄCY",
"OPIERDALAĆ", "OPIERDALAC", "OPIERDALA", "OPIERDALAJĄCY",
"OPIERDALAJACY", "OPIERDOL", "OPIERDOLIĆ", "OPIERDOLIC", "OPIERDOLI",
"OPIERDOLĄ", "OPIERDOLA", "PICZKA", "PIEPRZNIĘTY", "PIEPRZNIETY",
"PIEPRZONY", "PIERDEL", "PIERDLU", "PIERDOLĄ", "PIERDOLA", "PIERDOLĄCY",
"PIERDOLACY", "PIERDOLĄCA", "PIERDOLACA", "PIERDOL", "PIERDOLE",
"PIERDOLENIE", "PIERDOLENIEM", "PIERDOLENIU", "PIERDOLĘ", "PIERDOLEC",
"PIERDOLA", "PIERDOLĄ", "PIERDOLIĆ", "PIERDOLICIE", "PIERDOLIC",
"PIERDOLIŁ", "PIERDOLIL", "PIERDOLIŁA", "PIERDOLILA", "PIERDOLI",
"PIERDOLNIĘTY", "PIERDOLNIETY", "PIERDOLISZ", "PIERDOLNĄĆ",
"PIERDOLNAC", "PIERDOLNĄŁ", "PIERDOLNAL", "PIERDOLNĘŁA", "PIERDOLNELA",
"PIERDOLNIE", "PIERDOLNIĘTY", "PIERDOLNIJ", "PIERDOLNIK", "PIERDOLONA",
"PIERDOLONE", "PIERDOLONY", "PIERDOŁKI", "PIERDZĄCY", "PIERDZIEĆ",
"PIERDZIEC", "PIZDA", "PIZDĄ", "PIZDE", "PIZDĘ", "PIŹDZIE", "PIZDZIE",
"PIZDNĄĆ", "PIZDNAC", "PIZDU", "PODPIERDALAĆ", "PODPIERDALAC",
"PODPIERDALA", "PODPIERDALAJĄCY", "PODPIERDALAJACY", "PODPIERDOLIĆ",
"PODPIERDOLIC", "PODPIERDOLI", "POJEB", "POJEBA", "POJEBAMI",
"POJEBANI", "POJEBANEGO", "POJEBANEMU", "POJEBANI", "POJEBANY",
"POJEBANYCH", "POJEBANYM", "POJEBANYMI", "POJEBEM", "POJEBAĆ",
"POJEBAC", "POJEBALO", "POPIERDALA", "POPIERDALAC", "POPIERDALAĆ",
"POPIERDOLIĆ", "POPIERDOLIC", "POPIERDOLI", "POPIERDOLONEGO",
"POPIERDOLONEMU", "POPIERDOLONYM", "POPIERDOLONE", "POPIERDOLENI",
"POPIERDOLONY", "POROZPIERDALAĆ", "POROZPIERDALA", "POROZPIERDALAC",
"PORUCHAC", "PORUCHAĆ", "PRZEJEBAĆ", "PRZEJEBANE", "PRZEJEBAC",
"PRZYJEBALI", "PRZEPIERDALAĆ", "PRZEPIERDALAC", "PRZEPIERDALA",
"PRZEPIERDALAJĄCY", "PRZEPIERDALAJACY", "PRZEPIERDALAJĄCA",
"PRZEPIERDALAJACA", "PRZEPIERDOLIĆ", "PRZEPIERDOLIC", "PRZYJEBAĆ",
"PRZYJEBAC", "PRZYJEBIE", "PRZYJEBAŁA", "PRZYJEBALA", "PRZYJEBAŁ",
"PRZYJEBAL", "PRZYPIEPRZAĆ", "PRZYPIEPRZAC", "PRZYPIEPRZAJĄCY",
"PRZYPIEPRZAJACY", "PRZYPIEPRZAJĄCA", "PRZYPIEPRZAJACA",
"PRZYPIERDALAĆ", "PRZYPIERDALAC", "PRZYPIERDALA", "PRZYPIERDOLI",
"PRZYPIERDALAJĄCY", "PRZYPIERDALAJACY", "PRZYPIERDOLIĆ",
"PRZYPIERDOLIC", "QRWA", "ROZJEBAĆ", "ROZJEBAC", "ROZJEBIE",
"ROZJEBAŁA", "ROZJEBIĄ", "ROZPIERDALAĆ", "ROZPIERDALAC", "ROZPIERDALA",
"ROZPIERDOLIĆ", "ROZPIERDOLIC", "ROZPIERDOLE", "ROZPIERDOLI",
"ROZPIERDUCHA", "SKURWIĆ", "SKURWIEL", "SKURWIELA", "SKURWIELEM",
"SKURWIELU", "SKURWYSYN", "SKURWYSYNÓW", "SKURWYSYNOW", "SKURWYSYNA",
"SKURWYSYNEM", "SKURWYSYNU", "SKURWYSYNY", "SKURWYSYŃSKI",
"SKURWYSYNSKI", "SKURWYSYŃSTWO", "SKURWYSYNSTWO", "SPIEPRZAĆ",
"SPIEPRZAC", "SPIEPRZA", "SPIEPRZAJ", "SPIEPRZAJCIE", "SPIEPRZAJĄ",
"SPIEPRZAJA", "SPIEPRZAJĄCY", "SPIEPRZAJACY", "SPIEPRZAJĄCA",
"SPIEPRZAJACA", "SPIERDALAĆ", "SPIERDALAC", "SPIERDALA", "SPIERDALAŁ",
"SPIERDALAŁA", "SPIERDALAL", "SPIERDALALCIE", "SPIERDALALA",
"SPIERDALAJĄCY", "SPIERDALAJACY", "SPIERDOLIĆ", "SPIERDOLIC",
"SPIERDOLI", "SPIERDOLIŁA", "SPIERDOLIŁO", "SPIERDOLĄ", "SPIERDOLA",
"SRAĆ", "SRAC", "SRAJĄCY", "SRAJACY", "SRAJĄC", "SRAJAC", "SRAJ",
"SUKINSYN", "SUKINSYNY", "SUKINSYNOM", "SUKINSYNOWI", "SUKINSYNÓW",
"SUKINSYNOW", "ŚMIERDZIEL", "UDUPIĆ", "UJEBAĆ", "UJEBAC", "UJEBAŁ",
"UJEBAL", "UJEBANA", "UJEBANY", "UJEBIE", "UJEBAŁA", "UJEBALA",
"UPIERDALAĆ", "UPIERDALAC", "UPIERDALA", "UPIERDOLI", "UPIERDOLIĆ",
"UPIERDOLIC", "UPIERDOLI", "UPIERDOLĄ", "UPIERDOLA", "UPIERDOLENI",
"WJEBAĆ", "WJEBAC", "WJEBIE", "WJEBIĄ", "WJEBIA", "WJEBIEMY",
"WJEBIECIE", "WKURWIAĆ", "WKURWIAC", "WKURWI", "WKURWIA", "WKURWIAŁ",
"WKURWIAL", "WKURWIAJĄCY", "WKURWIAJACY", "WKURWIAJĄCA", "WKURWIAJACA",
"WKURWIĆ", "WKURWIC", "WKURWI", "WKURWIACIE", "WKURWIAJĄ", "WKURWIALI",
"WKURWIĄ", "WKURWIA", "WKURWIMY", "WKURWICIE", "WKURWIACIE", "WKURWIĆ",
"WKURWIC", "WKURWIA", "WPIERDALAĆ", "WPIERDALAC", "WPIERDALAJĄCY",
"WPIERDALAJACY", "WPIERDOL", "WPIERDOLIĆ", "WPIERDOLIC", "WPIZDU",
"WYJEBAĆ", "WYJEBAC", "WYJEBALI", "WYJEBAŁ", "WYJEBAC", "WYJEBAŁA",
"WYJEBAŁY", "WYJEBIE", "WYJEBIĄ", "WYJEBIA", "WYJEBIESZ", "WYJEBIE",
"WYJEBIECIE", "WYJEBIEMY", "WYPIEPRZAĆ", "WYPIEPRZAC", "WYPIEPRZA",
"WYPIEPRZAŁ", "WYPIEPRZAL", "WYPIEPRZAŁA", "WYPIEPRZALA", "WYPIEPRZY",
"WYPIEPRZYŁA", "WYPIEPRZYLA", "WYPIEPRZYŁ", "WYPIEPRZYL", "WYPIERDAL",
"WYPIERDALAĆ", "WYPIERDALAC", "WYPIERDALA", "WYPIERDALAJ",
"WYPIERDALAŁ", "WYPIERDALAL", "WYPIERDALAŁA", "WYPIERDALALA",
"WYPIERDALAĆ", "WYPIERDOLIĆ", "WYPIERDOLIC", "WYPIERDOLI",
"WYPIERDOLIMY", "WYPIERDOLICIE", "WYPIERDOLĄ", "WYPIERDOLA",
"WYPIERDOLILI", "WYPIERDOLIŁ", "WYPIERDOLIL", "WYPIERDOLIŁA",
"WYPIERDOLILA", "ZAJEBAĆ", "ZAJEBAC", "ZAJEBIE", "ZAJEBIĄ", "ZAJEBIA",
"ZAJEBIAŁ", "ZAJEBIAL", "ZAJEBAŁA", "ZAJEBIALA", "ZAJEBALI", "ZAJEBANA",
"ZAJEBANI", "ZAJEBANE", "ZAJEBANY", "ZAJEBANYCH", "ZAJEBANYM",
"ZAJEBANYMI", "ZAJEBISTE", "ZAJEBISTY", "ZAJEBISTYCH", "ZAJEBISTA",
"ZAJEBISTYM", "ZAJEBISTYMI", "ZAJEBIŚCIE", "ZAJEBISCIE", "ZAPIEPRZYĆ",
"ZAPIEPRZYC", "ZAPIEPRZY", "ZAPIEPRZYŁ", "ZAPIEPRZYL", "ZAPIEPRZYŁA",
"ZAPIEPRZYLA", "ZAPIEPRZĄ", "ZAPIEPRZA", "ZAPIEPRZY", "ZAPIEPRZYMY",
"ZAPIEPRZYCIE", "ZAPIEPRZYSZ", "ZAPIERDALA", "ZAPIERDALAĆ",
"ZAPIERDALAC", "ZAPIERDALAJA", "ZAPIERDALAŁ", "ZAPIERDALAJ",
"ZAPIERDALAJCIE", "ZAPIERDALAŁA", "ZAPIERDALALA", "ZAPIERDALALI",
"ZAPIERDALAJĄCY", "ZAPIERDALAJACY", "ZAPIERDOLIĆ", "ZAPIERDOLIC",
"ZAPIERDOLI", "ZAPIERDOLIŁ", "ZAPIERDOLIL", "ZAPIERDOLIŁA",
"ZAPIERDOLILA", "ZAPIERDOLĄ", "ZAPIERDOLA", "ZAPIERNICZAĆ",
"ZAPIERNICZAJĄCY", "ZASRAĆ", "ZASRANYM", "ZASRYWAĆ", "ZASRYWAJĄCY",
"ZESRYWAĆ", "ZESRYWAJĄCY", "ZJEBAĆ", "ZJEBAC", "ZJEBAŁ", "ZJEBAL",
"ZJEBAŁA", "ZJEBALA", "ZJEBANA", "ZJEBIĄ", "ZJEBALI", "ZJEBY"]
link_blacklist = ["discord.gg/", "discord.com/invite/", "discordapp.com/invite/"]

def load(gateway, discord):
    @gateway.event
    def GUILD_MEMBER_ADD(ctx):
        guild = ctx.data["guild_id"]
        guilds = functions.read_json("guilds")

        if not guild in guilds:
            return

        if "welcomemsg" in guilds[guild]:
            discord.create_message(guilds[guild]["welcomemsg"]["channel_id"], {
                "content": guilds[guild]["welcomemsg"]["text"].replace("<>", ctx.data["user"]["username"]).replace("[]", "<@" + ctx.data["user"]["id"] + ">").replace("{}", str(len(discord.list_guild_members(ctx.data["guild_id"]))))
            })

        if "autorole" in guilds[guild]:
            discord.add_guild_member_role(ctx.data["guild_id"], ctx.data["user"]["id"], guilds[guild]["autorole"])

    @gateway.event
    def GUILD_MEMBER_REMOVE(ctx):
        guild = ctx.data["guild_id"]
        guilds = functions.read_json("guilds")

        if not guild in guilds:
            return

        if "leavemsg" in guilds[guild]:
            discord.create_message(guilds[guild]["leavemsg"]["channel_id"], {
                "content": guilds[guild]["leavemsg"]["text"].replace("<>", ctx.data["user"]["username"]).replace("[]", "<@" + ctx.data["user"]["id"] + ">").replace("{}", str(len(discord.list_guild_members(ctx.data["guild_id"]))))
            })

    @gateway.event
    def MESSAGE_CREATE(ctx):
        guild = ctx.data["guild_id"]
        guilds = functions.read_json("guilds")

        if not guild in guilds:
            guilds[guild] = {}
            functions.write_json("guilds", guilds)

        if "bot" in ctx.data["author"]:
            return

        user = ctx.data["author"]["id"]
        users = functions.read_json("users")

        if not user in users:
            users[user] = {}
            functions.write_json("users", users)

        if not hasattr(ctx, "messages"):
            ctx.messages = {}

        if not ctx.data["guild_id"] in ctx.messages:
            ctx.messages[ctx.data["guild_id"]] = {}

        ctx.messages[ctx.data["guild_id"]][ctx.data["id"]] = {
            "author": ctx.data["author"],
            "content": ctx.data["content"],
            "channel_id": ctx.data["channel_id"]
        }

        mentions = [user["id"] for user in ctx.data["mentions"]]

        if ctx.bot["id"] in mentions and len(ctx.args) == 1:
            guild = ctx.data["guild_id"]
            guilds = functions.read_json("guilds")

            if guild in guilds and "prefix" in guilds[guild]:
                prefix = guilds[guild]["prefix"]
            else:
                prefix = "!!"

            return discord.create_message(ctx.data["channel_id"], {
                "content": f"Mój prefix na tym serwerze to `{prefix}`"
            })

        if guild in guilds and "cmd" in guilds[guild] and ctx.data["content"] in guilds[guild]["cmd"]:
            discord.create_message(ctx.data["channel_id"], {
                "content": guilds[guild]["cmd"][ctx.data["content"]]["text"].replace("<>", ctx.data["author"]["username"]).replace("[]", "<@" + ctx.data["author"]["id"] + ">")
            })

        if permissions.has_permission(ctx, ctx.data["author"]["id"], "ADMINISTRATOR"):
            return
        
        channel = discord.get_channel(ctx.data["channel_id"])
        
        if not channel["nsfw"] and guild in guilds and not "badwords" in guilds[guild]:
            for badword in badwords_list:
                if badword in ctx.data["content"].upper():
                    status = discord.delete_message(ctx.data["channel_id"], ctx.data["id"])
                    if status.status_code == 204:
                        discord.create_message(ctx.data["channel_id"], {
                            "content": "Na tym serwerze przeklinanie jest wyłączone"
                        })

        elif guild in guilds and not "invites" in guilds[guild]:
            for link in link_blacklist:
                if link.upper() in ctx.data["content"].upper():
                    status = discord.delete_message(ctx.data["channel_id"], ctx.data["id"])
                    if status.status_code == 204:
                        discord.create_message(ctx.data["channel_id"], {
                            "content": "Na tym serwerze wysyłanie zaproszeń jest wyłączone"
                        })

    @gateway.event
    def MESSAGE_DELETE(ctx):
        if not hasattr(ctx, "snipe"):
            ctx.snipe = {}

        if not ctx.data["guild_id"] in ctx.snipe:
            ctx.snipe[ctx.data["guild_id"]] = []
            
        ctx.snipe[ctx.data["guild_id"]].append(ctx.messages[ctx.data["guild_id"]][ctx.data["id"]])

    @gateway.event
    def GUILD_ROLE_DELETE(ctx):
        guild = ctx.data["guild_id"]
        role = ctx.data["role_id"]

        guilds = functions.read_json("guilds")

        if "mute_role" in guilds[guild] and guilds[guild]["mute_role"] == role:
            del guilds[guild]["mute_role"]
            functions.write_json("guilds", guilds)