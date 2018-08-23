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

VENDOR_IDS = (('Aeon Labs Gen5', 'VID_0658'),)


# noinspection PyUnresolvedReferences
class Discovery(object):

    def __init__(self):
        import threading

        self.vendor_ids = VENDOR_IDS
        self.in_event = threading.Event()
        self.out_event = threading.Event()
        self.event = threading.Event()
        self._devices = None
        self._thread = None

        import sys

        mod = sys.modules[__name__]
        self.__dict__.update(mod.__dict__)
        sys.modules[__name__] = self

    def start(self):
        if self._thread is None:
            import threading

            self._thread = threading.Thread(target=self.run)
            self._thread.start()

    def run(self):
        import pythoncom
        import win32com.client
        import win32com

        pythoncom.CoInitialize()
        wmi_obj = win32com.client.GetObject("winmgmts:\\root\\cimv2")

        while not self.event.isSet():
            self.in_event.wait()
            if self.event.isSet():
                break
            for vendor_name, vid in self.vendor_ids:
                # noinspection PyShadowingNames
                devices = wmi_obj.ExecQuery(
                    'Select DeviceID from Win32_SerialPort '
                    'where PNPDeviceID like "%' + vid + '%" '
                )

                coms = []
                for device in devices:
                    coms += [device.DeviceID]

                self._devices = coms

            self.in_event.clear()
            self.out_event.set()
        # noinspection PyPep8,PyBroadException
        try:
            pythoncom.CoUninitialize()
        except:
            pass

        self.event.clear()
        self.in_event.clear()
        self.out_event.clear()
        self._thread = None

    def stop(self):
        if self._thread is not None:
            self.event.set()
            self.in_event.set()
            self._thread.join(1.0)

    @property
    def devices(self):
        if not self.is_running:
            self.start()

        self.in_event.set()
        self.out_event.wait()
        self.out_event.clear()
        return self._devices

    @property
    def is_running(self):
        return self._thread is not None


discovery = Discovery()

start = discovery.start
stop = discovery.stop
devices = []
is_running = False
