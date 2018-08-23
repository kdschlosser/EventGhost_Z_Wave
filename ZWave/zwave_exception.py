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


class ZWaveException(Exception):
    """
    Exception class for OpenZWave
    """
    msg = u"Zwave Generic Exception"

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.msg+' : '+self.value)


class ZWaveCacheException(ZWaveException):
    """
    Exception class for OpenZWave
    """
    msg = u"Zwave Cache Exception"


class ZWaveTypeException(ZWaveException):
    """
    Exception class for OpenZWave
    """
    msg = u"Zwave Type Exception"


class ZWaveCommandClassException(ZWaveException):
    """
    Exception class for OpenZWave
    """
    msg = u"Zwave Command Class Exception"
