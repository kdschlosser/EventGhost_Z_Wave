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


class Dispatcher(object):
    __callbacks = {}
    __blocked_networks = {}

    def __init__(self):
        import sys
        mod = sys.modules[__name__]
        self.__dict__ = mod.__dict__
        sys.modules[__name__] = self

    def connect(self, callback, signal):
        if signal not in self.__callbacks:
            self.__callbacks[signal] = set()
        self.__callbacks[signal].add(callback)

    def disconnect(self, callback, signal):
        if signal in self.__callbacks:
            self.__callbacks[signal].discard(callback)
            if not len(self.__callbacks[signal]):
                del self.__callbacks[signal]

    def send(self, signal, sender, *args, **kwargs):
        if sender in self.__blocked_networks:
            self.__blocked_networks[sender](
                signal=signal,
                sender=sender,
                *args,
                **kwargs
            )
        elif (
            'network' in kwargs and
            kwargs['network'] in self.__blocked_networks
        ):
            self.__blocked_networks[sender](
                signal=signal,
                sender=sender,
                *args,
                **kwargs
            )
        elif signal in self.__callbacks:
            for callback in self.__callbacks[signal]:
                callback(signal=signal, sender=sender, *args, **kwargs)

    def set_redirect(self, network, callback):
        if network not in self.__blocked_networks:
            self.__blocked_networks[network] = callback

    def unset_redirect(self, network):

        if network in self.__blocked_networks:
            del self.__blocked_networks[network]


dispatcher = Dispatcher()
connect = dispatcher.connect
disconnect = dispatcher.disconnect
send = dispatcher.send
set_redirect = dispatcher.set_redirect
unset_redirect = dispatcher.unset_redirect
