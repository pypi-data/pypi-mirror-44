# bot/email.py
#
#

""" email scanning module. """

import logging
import mailbox
import os

from obj.base import Dotted
from obj.store import Store
from obj.utils import get_exception

## defines

bdmonths = ['Bo', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug',
            'Sep', 'Oct', 'Nov', 'Dec']

monthint = {
    'Jan': 1,
    'Feb': 2,
    'Mar': 3,
    'Apr': 4,
    'May': 5,
    'Jun': 6,
    'Jul': 7,
    'Aug': 8,
    'Sep': 9,
    'Oct': 10,
    'Nov': 11,
    'Dec': 12
}

## classes

class Email(Dotted):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.text = ""

## functions

def to_date(date):
    date = date.replace("_", ":")
    res = date.split()
    ddd = ""
    try:
        if "+" in res[3]:
            raise ValueError
        if "-" in res[3]:
            raise ValueError
        int(res[3])
        ddd = "{:4}-{:#02}-{:#02} {:6}".format(res[3], monthint[res[2]], int(res[1]), res[4])
    except (IndexError, KeyError, ValueError):
        try:
            if "+" in res[4]:
                raise ValueError
            if "-" in res[4]:
                raise ValueError
            int(res[4])
            ddd = "{:4}-{:#02}-{:02} {:6}".format(res[4], monthint[res[1]], int(res[2]), res[3])
        except (IndexError, KeyError, ValueError):
            try:
                ddd = "{:4}-{:#02}-{:02} {:6}".format(res[2], monthint[res[1]], int(res[0]), res[3])
            except (IndexError, KeyError):
                try:
                    ddd = "{:4}-{:#02}-{:02}".format(res[2], monthint[res[1]], int(res[0]))
                except (IndexError, KeyError):
                    try:
                        ddd = "{:4}-{:#02}".format(res[2], monthint[res[1]])
                    except (IndexError, KeyError):
                        try:
                            ddd = "{:4}".format(res[2])
                        except (IndexError, KeyError):
                            ddd = ""
    return ddd

## instances

store = Store()

## commands

def mbox(event):
    if not event.args:
        event.reply("mbox <path>")
        return
    fn = os.path.expanduser(event.args[0])
    event.reply("reading from %s" % fn)
    nr = 0
    if os.path.isdir(fn):
        thing = mailbox.Maildir(fn, create=False)
    elif os.path.isfile(fn):
        thing = mailbox.mbox(fn, create=False)
    else:
        event.reply("need a mbox or maildir.")
        return
    try:
        thing.lock()
    except FileNotFoundError:
        pass
    for m in thing:
        try:
            obj = Email()
            obj.update(m.items())
            try:
                sdate = os.sep.join(to_date(obj.Date).split())
            except AttributeError:
                sdate = None
            obj.text = ""
            for payload in m.walk():
                if payload.get_content_type() == 'text/plain':
                    obj.text += payload.get_payload()
            obj.text = obj.text.replace("\\n", "\n")
            if sdate:
                obj.save(stime=sdate)
            else:
                obj.save()
            nr += 1
        except Exception:
            logging.error(get_exception())
    if nr:
        event.reply("ok %s" % nr)

def cor(event):
    if not event.args:
        event.reply("cor <email>")
        return
    email = event.args[0]
    for email in store.find("bot.email.Email", event.selector):
        event.display(email)
