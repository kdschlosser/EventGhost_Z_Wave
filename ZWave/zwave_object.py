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


import logging
import warnings
from zwave_exception import ZWaveCacheException

logger = logging.getLogger('openzwave')


def deprecated(func):
    """
    This is a decorator which can be used to mark functions
    as deprecated. It will result in a warning being emitted
    when the function is used.
    """
    def new_func(*args, **kwargs):
        warnings.simplefilter('always', DeprecationWarning)# turn off filter
        warnings.warn("Call to deprecated function {}.".format(func.__name__),
                      category=DeprecationWarning, stacklevel=2)
        warnings.simplefilter('default', DeprecationWarning) # reset filter
        return func(*args, **kwargs)
    new_func.__name__ = func.__name__
    new_func.__doc__ = func.__doc__
    new_func.__dict__.update(func.__dict__)
    return new_func


class ZWaveObject(object):
    """
    Represents a Zwave object. Values, nodes, ... can be changer by
    other managers on the network.
    """

    def __init__(self, object_id, network=None, use_cache=True):
        """
        Initialize a Zwave object

        :param object_id: ID of the object
        :type object_id: int, None
        :param network: The network object to access the manager
        :type network: ZWaveNetwork
        """
        self._network = network
        self._last_update = None
        self._outdated = True
        self._use_cache = use_cache
        self._object_id = object_id
        if self._use_cache:
            self._cached_properties = dict()
        else:
            self._cached_properties = None

    @property
    def home_id(self):
        """
        The home_id of the node.

        :rtype: int
        """
        if self._network is not None:
            return self._network.home_id

    @home_id.setter
    def home_id(self, _):
        raise NotImplementedError

    @property
    def network(self):
        """
        The network of the node.

        :rtype: ZWaveNetwork
        """
        return self._network

    @property
    def use_cache(self):
        """
        Should this object use cache from property

        :rtype: bool
        """
        return self._use_cache

    @property
    def last_update(self):
        """
        The last update date of the device.

        :rtype: time
        """
        return self._last_update

    @last_update.setter
    def last_update(self, value):
        """
        Set the last update date of the device.

        :param value: The time of last update
        :type value: time
        """
        self._last_update = value

    @property
    def outdated(self):
        """
        Are the information of this object outdated.

        How to manage the cache ?

        2 ways of doing it :
        - refresh information when setting the property
        - refresh information when getting getting property.
        Maybe whe could implement the 2 methods.

        :rtype: int
        """
        return self._outdated

    @outdated.setter
    def outdated(self, value):
        """
        Set that this object ist outdated.

        :param value: True
        :type value: bool - True
        """
        if self._use_cache:
            if value:
                for prop in self._cached_properties:
                    self._cached_properties[prop] = True
                self._outdated = value
            else:
                raise ZWaveCacheException(
                    u"Can't set outdated to False manually."
                    u" It is done automatically."
                )
        else:
            raise ZWaveCacheException(u"Cache not enabled")

    def is_outdated(self, prop):
        """
        Check if property information is outdated.

        :param prop: The property to check
        :type prop: lambda
        :rtype: bool
        """
        if self._use_cache:
            if str(prop) in self._cached_properties:
                # print "property in cache %s" %
                # self._cached_properties[str(prop)]
                return self._cached_properties[str(prop)]
            else:
                # This property is not cached so return true
                return True
        else:
            raise ZWaveCacheException(u"Cache not enabled")

    def outdate(self, prop):
        """
        Sets a property to outdated.

        :param prop: The property to out date
        :type prop: int
        """
        if self._use_cache:
            if str(prop) in self._cached_properties:
                self._cached_properties[str(prop)] = True
                self._outdated = True
        else:
            raise ZWaveCacheException(u"Cache not enabled")

    def update(self, prop):
        """
        Says that the property are updated.

        :param prop: The property to update
        :type prop: lambda
        """
        if self._use_cache:
            if str(prop) in self._cached_properties:
                self._cached_properties[str(prop)] = False
                out_dated = False
                for prop in self._cached_properties:
                    if self._cached_properties[prop]:
                        out_dated = True
                        break
                self._outdated = out_dated
        else:
            raise ZWaveCacheException(u"Cache not enabled")

    def cache_property(self, prop):
        """
        Add this property to the cache manager.

        :param prop: The property to cache
        :type prop: lambda
        """
        if self._use_cache:
            self._cached_properties[str(prop)] = True
        else:
            raise ZWaveCacheException(u"Cache not enabled")

    @property
    def object_id(self):
        """
        The id of the object.
        object_id could be None, when creating a scene for example.

        :rtype: int
        """
        return self._object_id

    @property
    def object_id_str(self):
        return '0x' + hex(self._object_id)[2:].upper()

    @property
    def command_class(self):
        raise NotImplementedError

    def __eq__(self, other):
        if isinstance(other, int):
            if hasattr(self, '_cls_ids'):
                return other in self._cls_ids

            try:
                return other == self.command_class
            except NotImplementedError:
                return False

        return getattr(other, '_object_id', None) == self._object_id
