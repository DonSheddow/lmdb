#!/usr/bin/env python
import pyinotify
from os.path import basename
from contextlib import contextmanager

from lmdb import app

from films import add_film


wm = pyinotify.WatchManager()
mask = pyinotify.IN_CREATE | pyinotify.IN_DELETE | pyinotify.IN_MOVED_TO | pyinotify.IN_MOVED_FROM

class EventHandler(pyinotify.ProcessEvent):
    
    def process_IN_CREATE(self, event):
        pathname = basename(event.pathname)
        add_film(pathname)


handler = EventHandler()
notifier = pyinotify.Notifier(wm, handler)

wdd = wm.add_watch(app.config['FILM_DIR'], mask)

notifier.loop(daemonize=True, stdout='/tmp/lmdb.out', stderr='/tmp/lmdb.out', pid_file='/tmp/lmdb.pid')
