""" basic bot commands. """

from bot.run import kernel
from obj.base import get_type
from obj.loader import Loader

def fleet(event):
    try:
        nr = int(event.args[0])
    except (IndexError, ValueError):
        event.reply(str([get_type(b) for b in kernel.bots]))
        return
    try:
        event.reply(str(kernel.bots[nr]))
    except IndexError:
        pass

def load(event):
    if not event.args:
        loader = Loader()
        loader.walk("obj")
        loader.walk("bot")
        event.reply("|".join(sorted([x.split(".")[-1] for x in ref.table.keys()])))
        return
    name = event.args[0]
    try:
        mod = kernel.walk(name)
    except:
        event.reply(get_exception())
    event.reply("%s loaded" % name)

def unload(event):
    if not event.args:
        loader = Loader()
        loader.walk("obj.cmds")
        loader.walk("bot")
        event.reply("|".join(loader.table.keys()))
        return
    name = event.args[0]
    broker = Broker()
    ref = broker.get(event.orig)
    try:
        del kernel.table[name]
    except KeyError:
        event.reply("%s is not loaded." % name)        
        return
    event.reply("unload %s" % name)
