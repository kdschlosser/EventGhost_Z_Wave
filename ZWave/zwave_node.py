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
import zwave_command_classes
import zwave_device_classes
from zwave_object import ZWaveObject
from zwave import PyStatNode
from zwave_group import ZWaveGroup
from zwave_value import ValuesContainer

logger = logging.getLogger('openzwave')


# noinspection PyShadowingBuiltins,PyAbstractClass
class ZWaveNode(ZWaveObject):
    """
    Represents a single Node within the Z-Wave Network.
    """

    _isReady = False

    def __init__(self, object_id, network=None, use_cache=False):
        """
        Initialize zwave node

        :param object_id: ID of the node
        :type object_id: int
        :param network: The network object to access the manager
        :type network: ZWaveNetwork
        """
        logger.debug("Create object node (node_id:%s)", object_id)

        if not hasattr(self, '_cls_ids'):
            self._cls_ids = []

        self._values = ValuesContainer()
        self._is_locked = False
        self._isReady = False

        ZWaveObject.__init__(
            self,
            object_id,
            network,
            use_cache
        )

    @property
    def values(self):
        return self._values

    @values.setter
    def values(self, values):
        pass

    def __str__(self):
        """
        The string representation of the node.

        :rtype: str
        """
        try:
            return (
                u'home_id: [%s] id: [%s] name: [%s] model: [%s]' %
                (
                    self._network.home_id_str,
                    self._object_id,
                    self.name,
                    self.product_name
                )
            )
        except UnicodeDecodeError:
            return (
                u'home_id: [%s] id: [%s] name: [%s] model: [%s]' %
                (
                    self._network.home_id_str,
                    self._object_id,
                    self.name.decode('utf-8', 'ignore'),
                    self.product_name.decode('utf-8', 'ignore')
                )
            )

    @property
    def node_id(self):
        """
        The id of the node.

        :rtype: int
        """
        return self._object_id

    def __get(self, method, *args, **kwargs):
        return getattr(self._network.manager, 'get' + method)(
            self.home_id,
            self.object_id,
            *args,
            **kwargs
        )

    def __set(self, method, *args, **kwargs):
        return getattr(self._network.manager, 'set' + method)(
            self.home_id,
            self.object_id,
            *args,
            **kwargs
        )

    @property
    def name(self):
        """
        The name of the node.

        :rtype: str
        """
        return self.__get('NodeName')

    @name.setter
    def name(self, value):
        """
        Set the name of the node.

        :param value: The new name of the node
        :type value: str
        """

        self.__set('NodeName', value)

    @property
    def location(self):
        """
        The location of the node.

        :rtype: str
        """
        return self.__get('NodeLocation')

    @location.setter
    def location(self, value):
        """
        Set the location of the node.

        :param value: The new location of the node
        :type value: str
        """
        self.__set('NodeLocation', value)

    @property
    def product_name(self):
        """
        The product name of the node.

        :rtype: str
        """
        return self.__get('NodeProductName')

    @product_name.setter
    def product_name(self, value):
        """
        Set the product name of the node.

        :param value: The new name of the product
        :type value: str
        """
        self.__set('NodeProductName', value)

    @property
    def product_type(self):
        """
        The product type of the node.

        :rtype: str
        """
        return self.__get('NodeProductType')

    @property
    def product_id(self):
        """
        The product Id of the node.

        :rtype: str
        """
        return self.__get('NodeProductId')

    @property
    def device_type(self):
        """
        The device_type of the node.

        :rtype: str
        """
        return self.__get('NodeDeviceTypeString')

    @property
    def device_type_as_str(self):
        return zwave_device_classes.device_type_to_string(self.device_type)

    @property
    def role(self):
        """
        The role of the node.

        :rtype: str
        """
        return self.__get('NodeRoleString')

    @property
    def role_as_str(self):
        return zwave_device_classes.role_type_to_string(self.role)

    def to_dict(self, *extras):
        """
        Return a dict representation of the node.

        :param extras: The extra information to add
        :type extras: list
        :returns: A dict
        :rtype: dict
        """

        if not extras:
            extras = ('all',)
        if 'all' in extras:
            extras = ('capabilities', 'neighbors', 'groups', 'values')
        ret = dict(
            name=self.name,
            location=self.location,
            product_type=self.product_type,
            product_name=self.product_name,
            node_id=self.node_id
        )
        if 'values' in extras:
            ret['values'] = self.values_to_dict(*extras)
        if 'groups' in extras:
            ret['groups'] = self.groups_to_dict(*extras)
        if 'neighbors' in extras:
            ret['neighbors'] = dict.fromkeys(self.neighbors, 0)
        if 'capabilities' in extras:
            ret['capabilities'] = dict.fromkeys(self.capabilities, 0)
        return ret

    @property
    def capabilities(self):
        """
        The capabilities of the node.

        :rtype: set()
        """
        caps = set()
        if self.is_routing_device:
            caps.add('routing')
        if self.is_listening_device:
            caps.add('listening')
        if self.is_frequent_listening_device:
            caps.add('frequent')
        if self.is_security_device:
            caps.add('security')
        if self.is_beaming_device:
            caps.add('beaming')
        if self.is_zwave_plus:
            caps.add('zwave_plus')
        if self.node_id == self._network.controller.node_id:
            for cap in self._network.controller.capabilities:
                caps.add(cap)
        return caps

    @property
    def neighbors(self):
        """
        The neighbors of the node.

        :rtype: list
        """
        return self.__get('NodeNeighbors')

    @property
    def num_groups(self):
        """
        Gets the number of association groups reported by this node.

        :rtype: int
        """
        return self.__get('NumGroups')

    def get_max_associations(self, group_id):
        """
        Gets the maximum number of associations for a group.

        :param group_id: The group to query
        :type group_id: int
        :rtype: int
        """
        return self.__get('MaxAssociations', group_id)

    @property
    def groups(self):
        """
        Get the association groups reported by this node

        In Z-Wave, groups are numbered starting from one.  For example,
        if a call to GetNumGroups returns 4, the _groupIdx value to use in
        calls to GetAssociations AddAssociation and RemoveAssociation will be
        a number between 1 and 4.

        :rtype: dict
        """
        groups = dict()
        groups_added = 0
        i = 1
        while groups_added < self.num_groups and i < 256:
            if self.get_max_associations(i) > 0:
                groups[i] = ZWaveGroup(
                    i,
                    network=self._network,
                    node_id=self.node_id
                )
                groups_added += 1
            i += 1
        return groups

    def groups_to_dict(self, *extras):
        """
        Return a dict representation of the groups.

        :param extras: The extra information to add
        :type extras: list
        :returns: A dict
        :rtype: dict
        """

        if not extras:
            extras = ('all',)
        groups = self.groups
        ret = {}
        for gid in groups.keys():
            ret[gid] = groups[gid].to_dict(extras=extras)
        return ret

    @property
    def command_classes(self):
        """
        The commandClasses of the node.

        :rtype: set
        """
        command_cls = set()
        for cls in self._network.manager.COMMAND_CLASS_DESC:
            if self.__get('NodeClassInformation', cls):
                command_cls.add(cls)
        return command_cls

    @property
    def command_classes_as_str(self):
        """
        Return the command classes of the node as string.

        :rtype: set
        """
        commands = self.command_classes
        command_str = set()
        for cls in commands:
            command_str.add(self._network.manager.COMMAND_CLASS_DESC[cls])
        return ', '.join(cc for cc in command_str)

    def get_command_class_as_str(self, class_id):
        """
        Return the command class representation as string.

        :param class_id: the COMMAND_CLASS to get string representation
        :type class_id: hexadecimal code
        :rtype: str
        """
        return self._network.manager.COMMAND_CLASS_DESC[class_id]

    # noinspection PyMethodMayBeStatic
    def get_command_class_genres(self):
        """
        Return the list of genres of command classes

        :rtype: list
        """
        return ['User', 'Basic', 'Config', 'System']

    def get_values_by_command_classes(
        self,
        genre='All',
        type='All',
        readonly='All',
        writeonly='All'
    ):
        """
        Retrieve values in a dict() of dicts(). The dict is indexed on the
        COMMAND_CLASS. This allows to browse values grouped by the
        COMMAND_CLASS.You can optionally filter for a command class,
        a genre and/or a type. You can also filter readonly and writeonly
        params.

        This method always filter the values.
        If you wan't to get all the node's values, use the property
        self.values instead.

        :param genre: the genre of value
        :type genre: 'All' or PyGenres
        :param type: the type of value
        :type type: 'All' or PyValueTypes
        :param readonly: Is this value readonly
        :type readonly: 'All' or True or False
        :param writeonly: Is this value readonly
        :type writeonly: 'All' or True or False
        :rtype: dict
        """
        values = dict()
        for value in self.values:
            if (
                genre in ('All', value.genre) and
                type in ('All', value.type) and
                readonly in ('All', value.is_read_only) and
                writeonly in ('All', value.is_write_only)
            ):
                if value.command_class not in values:
                    values[value.command_class] = []

                values[value.command_class] += [value]
        return values

    def get_values_for_command_class(self, class_id):
        """
        Retrieve the set of values for a command class.
        Deprecated
        For backward compatibility only.
        Use get_values instead

        :param class_id: the COMMAND_CLASS to get values
        :type class_id: hexadecimal code or string
        :rtype: set() of classId
        """
        return self.get_values(class_id=class_id)

    def get_values(
        self,
        class_id='All',
        genre='All',
        type='All',
        readonly='All',
        writeonly='All',
        index='All',
        label='All'
    ):
        """
        Retrieve the set of values. You can optionally filter for a command
        class, a genre and/or a type. You can also filter readonly and
        writeonly params.

        This method always filter the values.
        If you wan't to get all the node's values, use self.values instead.

        :param class_id: the COMMAND_CLASS to get values
        :type class_id: hexadecimal code or string
        :param genre: the genre of value
        :type genre: 'All' or PyGenres
        :param type: the type of value
        :type type: 'All' or PyValueTypes
        :param readonly: Is this value readonly
        :type readonly: 'All' or True or False
        :param writeonly: Is this value writeonly
        :type writeonly: 'All' or True or False
        :param index: Index of value within all the values
        :type index: int
        :param label: Label of the value as set by openzwave
        :type label: str
        :rtype: set() of Values
        """
        ret = []
        for value in self.values:
            if (
                class_id in ('All', value.command_class) and
                genre in ('All', value.genre) and
                type in ('All', value.type) and
                readonly in ('All', value.is_read_only) and
                writeonly in ('All', value.is_write_only) and
                index in ('All', value.index) and
                label in ('All', value.label)
            ):
                ret += [value]
        return ret

    def values_to_dict(self, *extras):
        """
        Return a dict representation of the values.

        :param extras: The extra information to add
        :type extras: []
        :returns: A dict
        :rtype: dict()
        """

        if not extras:
            extras = ('all',)

        ret = []
        for value in self.values:
            ret += [value.to_dict(extras=extras)]
        return ret

    def add_value(self, value_id):
        """
        Add a value to the node

        :param value_id: The id of the value to add
        :type value_id: dict
        :rtype: bool
        """
        value_id['node'] = self
        value_id['network'] = self.network

        self._values[value_id] = value_id
        value = self._values[value_id]

        return value

    def change_value(self, value_id):
        """
        Change a value of the node.
        Not implemented

        :param value_id: The id of the value to change
        :type value_id: dict
        """
        if value_id in self.values:
            value = self.values[value_id]
            value.update_value(**value_id)
        else:
            value = self.add_value(value_id)

        return value

    def refresh_value(self, value_id):
        """
        Refresh a value of the node.
        Not implemented

        :param value_id: The id of the value to change
        :type value_id: dict
        """
        if value_id in self.values:
            value = self.values[value_id]
            value.refresh_value(**value_id)
        else:
            value = self.add_value(value_id)

        return value

    def reload_value(self, index):
        """
        Refresh a value of the node.
        Not implemented

        :param index: The id of the value to change
        :type index: int
        """
        if not isinstance(index, int):
            value = index
        else:
            value = self.values[index]

        self.remove_value(value)
        return self._network.manager.refreshValue(value.id)

    def remove_value(self, value_id):
        return self.values.pop(value_id, False)

    def set_field(self, field, value):
        """
        A helper to set a writable field : name, location, product_name, ...

        :param field: The field to set : name, location, product_name,
        manufacturer_name
        :type field: str
        :param value: The value to set
        :type value: str
        :rtype: bool
        """
        if field == "name":
            self.name = value
        elif field == "location":
            self.location = value
        elif field == "product_name":
            self.product_name = value
        elif field == "manufacturer_name":
            self.manufacturer_name = value

    def has_command_class(self, class_id):
        """
        Check that this node use this commandClass.

        :param class_id: the COMMAND_CLASS to check
        :type class_id: hexadecimal code
        :rtype: bool
        """
        return class_id in self.command_classes

    @property
    def manufacturer_id(self):
        """
        The manufacturer id of the node.

        :rtype: str
        """
        return self.__get('NodeManufacturerId')

    @property
    def manufacturer_name(self):
        """
        The manufacturer name of the node.

        :rtype: str
        """
        return self.__get('NodeManufacturerName')

    @manufacturer_name.setter
    def manufacturer_name(self, value):
        """
        Set the manufacturer name of the node.

        :param value: The new manufacturer name of the node
        :type value: str
        """
        self.__set('NodeManufacturerName', value)

    @property
    def generic(self):
        """
        The generic type of the node.

        :rtype: int
        """
        return self.__get('NodeGeneric')

    @property
    def generic_as_str(self):
        return zwave_device_classes.generic_type_to_string(self.generic)

    @property
    def basic(self):
        """
        The basic type of the node.

        :rtype: int
        """
        return self.__get('NodeBasic')

    @property
    def basic_as_str(self):
        return zwave_device_classes.basic_type_to_string(self.basic)

    @property
    def specific(self):
        """
        The specific type of the node.

        :return: The specific type of the node
        :rtype: int
        """
        return self.__get('NodeSpecific')

    @property
    def specific_as_str(self):
        return zwave_device_classes.specific_type_to_string(
            self.generic,
            self.specific
        )

    @property
    def security(self):
        """
        The security type of the node.

        :return: The security type of the node
        :rtype: int
        """
        return self.__get('NodeSecurity')

    @property
    def version(self):
        """
        The version of the node.

        :return: The version of the node
        :rtype: int
        """
        return self.__get('NodeVersion')

    @property
    def is_listening_device(self):
        """
        Is this node a listening device.

        :rtype: bool
        """
        return self._network.manager.isNodeListeningDevice(
            self.home_id,
            self.object_id
        )

    @property
    def is_beaming_device(self):
        """
        Is this node a beaming device.

        :rtype: bool
        """
        return self._network.manager.isNodeBeamingDevice(
            self.home_id,
            self.object_id
        )

    @property
    def is_frequent_listening_device(self):
        """
        Is this node a frequent listening device.

        :rtype: bool
        """
        return self._network.manager.isNodeFrequentListeningDevice(
            self.home_id,
            self.object_id
        )

    @property
    def is_security_device(self):
        """
        Is this node a security device.

        :rtype: bool
        """
        return self._network.manager.isNodeSecurityDevice(
            self.home_id,
            self.object_id
        )

    @property
    def is_routing_device(self):
        """
        Is this node a routing device.

        :rtype: bool
        """
        return self._network.manager.isNodeRoutingDevice(
            self.home_id,
            self.object_id
        )

    @property
    def is_zwave_plus(self):
        """
        Is this node a zwave plus one.

        :rtype: bool
        """
        return self._network.manager.isNodeZWavePlus(
            self.home_id,
            self.object_id
        )

    @property
    def is_locked(self):
        """
        Is this node locked.

        :rtype: bool
        """
        return self._is_locked

    @property
    def is_sleeping(self):
        """
        Is this node sleeping.

        :rtype: bool

        """
        return not self.is_awake

    @property
    def max_baud_rate(self):
        """
        Get the maximum baud rate of a node
        """
        return self.__get('NodeMaxBaudRate')

    def heal(self, update_node_route=False):
        """
        Heal network node by requesting the node rediscover their neighbors.
        Sends a ControllerCommand_RequestNodeNeighborUpdate to the node.

        :param update_node_route: Optional Whether to perform return routes
        initialization. (default = false).
        :type update_node_route: bool
        :return: True is the ControllerCommand is sent. False otherwise
        :rtype: bool
        """
        if self.is_awake is False:
            logger.warning(u'Node state must a minimum set to awake')
            return False
        self._network.manager.healNetworkNode(
            self.home_id,
            self.object_id,
            update_node_route
        )
        return True

    def test(self, count=1):
        """
        Send a number of test messages to node and record results.

        :param count: The number of test messages to send.
        :type count: int
        """
        self._network.manager.testNetworkNode(
            self.home_id,
            self.object_id,
            count
        )

    def assign_return_route(self):
        """
        Ask the to update its update its Return Route to the Controller

        This command will ask a Node to update its Return Route to the
        Controller

        Results of the AssignReturnRoute Command will be send as a
        Notification with the Notification type as
        Notification::Type_ControllerCommand

        :return: True if the request was sent successfully.
        :rtype: bool
        """
        logger.debug('assign_return_route for node [%s]', self.object_id)
        return self._network.controller.assign_return_route(self.object_id)

    def refresh_info(self):
        """
        Trigger the fetching of fixed data about a node.

        Causes the nodes data to be obtained from the Z-Wave network in the
        same way as if it had just been added.  This method would normally be
        called automatically by OpenZWave, but if you know that a node has
        been changed, calling this method will force a refresh of the data
        held by the library.  This can be especially useful for devices that
        were asleep when the application was first run.

        :rtype: bool
        """
        logger.debug(u'refresh_info for node [%s]', self.object_id)
        return self._network.manager.refreshNodeInfo(
            self.home_id,
            self.object_id
        )

    def request_state(self):
        """
        Trigger the fetching of just the dynamic value data for a node.
        Causes the node's values to be requested from the Z-Wave network.
        This is the same as the query state starting from the dynamic state.

        :rtype: bool
        """
        logger.debug(u'request_state for node [%s]', self.object_id)
        return self._network.manager.requestNodeState(
            self.home_id,
            self.object_id
        )

    def send_information(self):
        """
        Send a NIF frame from the Controller to a Node.
        This command send a NIF frame from the Controller to a Node

        Results of the SendNodeInformation Command will be send as a
        Notification with the Notification type as
        Notification::Type_ControllerCommand

        :return: True if the request was sent successfully.
        :rtype: bool
        """
        logger.debug(u'send_information for node [%s]', self.object_id)
        return self._network.controller.send_node_information(self.object_id)

    def network_update(self):
        """
        Update the controller with network information from the SUC/SIS.

        Results of the RequestNetworkUpdate Command will be send as a
        Notification with the Notification type as
        Notification::Type_ControllerCommand

        :return: True if the request was sent successfully.
        :rtype: bool
        """
        logger.debug(u'network_update for node [%s]', self.object_id)
        return self._network.controller.request_network_update(self.object_id)

    def neighbor_update(self):
        """
        Ask a Node to update its Neighbor Tables

        This command will ask a Node to update its Neighbor Tables.

        Results of the RequestNodeNeighborUpdate Command will be send as a
        Notification with the Notification type as
        Notification::Type_ControllerCommand

        :return: True if the request was sent successfully.
        :rtype: bool
        """
        logger.debug(u'neighbor_update for node [%s]', self.object_id)
        return self._network.controller.request_node_neighbor_update(
            self.object_id
        )

    def create_button(self, button_id):
        """
        Create a handheld button id.

        Only intended for Bridge Firmware Controllers.

        Results of the CreateButton Command will be send as a
        Notification with the Notification type as
        Notification::Type_ControllerCommand

        :param button_id: the ID of the Button to query.
        :type button_id: int
        :return: True if the request was sent successfully.
        :rtype: bool
        """
        logger.debug(u'create_button for node [%s]', self.object_id)
        return self._network.controller.create_button(
            self.object_id,
            button_id
        )

    def delete_button(self, button_id):
        """
        Delete a handheld button id.

        Only intended for Bridge Firmware Controllers.

        Results of the CreateButton Command will be send as a
        Notification with the Notification type as
        Notification::Type_ControllerCommand

        :param button_id: the ID of the Button to query.
        :type button_id: int
        :return: True if the request was sent successfully.
        :rtype: bool
        """
        logger.debug(u'delete_button for node [%s]', self.object_id)
        return self._network.controller.delete_button(
            self.object_id,
            button_id
        )

    def request_all_config_params(self):
        """
        Request the values of all known configurable parameters from a device.

        """
        logger.debug(u'Requesting config params for node [%s]', self.object_id)
        self._network.manager.requestAllConfigParams(
            self.home_id,
            self.object_id
        )

    def request_config_param(self, param):
        """
        Request the value of a configurable parameter from a device.

        Some devices have various parameters that can be configured to
        control the device behaviour.  These are not reported by the device
        over the Z-Wave network but can usually be found in the devices user
        manual.  This method requests the value of a parameter from the
        device, and then returns immediately, without waiting for a response.
        If the parameter index is valid for this device, and the device is
        awake, the value will eventually be reported via a ValueChanged
        notification callback.  The ValueID reported in the callback will have
        an index set the same as _param and a command class set to the same
        value as returned by a call to Configuration::StaticGetCommandClassId.

        :param param: The param of the node.
        :type param:
        """
        logger.debug(
            u'Requesting config param %s for node [%s]',
            param,
            self.object_id
        )
        self._network.manager.requestConfigParam(
            self.home_id,
            self.object_id,
            param
        )

    def set_config_param(self, param, value, size=2):
        """
        Set the value of a configurable parameter in a device.

        Some devices have various parameters that can be configured to
        control the device behaviour.  These are not reported by the device
        over the Z-Wave network but can usually be found in the devices user
        manual.  This method returns immediately, without waiting for
        confirmation from the device that the change has been made.

        :param param: The param of the node.
        :type param:
        :param value: The value of the param.
        :type value:
        :param size: Is an optional number of bytes to be sent for the
        parameter value. Defaults to 2.
        :type size: int
        :return:
        :rtype: bool
        """
        logger.debug(
            u'Set config param %s for node [%s]',
            param,
            self.object_id
        )
        return self.__set('ConfigParam', param, value, size)

    @property
    def is_awake(self):
        """
        Is this node a awake.

        :rtype: bool
        """

        return self._network.manager.isNodeAwake(self.home_id, self.object_id)

    @property
    def is_failed(self):
        """
        Is this node is presume failed.

        :rtype: bool
        """

        return self._network.manager.isNodeFailed(self.home_id, self.object_id)

    @property
    def query_stage(self):
        """
        Is this node a awake.

        :rtype: string
        """
        return self.__get('NodeQueryStage')

    @property
    def is_ready(self):
        """
        Get whether the node is ready to operate (QueryStage Completed).

        :rtype: bool
        """
        return self._isReady

    @is_ready.setter
    def is_ready(self, value):
        """
        Set whether the node is ready to operate.
        automatically set to True by notification SIGNAL_NODE_QUERIES_COMPLETE

        :param value: is node ready
        :type value: bool

        """
        self._isReady = value

    @property
    def is_info_received(self):
        """
        Get whether the node information has been received. Returns True if
        the node information has been received yet

        :rtype: bool
        """
        return self._network.manager.isNodeInfoReceived(
            self.home_id,
            self.object_id
        )

    @property
    def type(self):
        """
        Get a human-readable label describing the node
        :rtype: str
        """
        return self.__get('NodeType')

    @property
    def type_as_str(self):
        return zwave_device_classes.node_type_to_string(self.type)

    @property
    def stats(self):
        """
        Retrieve statistics for node.

        Statistics:

            * sentCnt:

                Number of messages sent from this node.

            * sentFailed:

                Number of sent messages failed

            * retries:

                Number of message retries

            * receivedCnt:

                Number of messages received from this node.

            * receivedDups:

                Number of duplicated messages received.

            * receivedUnsolicited:

                Number of messages received unsolicited.

            * lastRequestRTT:

                Last message request RTT.

            * lastResponseRTT:

                Last message response RTT.

            * sentTS:

                Last message sent time.

            * receivedTS:

                Last message received time.

            * averageRequestRTT:

                Average Request round trip time.

            * averageResponseRTT:

                Average Response round trip time.

            * quality:

                Node quality measure.

            * lastReceivedMessage[254]:

                Place to hold last received message.

            * errors:

                Count errors for dead node detection.

        :return: Statistics of the node
        :rtype: dict()
        """
        return self.__get('NodeStatistics')

    # noinspection PyMethodMayBeStatic
    def get_stats_label(self, stat):
        """
        Retrieve label of the statistic for node.

        :param stat: The code of the stat label to retrieve.
        :type stat:
        :return: The label or the stat.
        :rtype: str
        """
        return PyStatNode[stat]

    @property
    def id(self):
        return self.node_id

    @property
    def properties(self):
        return self.values.values()


class ZWaveNodeInterfaceMeta(type):
    instances = {}

    def __call__(cls, object_id, network=None, use_cache=True):

        if (object_id, network) not in ZWaveNodeInterfaceMeta.instances:

            bases = (ZWaveNode,)

            for command_cls in network.manager.COMMAND_CLASS_DESC:
                if network.manager.getNodeClassInformation(
                    network.home_id,
                    object_id,
                    command_cls
                ):
                    # noinspection PyUnresolvedReferences
                    command_cls = zwave_command_classes[command_cls]
                    if command_cls not in bases:
                        bases += (command_cls,)

            # noinspection PyShadowingBuiltins
            def __init__(self, id, net, cache):
                ZWaveNode.__init__(
                    self,
                    id,
                    net,
                    cache
                )

                for cmd_cls in self.__bases__[1:]:
                    cmd_cls.__init__(self)
            node = type(
                'ZWaveNode',
                bases,
                {"__init__": __init__, '__bases__': bases}
            )
            ZWaveNodeInterfaceMeta.instances[(object_id, network)] = (
                node(object_id, network, use_cache)
            )

        return ZWaveNodeInterfaceMeta.instances[(object_id, network)]


class ZWaveNodeInterface(object):
    __metaclass__ = ZWaveNodeInterfaceMeta

    def __init__(self, *args, **kwargs):
        pass

    def __getattr__(self, item):
        if item in self.__dict__:
            return self.__dict__[item]

        raise AttributeError(item)
