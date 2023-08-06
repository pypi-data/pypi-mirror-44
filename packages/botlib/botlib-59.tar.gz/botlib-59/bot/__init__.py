""" bot package. """

__version__ = 59

import logging
import sys

from bot.event import Event
from bot.run import kernel
from obj.base import Dotted, OutputCache, cdir, cfg
from obj.handler import Handler
from obj.tasks import launch
from obj.utils import get_name, hd

class Bot(Handler):

    def __init__(self):
        super().__init__()
        self.cache = OutputCache()
        self.channels = []
        self.prompt = False
        self.state = Dotted()
        self.verbose = True

    def announce(self, txt):
        for channel in self.channels:
            self.say(channel, txt)

    def cmd(self, txt, options="", origin=""):
        if not cfg.workdir:
            cfg.workdir = hd(".bot")
            cdir(cfg.workdir)
        self.start()
        txt = self.get_aliased(txt)
        e = Event(txt)
        e.orig = repr(self)
        e.options = options
        e.origin = origin or "root@shell"
        self.dispatch(e)
        self.ready()
        return e

    def dispatch(self, event):
        kernel.dispatch(event)

    def fileno(self):
        return sys.stdin

    def join(self):
        pass

    def raw(self, txt):
        print(txt)

    def resume(self):
        pass

    def say(self, botid, channel, txt):
        if self.verbose:
            self.cache.add(channel, txt)
            self.raw(txt)

    def show_prompt(self):
        pass

    def start(self):
        super().start()
        kernel.add(self)

    def work(self):
        while not self._stopped:
            event = self._queue.get()
            if not event:
                break
            self.dispatch(event)
        self.ready()
