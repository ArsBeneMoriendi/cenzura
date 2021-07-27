from .ctx import ctx
import importlib

bot, discord = None, None

def load_modules(_bot, _discord, *modules):
    global bot, discord
    bot, discord = _bot, _discord
    
    for module_name in modules:
        importlib.reload(__import__(module_name))

def reload(*modules):
    for module_name in modules:
        importlib.reload(__import__(module_name))

def module(Module):
    ctx.modules[Module.__name__] = Module(bot, discord)
    
def event(func):
    ctx.events[func.__name__] = func
    
def command(**kwargs):
    def _command(func):                
        kwargs["function"] = func
        ctx.commands[func.__name__] = kwargs

    return _command