""" main loop. """

import logging
import os
import sys
import threading
import time

from bot import __version__
from bot.event import Event
from bot.fleet import Fleet
from bot.poller import Poller

from obj.base import Dotted, OutputCache, cfg, cdir, get_type
from obj.command import Command
from obj.loader import names
from obj.shell import level, opts, parse_cli, set_completer, start, startup, reset
from obj.store import Store
from obj.tasks import launch
from obj.utils import get_cls, get_exception, get_name, hd

def init():
    from bot.run import kernel
    return kernel.start()

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

class Kernel(Poller, Fleet, Store):

    def __init__(self):
        super().__init__()
        self._in = sys.stdin    
        self._out = sys.stdout
        self._err = sys.stderr
        self._type = get_type(self)
        self.cfg = Cfg(defaults)
        self.mods = []
        self.loaded = []

    def start(self, name, bots=[], modules="",  version=__version__, wd=""):
        start(name, bots, modules, version, wd)
