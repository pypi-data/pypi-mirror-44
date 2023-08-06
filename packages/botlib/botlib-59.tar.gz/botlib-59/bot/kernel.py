""" main loop. """

import logging
import os
import sys
import threading
import time

from bot import __version__
from bot.fleet import Fleet

from obj.base import Dotted, OutputCache, cfg, cdir, get_type
from obj.command import Command
from obj.handler import Handler
from obj.shell import set_completer, start, startup, reset
from obj.store import Store
from obj.tasks import launch
from obj.utils import get_cls, get_exception, get_name, hd

defaults = Dotted()
defaults.background = ""
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

class Kernel(Handler, Fleet, Store):

    def __init__(self):
        super().__init__()
        self._in = sys.stdin    
        self._out = sys.stdout
        self._err = sys.stderr
        self._type = get_type(self)
        self.cfg = Cfg(defaults)
        self.mods = []
        self.loaded = []

    def dispatch(self, event):
        logging.warn("dispatch %s" % event.txt)
        event._func = self.get_cmd(event)
        if event._func:
            event._func(event)
            event.show()
        event.ready()


    def start(self, name, version=__version__, wd=""):
        super().start()
        shell = start(name, version, wd)
        self.add(shell)
        return shell
