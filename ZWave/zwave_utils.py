# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
# Copyright © 2005-2016 EventGhost Project <http://www.eventghost.net/>
#
# EventGhost is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 2 of the License, or (at your option)
# any later version.
#
# EventGhost is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along
# with EventGhost. If not, see <http://www.gnu.org/licenses/>.


import threading
import wx

_threads = {}
_lock = threading.Lock()


def thread_call_wait(func):
    _threads[func] = []

    def wrapper(*args, **kwargs):
        def do(*a, **k):
            try:
                func(*a, **k)
            except wx.PyDeadObjectError:
                pass
            with _lock:
                _threads[func].pop(0)
                if _threads[func]:
                    _threads[func][0].start()

        t = threading.Thread(target=do, args=args, kwargs=kwargs)
        t.daemon = True
        with _lock:
            _threads[func] += [t]
            if len(_threads[func]) == 1:
                t.start()
        return t

    return wrapper


def thread_call(func):
    def wrapper(*args, **kwargs):
        t = threading.Thread(target=func, args=args, kwargs=kwargs)
        t.daemon = True
        t.start()
        return t

    return wrapper


def remap(value, old_min, old_max, new_min, new_max):
    old_range = old_max - old_min
    new_range = new_max - new_min

    return (((value - old_min) * new_range) / old_range) + new_min
