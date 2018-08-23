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
from zwave_object import ZWaveObject

logger = logging.getLogger('openzwave')


# noinspection PyAbstractClass
class ZWaveScene(ZWaveObject):
    """
    Represents a single scene within the Z-Wave Network
    """

    def __init__(self, scene_id, network=None):
        """
        Initialize zwave scene

        :param scene_id: ID of the scene
        :type scene_id: int, None
        :param network: The network object to access the manager
        :type network: ZWaveNetwork
        """
        ZWaveObject.__init__(self, scene_id, network)
        logger.debug(u"Create object scene (scene_id:%s)", scene_id)
        self.values = dict()

    def __str__(self):
        """
        The string representation of the scene.

        :rtype: str
        """
        return u'scene_id: [%s] label: [%s]' % (self.scene_id, self.label)

    @property
    def scene_id(self):
        """
        The id of the scene.

        :rtype: int
        """
        return self._object_id

    @property
    def label(self):
        """
        The label of the scene.

        :rtype: str
        """
        return self._network.manager.getSceneLabel(self.object_id)

    @label.setter
    def label(self, value):
        """
        Set the label of the scene.

        :param value: The new label of the scene
        :type value: str
        """
        self._network.manager.setSceneLabel(self.object_id, value)

    def create(self, label=None):
        """
        Create a new zwave scene on the network and update the object_id field
        If label is set, also change the label of the scene

        :param label: The new label
        :type label: str or None
        :returns: return the id of scene on the network. Return 0 if fails
        :rtype: int
        """
        scene_id = self._network.manager.createScene()
        if scene_id != 0:
            self._object_id = scene_id
            if label is not None:
                self.label = label
        return scene_id

    def add_value(self, value_id, value_data):
        """
        Add a value with data value_data to the zwave scene.

        :param value_id: The id of the value to add
        :type value_id: int
        :param value_data: The data of the value to add
        :type value_data: variable
        """
        ret = self._network.manager.addSceneValue(
            self.scene_id,
            value_id,
            value_data
        )
        return ret == 1

    def set_value(self, value_id, value_data):
        """
        Set a value data to value_data in the zwave scene.

        :param value_id: The id of the value to add
        :type value_id: int
        :param value_data: The data of the value to add
        :type value_data: variable
        """
        ret = self._network.manager.setSceneValue(
            self.scene_id,
            value_id,
            value_data
        )
        return ret == 1

    def get_values(self):
        """
        Get all the values of the scene

        :returns: A dict of values
        :rtype: dict()
        """
        ret = dict()
        values = self._network.manager.sceneGetValues(self.scene_id)
        if values is None:
            return ret
        for val in values:
            value = self._network.get_value(val)
            ret[val] = dict(
                value=value,
                data=values[val]
            )
        return ret

    def get_values_by_node(self):
        """
        Get all the values of the scene grouped by nodes

        :returns: A dict of values
        :rtype: dict()
        """
        ret = dict()
        values = self._network.manager.sceneGetValues(self.scene_id)
        if values is None:
            return ret
        for val in values:
            value = self._network.get_value(val)
            if value is not None:
                if value.node.node_id not in ret:
                    ret[value.node.node_id] = {}
                ret[value.node.node_id][val] = {
                    'value': value,
                    'data': values[val]
                }
        return ret

    def remove_value(self, value_id):
        """
        Remove a value from the scene.

        :param value_id: The id of the value to change
        :type value_id: int
        :returns: True if the scene is removed. False otherwise.
        :rtype: bool
        """
        return self._network.manager.removeSceneValue(self.scene_id, value_id)

    def activate(self):
        """
        Activate the zwave scene.

        :returns: True if the scene is activated. False otherwise.
        :rtype: bool
        """
        return self._network.manager.activateScene(self.object_id)

    def to_dict(self, *_):
        """
        Return a dict representation of the node.

        :returns: A dict
        :rtype: dict()
        """
        ret = dict(
            label=self.label,
            scene_id=self.scene_id
        )
        return ret
