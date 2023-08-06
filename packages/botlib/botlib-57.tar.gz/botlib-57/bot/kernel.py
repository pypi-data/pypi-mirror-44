""" main loop. """

import logging
import os
import sys
import threading
import time

from bot.event import Event
from bot.fleet import Fleet
from bot.poller import Poller

from obj.base import Dotted, cfg, cdir, get_type, __version__
from obj.command import Command
from obj.store import Store
from obj.tasks import launch
from obj.utils import get_cls, get_exception, get_name, hd

def init():
    from bot.run import kernel
    bot = Shell()
    kernel.add(bot)
    thr = launch(bot.start)
    return thr

defaults = Dotted()
defaults.exclude = ""
defaults.logdir = ""
defaults.modules = ""
defaults.name = "bot"
defaults.options = ""
defaults.shell = False
defaults.usage = ""
defaults.version = __version__
defaults.wait = True
defaults.workdir = ""

class Cfg(Dotted):

    _default = ""

class Kernel(Fleet, Poller, Store):

    def __init__(self):
        super().__init__()
        self._in = sys.stdin    
        self._out = sys.stdout
        self._err = sys.stderr
        self.cfg = Cfg(defaults)
        self.prompt = False
        self.verbose = False
        self.loaded = []

    def say(self, orig, channel, txt):
        if self.verbose:
            self._out.write(str(txt))
            self._out.write("\n")
            self._out.flush()
        
    def unload(self, name):
        for bot in self.bots:
            bot.unload(name)
