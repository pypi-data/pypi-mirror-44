""" place to stash runtime objects. """

import sys

from obj.base import Cfg
from obj.shell import Shell
from bot.kernel import Kernel
from bot.users import Users

cfg = Cfg()
kernel = Kernel()
users = Users()

def cmd(txt):
    s = Shell()
    s.prompt = False
    s.verbose = False
    e = s.cmd(txt)
    e.wait()
    return e
    
def get(name):
    return getattr(sys.modules[__name__], name, None)

def set(name, obj):
    return setattr(sys.modules[__name__], name, obj)
