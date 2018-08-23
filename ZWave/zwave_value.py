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
import threading
import dispatcher
import zwave_command_classes
from zwave_object import ZWaveObject

logger = logging.getLogger('openzwave')


class ValuesContainer(object):

    def __init__(self):
        self._values = {}

    def __radd__(self, other):
        if isinstance(other, dict):
            other = ZWaveValue(**other)

        self._values[other.id] = other
        return self

    def __add__(self, other):
        self._values[other['id']] = ZWaveValue(**other)
        return self._values[other['id']]

    def __rsub__(self, other):
        if isinstance(other, int):
            del self._values[other]
        else:
            del self._values[other.id]
        return self

    def __contains__(self, item):
        if isinstance(item, dict):
            return item['id'] in self._values

        return item in self._values

    def __getitem__(self, item):
        if isinstance(item, dict):
            if item['id'] in self._values:
                return self._values[item['id']]
        elif item in self._values:
            return self._values[item]

        raise KeyError(item)

    def __iter__(self):
        keys = sorted(self._values.keys(), key=int)

        for key in keys:
            yield self._values[key]

    def __setitem__(self, key, value):
        if isinstance(key, dict):
            key = key['id']

        self._values[key] = ZWaveValue(**value)

    def pop(self, value, default=None):
        if isinstance(value, dict):
            return self._values.pop(value['id'], default)
        else:
            return self._values.pop(value, default)

    def values(self):
        return self._values.values()

    def keys(self):
        return self._values.keys()

    def items(self):
        return self._values.items()

    def __eq__(self, other):
        for value in self._values.values():
            if value.command_class == other:
                return True
        return False


class ValueTimer(object):

    def __init__(self, time_out, func):
        self._thread = threading.Thread(target=self.run)
        self._event = threading.Event()
        self._func = func
        self._time_out = time_out

    def __call__(self, *args, **kwargs):
        self._args = args
        self._kwargs = kwargs
        self._thread.start()

    def run(self):
        self._event.wait(self._time_out)
        if not self._event.isSet():
            self._func(*self._args, **self._kwargs)
            self._event.set()
        self._thread = None

    def cancel(self):
        if self._thread is not None and self._thread.is_alive():
            self._event.set()


# noinspection PyPep8Naming,PyShadowingBuiltins
class ZWaveValue(ZWaveObject):

    def __init__(
        self,
        node,
        network,
        homeId,
        nodeId,
        commandClass,
        instance,
        index,
        id,
        genre,
        type,
        value,
        label,
        units,
        readOnly
    ):
        ZWaveObject.__init__(self, id, network=network)
        logger.debug(u"Create object value (valueId:%s)", id)
        self._node = node
        self._data = value
        self._homeId = homeId
        self._nodeId = nodeId
        self._commandClass = commandClass
        self._instance = instance
        self._index = index
        self._id = id
        self._genre = genre
        self._type = type
        self._label = label
        self._units = units
        self._readOnly = readOnly
        self._poll_intensity = 0

        self._label_timer = ValueTimer(0, None)
        self._units_timer = ValueTimer(0, None)
        self._data_timer = ValueTimer(0, None)

        self._entered_event = threading.Event()
        self._entered_lock = threading.Lock()

        dispatcher.send(
            network.SIGNAL_VALUE_ADDED,
            sender=self,
            network=network,
            node=node,
            node_id=node.id,
            value=self,
            value_id=id
        )

    def update_value(self, **kwargs):
        changed_values = self._update(**kwargs)
        self._entered_event.set()

        if changed_values:
            dispatcher.send(
                self._network.SIGNAL_VALUE_CHANGED,
                sender=self,
                network=self._network,
                node=self._node,
                node_id=self._node.id,
                value=self,
                value_id=self.id,
                changed_values=changed_values
            )

    def refresh_value(self, **kwargs):
        refreshed_values = self._update(**kwargs)

        if refreshed_values:
            dispatcher.send(
                self._network.SIGNAL_VALUE_REFRESHED,
                sender=self,
                network=self._network,
                node=self._node,
                node_id=self._node.id,
                value=self,
                value_id=self.id,
                refreshed_values=refreshed_values
            )

    def _update(self, **kwargs):
        """
        value
        homeId
        nodeId
        commandClass
        instance
        index
        id
        genre
        type
        label
        units
        readOnly
        """
        changed_values = []

        if 'value' in kwargs:
            kwargs['data'] = kwargs.pop('value')

        def check(attr_name):
            old = getattr(self, '_' + attr_name)
            new = kwargs[attr_name]
            if old != new:
                changed_values.append(attr_name)
                setattr(self, '_' + attr_name, new)
                timer = getattr(self, '_' + attr_name + '_timer', None)
                if timer is not None:
                    timer.cancel()

        for key in kwargs.keys()[:]:
            check(key)

        return changed_values

    def __str__(self):
        """
        The string representation of the value.

        :rtype: str
        """
        return (
            u'home_id: [%s] id: [%s] parent_id: [%s] label: [%s] data: [%s]' %
            (
                self._network.home_id_str,
                self._object_id,
                self.parent_id,
                self.label,
                self.data
            )
        )

    def _get(self, item):
        return getattr(self._network.manager, item)(self.id)

    @property
    def parent_id(self):
        """
        Get the parent_id of the value.
        """
        return self._node.object_id

    @property
    def id(self):
        """
        Get the value_id of the value.
        """
        return self._id

    @property
    def id_on_network(self):
        """
        Get an unique id for this value.

        The scenes use this to retrieve values

        .. code-block:: xml

                <Scene id="1" label="scene1">
                        <Value homeId="0x014d0ef5" nodeId="2" genre="user"
                        commandClassId="38" instance="1" index="0"
                        type="byte">54</Value>
                </Scene>

        The format is :

            home_id.node_id.command_class.instance.index
        """
        separator = self._network.id_separator
        return "0x{1:08x}{0}{2}{0}0x{3:02x}{0}{4}{0}{5}".format(
            separator,
            self._network.home_id,
            self.parent_id,
            self.command_class,
            self.instance,
            self.index
        )

    @property
    def node(self):
        """
        The value_id of the value.
        """
        return self._node

    @property
    def label(self):
        """
        Get the label of the value.

        :rtype: str
        """
        return str(self._label)
        # return self._get('getValueLabel')

    @label.setter
    def label(self, value):
        """
        Set the label of the value.

        :param value: The new label value
        :type value: str
        """

        self._label_timer.cancel()
        self._label_timer = ValueTimer(
            0.2,
            self._network.manager.setValueLabel
        )
        self._network.manager.setValueLabel(self.id, value)
        self._label_timer(self.id, value)

    @property
    def help(self):
        """
        Gets a help string describing the value's purpose and usage.

        :rtype: str
        """
        return self._get('getValueHelp')

    @help.setter
    def help(self, value):
        """
        Sets a help string describing the value's purpose and usage..

        :param value: The new help value
        :type value: str
        """
        self._network.manager.setValueHelp(self.id, value)

    @property
    def units(self):
        """
        Gets the units that the value is measured in.

        :rtype: str
        """
        return self._units
        # return self._get('getValueUnits')

    @units.setter
    def units(self, value):
        """
        Sets the units that the value is measured in.

        :param value: The new units value
        :type value: str
        """

        self._units_timer.cancel()
        self._units_timer = ValueTimer(
            0.2,
            self._network.manager.setValueUnits
        )
        self._network.manager.setValueUnits(self.id, value)
        self._units_timer(self.id, value)

    @property
    def max(self):
        """
        Gets the maximum that this value may contain.

        :rtype: int
        """
        return self._get('getValueMax')

    @property
    def min(self):
        """
        Gets the minimum that this value may contain.

        :rtype: int
        """
        return self._get('getValueMin')

    @property
    def type(self):
        """
        Get the type of the value.  The type describes the data held by the
        value and enables the user to select the correct value accessor method
        in the Manager class.

        :return: type of the value
        :rtype: str
        """

        data_type = self._type # self._get('getValueType')

        if data_type == "Bool":
            return bool
        elif data_type == "Byte":
            return int
        elif data_type == "Decimal":
            return float
        elif data_type == "Int":
            return int
        elif data_type == "Short":
            return int
        elif data_type == "String":
            return str
        elif data_type == "Button":
            return bool
        elif data_type == "List":
            return list
        else:
            return str

    @property
    def genre(self):
        """
        Get the genre of the value.  The genre classifies a value to enable
        low-level system or configuration parameters to be filtered out
        by the application

        :return: genre of the value (Basic, User, Config, System)
        :rtype: str
        """
        return self._genre
        # return self._get('getValueGenre')

    @property
    def index(self):
        """
        Get the value index.  The index is used to identify one of multiple
        values created and managed by a command class.  In the case of
        configurable parameters (handled by the configuration command class),
        the index is the same as the parameter ID.

        :return: index of the value
        :rtype: int
        """
        return self._index
        # return self._get('getValueIndex')

    @property
    def instance(self):
        """
        Get the command class instance of this value.  It is possible for
        there to be multiple instances of a command class, although currently
        it appears that only the SensorMultilevel command class ever does this.

        :return: instance of the value
        :rtype: int
        """
        return self._instance
        # return self._get('getValueInstance')

    @property
    def data(self):
        """
        Get the current data of the value.

        :return: The data of the value
        :rtype: depending of the type of the value
        """
        return self._data
        # return self._get('getValue')

    @data.setter
    def data(self, value):
        """
        Set the data of the value.

        Best practice: Use check_data before setting it:

        new_val = value.check_data(some_data)
        if new_val != None:
            value.data = new_val

        :param value: The new data value
        :type value:
        """

        self._data_timer.cancel()
        self._data_timer = ValueTimer(
            0.2,
            self._network.manager.setValue
        )
        self._data_timer(self.id, value)
        self._network.manager.setValue(self.id, value)

    def __enter__(self):
        self._entered_lock.acquire()
        self._entered_event.clear()
        return self._entered_event

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._entered_lock.release()

    def __iter__(self):
        if self.type == list:
            for item in self._get('getValueListItems'):
                yield item

    @property
    def data_help(self):
        """
        When type of value is list, data_items contains a list of valid values

        :return: The valid values or a help string
        :rtype: string or set
        """

        data_type = self._get('getValueType')
        if self.is_read_only:
            return "Read only"
        if data_type == "Bool":
            return "True or False"
        elif data_type == "Byte":
            return "A byte between %s and %s" % (self.min, self.max)
        elif data_type == "Decimal":
            return "A float"
        elif data_type == "Int":
            return "An integer between %s and %s" % (self.min, self.max)
        elif data_type == "Short":
            return "A integer between %s and %s" % (self.min, self.max)
        elif data_type == "String":
            return "A string"
        elif data_type == "Button":
            return "True or False"
        elif data_type == "List":
            return "A list"
        else:
            return "Unknown"

    @property
    def is_set(self):
        """
        Test whether the value has been set.

        :return: True if the value has actually been set by a status message
                 from the device, rather than simply being the default.
        :rtype: bool
        """
        return self._get('isValueSet')

    @property
    def is_read_only(self):
        """
        Test whether the value is read-only.

        :return: True if the value cannot be changed by the user.
        :rtype: bool
        """
        return self._readOnly
        # return self._get('isValueReadOnly')

    @property
    def is_write_only(self):
        """
        Test whether the value is write-only.

        :return: True if the value can only be written to and not read.
        :rtype: bool

        """
        return self._get('isValueWriteOnly')

    def enable_poll(self, intensity=1):
        """
        Enable the polling of a device's state.

        :param intensity: The intensity of the poll
        :type intensity: int
        :return: True if polling was enabled.
        :rtype: bool
        """
        self._poll_intensity = intensity
        return self._network.manager.enablePoll(self.id, intensity)

    def disable_poll(self):
        """
        Disable poll off this value.

        :return: True if polling was disabled.
        :rtype: bool
        """
        self._poll_intensity = 0
        return self._get('disablePoll')

    @property
    def poll_intensity(self):
        """
        The poll intensity of the value.

        :returns: 0=none, 1=every time through the list, 2-every other time,
        etc
        :rtype: int

        """
        return self._get('getPollIntensity')

    @property
    def is_polled(self):
        """
        Verify that the value is polled.

        :rtype: bool
        """
        return self._get('isPolled')

    @property
    def command_class(self):
        """
        The command class of the value.

        :returns: The command class of this value
        :rtype: int

        """
        return getattr(zwave_command_classes, self._commandClass)
        # return self._get('getValueCommandClass')

    def refresh(self):
        """
        Refresh the value.

        :returns: True if the command was transmitted to controller
        :rtype: bool
        """
        return self._get('refreshValue')

    @property
    def precision(self):
        """
        Gets a float value's precision.

        :returns: a float value's precision
        :rtype: int
        """
        return self._get('getValueFloatPrecision')

    def is_change_verified(self):
        """
        determine if value changes upon a refresh should be verified.
        If so, the library will immediately refresh the value a second time
        whenever a change is observed. This helps to filter out spurious data
        reported occasionally by some devices.
        """
        return self._get('getChangeVerified')

    def set_change_verified(self, verify):
        """
        Sets a flag indicating whether value changes noted upon a refresh
        should be verified.

        If so, the library will immediately refresh the value a second time
        whenever a change is observed. This helps to filter out spurious data
        reported occasionally by some devices.

        :param verify: if true, verify changes; if false, don't verify changes.
        :type verify: bool
        """
        logger.debug(
            u'Set change verified %s for valueId [%s]',
            verify,
            self.id
        )
        self._network.manager.setChangeVerified(self.id, verify)

    def to_dict(self, *extras):
        """
        Return a dict representation of the node.

        :param extras: The extra inforamtion to add
        :type extras: list
        :returns: A dict
        :rtype: dict
        """
        attrs = []

        if not extras:
            extras = ('all',)

        if 'all' in extras:
            attrs = [
                'data_items',
                'command_class',
                'is_read_only',
                'is_write_only',
                'type',
                'index'
            ]
        ret = dict(
            label=self.label,
            id=self.id,
            node_id=self.node.node_id,
            units=self.units,
            genre=self.genre,
            data=self.data
        )

        ret.update(dict((key, getattr(self, key)) for key in attrs))

        return ret
