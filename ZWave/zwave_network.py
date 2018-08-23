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
import dispatcher
import sys
import traceback
import threading
import zwave
import zwave_command_classes
from zwave_object import ZWaveObject
from zwave_controller import ZWaveController
from zwave_node import ZWaveNodeInterface
from zwave_option import ZWaveOption
from zwave_scene import ZWaveScene

logger = logging.getLogger('openzwave')


# noinspection PyPep8Naming,PyAbstractClass
class ZWaveNetwork(ZWaveObject):
    """
    The network object = home_id.
    It contains a reference to the manager and the controller.

    It dispatches the following louie signals :

        * SIGNAL_NETWORK_FAILED = 'NetworkFailed'
        * SIGNAL_NETWORK_START = 'NetworkStarted'
        * SIGNAL_NETWORK_READY = 'NetworkReady'
        * SIGNAL_NETWORK_STOP = 'NetworkStopped'
        * SIGNAL_NETWORK_RESET = 'DriverReset'
        * SIGNAL_NETWORK_AWAKE = 'DriverAwake'
        * SIGNAL_DRIVER_FAILED = 'DriverFailed'
        * SIGNAL_DRIVER_READY = 'DriverReady'
        * SIGNAL_DRIVER_RESET = 'DriverReset'
        * SIGNAL_DRIVER_REMOVED = 'DriverRemoved'
        * SIGNAL_NODE_ADDED = 'NodeAdded'
        * SIGNAL_NODE_EVENT = 'NodeEvent'
        * SIGNAL_NODE_NAMING = 'NodeNaming'
        * SIGNAL_NODE_NEW = 'NodeNew'
        * SIGNAL_NODE_PROTOCOL_INFO = 'NodeProtocolInfo'
        * SIGNAL_NODE_READY = 'NodeReady'
        * SIGNAL_NODE_REMOVED = 'NodeRemoved'
        * SIGNAL_SCENE_EVENT = 'SceneEvent'
        * SIGNAL_VALUE_ADDED = 'ValueAdded'
        * SIGNAL_VALUE_CHANGED = 'ValueChanged'
        * SIGNAL_VALUE_REFRESHED = 'ValueRefreshed'
        * SIGNAL_VALUE_REMOVED = 'ValueRemoved'
        * SIGNAL_POLLING_ENABLED = 'PollingEnabled'
        * SIGNAL_POLLING_DISABLED = 'PollingDisabled'
        * SIGNAL_CREATE_BUTTON = 'CreateButton'
        * SIGNAL_DELETE_BUTTON = 'DeleteButton'
        * SIGNAL_BUTTON_ON = 'ButtonOn'
        * SIGNAL_BUTTON_OFF = 'ButtonOff'
        * SIGNAL_ESSENTIAL_NODE_QUERIES_COMPLETE =
        'EssentialNodeQueriesComplete'
        * SIGNAL_NODE_QUERIES_COMPLETE = 'NodeQueriesComplete'
        * SIGNAL_AWAKE_NODES_QUERIED = 'AwakeNodesQueried'
        * SIGNAL_ALL_NODES_QUERIED = 'AllNodesQueried'
        * SIGNAL_ALL_NODES_QUERIED_SOME_DEAD = 'AllNodesQueriedSomeDead'
        * SIGNAL_MSG_COMPLETE = 'MsgComplete'
        * SIGNAL_ERROR = 'Error'
        * SIGNAL_NOTIFICATION = 'Notification'
        * SIGNAL_CONTROLLER_COMMAND = 'ControllerCommand'
        * SIGNAL_CONTROLLER_WAITING = 'ControllerWaiting'

    The table presented below sets notifications in the order they might
    typically be received, and grouped into a few logically related
    categories.  Of course, given the variety of ZWave controllers, devices
    and network configurations the actual sequence will vary (somewhat). The
    descriptions below the notification name (in square brackets) identify
    whether the notification is always sent (unless there’s a significant
    error in the network or software) or potentially sent during the execution
    sequence.

    Driver Initialization Notification

    The notification below is sent when OpenZWave has successfully connected
    to a physical ZWave controller.

    * DriverReady

    [always sent]   Sent when the driver (representing a connection between
    OpenZWave and a Z-Wave controller attached to the specified serial
    (or HID) port) has been initialized. At the time this notification is
    sent, only certain information about the controller itself is known:

        * Controller Z-Wave version
        * Network HomeID
        * Controller capabilities
        * Controller Application Version & Manufacturer/Product ID
        * Nodes included in the network

    * DriverRemoved

    [always sent (either due to Error or by request)] The Driver is being
    removed. Do Not Call Any Driver Related Methods after receiving this

    Node Initialization Notifications

    As OpenZWave starts, it identifies and reads information about each node
    in the network. The following notifications may be sent during the
    initialization process.

    * NodeNew

    [potentially sent]  Sent when a new node has been identified as part of the
    Z-Wave network. It is not sent if the node was identified in a prior
    execution of the OpenZWave library    and stored in the zwcfg*.xml file.
    At the time this notification is sent, very little is known about the node
    itself... only that it is new to OpenZWave. This message is sent once for
    each new node identified.

    * NodeAdded

    [always sent (for each node associated with the controller)]
    Sent when a node has been added to OpenZWave’s set of nodes.  It can be
    triggered either as the zwcfg*.xml file is being read, when a new node
    is found on startup (see NodeNew notification above), or if a new node
    is included in the network while OpenZWave is running.
    As with NodeNew, very little is known about the node at the time the
    notification is sent…just the fact that a new node has been identified
    and its assigned NodeID.

    * NodeProtocolInfo

    [potentially sent]  Sent after a node’s protocol information has been
    successfully read from the controller.
    At the time this notification is sent, only certain information about the
    node is known:

        * Whether it is a “listening” or “sleeping” device
        * Whether the node is capable of routing messages
        * Maximum baud rate for communication
        * Version number
        * Security byte

    NodeNaming

    [potentially sent]  Sent when a node’s name has been set or changed
    (although it may be “set” to “” or NULL).

    * ValueAdded

    [potentially sent]  Sent when a new value has been associated with the
    node.
    At the time this notification is sent, the new value may or may not
    have “live” data associated with it. It may be populated, but it may
    alternatively just be a placeholder for a value that has not been read
    at the time the notification is sent.

    * NodeQueriesComplete

    [always sent (for each node associated with the controller that has been
    successfully queried)]
    Sent when a node’s values and attributes have been fully queried. At the
    time this notification is sent, the node’s information has been fully
    read at least once.  So this notification might trigger “full” display
    of the node’s information, values, etc. If this notification is not sent,
    it indicates that there has been a problem initializing the device.
    The most common issue is that the node is a “sleeping” device.  The
    NodeQueriesComplete notification will be sent when the node wakes up and
    the query process completes.

    Initialization Complete Notifications

    As indicated above, when OpenZWave starts it reads certain information
    from a file, from the controller and from the network.  The following
    notifications identify when this initialization/querying process is
    complete.

    * AwakeNodesQueried

    [always sent]   Sent when all “listening” -always-on-devices have been
    queried successfully.  It also indicates, by implication, that there
    are some “sleeping” nodes that will not complete their queries until
    they wake up. This notification should be sent relatively quickly
    after start-up. (Of course, it depends on the number of devices on
    the ZWave network and whether there are any messages that “time out”
    without a proper response.)

    * AllNodesQueried

    [potentially sent]  Sent when all nodes have been successfully queried.

    This notification should be sent relatively quickly if there are
    no “sleeping” nodes. But it might be sent quite a while after start-up
    if there are sleeping nodes and at least one of these nodes has a long
    “wake-up” interval.

    Other Notifications

    In addition to the notifications described above, which are primarily
    “initialization” notifications that are sent during program start-up,
    the following notifications may be sent as a result of user actions,
    external program control, etc.

    * ValueChanged : Sent when a value associated with a node has changed.
    Receipt of this notification indicates that it may be a good time to read
    the new value and display or otherwise process it accordingly.
    * ValueRemoved : Sent when a value associated with a node has been removed.
    * Group : Sent when a node’s group association has changed.
    * NodeRemoved : Sent when a node has been removed from the ZWave network.
    * NodeEvent : Sent when a node sends a Basic_Set command to the
    controller. This notification can be generated by certain sensors,
    for example, motion detectors, to indicate that an event has been sensed.
    * PollingEnabled : Sent when node/value polling has been enabled.
    * PollingDisabled : Sent when node/value polling has been disabled.
    * DriverReset : Sent to indicate when a controller has been reset.
    This notification is intended to replace the potentially hundreds of
    notifications representing each value and node removed from the network.

    About the use of louie signals :
    For network, python-openzwave send the following louie signal :

        SIGNAL_NETWORK_FAILED : the driver has failed to start.
        SIGNAL_NETWORK_START : the driver is ready, but network is not
        available.
        SIGNAL_NETWORK_AWAKE : all awake nodes are queried. Some sleeping
        nodes may be missing.
        SIGNAL_NETWORK_READY : all nodes are queried. Network is fully
        functional.
        SIGNAL_NETWORK_RESET : the network has been reset. It will start
        again.
        SIGNAL_NETWORK_STOP : the network has been stopped.

    Deprecated : SIGNAL_DRIVER_* shouldn't be used anymore.

    """

    SIGNAL_NETWORK_FAILED = 'NetworkFailed'
    SIGNAL_NETWORK_START = 'NetworkStart'
    SIGNAL_NETWORK_READY = 'NetworkReady'
    SIGNAL_NETWORK_STOP = 'NetworkStop'
    SIGNAL_NETWORK_RESET = 'DriverReset'
    SIGNAL_NETWORK_AWAKE = 'DriverAwake'
    SIGNAL_DRIVER_FAILED = 'DriverFailed'
    SIGNAL_DRIVER_READY = 'DriverReady'
    SIGNAL_DRIVER_RESET = 'DriverReset'
    SIGNAL_DRIVER_REMOVED = 'DriverRemoved'
    SIGNAL_GROUP = 'Group'
    SIGNAL_NODE = 'Node'
    SIGNAL_NODE_ADDED = 'NodeAdded'
    SIGNAL_NODE_EVENT = 'NodeEvent'
    SIGNAL_NODE_NAMING = 'NodeNaming'
    SIGNAL_NODE_NEW = 'NodeNew'
    SIGNAL_NODE_PROTOCOL_INFO = 'NodeProtocolInfo'
    SIGNAL_NODE_READY = 'NodeReady'
    SIGNAL_NODE_REMOVED = 'NodeRemoved'
    SIGNAL_SCENE_EVENT = 'SceneEvent'
    SIGNAL_VALUE = 'Value'
    SIGNAL_VALUE_ADDED = 'ValueAdded'
    SIGNAL_VALUE_CHANGED = 'ValueChanged'
    SIGNAL_VALUE_REFRESHED = 'ValueRefreshed'
    SIGNAL_VALUE_REMOVED = 'ValueRemoved'
    SIGNAL_POLLING_ENABLED = 'PollingEnabled'
    SIGNAL_POLLING_DISABLED = 'PollingDisabled'
    SIGNAL_CREATE_BUTTON = 'CreateButton'
    SIGNAL_DELETE_BUTTON = 'DeleteButton'
    SIGNAL_BUTTON_ON = 'ButtonOn'
    SIGNAL_BUTTON_OFF = 'ButtonOff'
    SIGNAL_ESSENTIAL_NODE_QUERIES_COMPLETE = 'EssentialNodeQueriesComplete'
    SIGNAL_NODE_QUERIES_COMPLETE = 'NodeQueriesComplete'
    SIGNAL_AWAKE_NODES_QUERIED = 'AwakeNodesQueried'
    SIGNAL_ALL_NODES_QUERIED = 'AllNodesQueried'
    SIGNAL_ALL_NODES_QUERIED_SOME_DEAD = 'AllNodesQueriedSomeDead'
    SIGNAL_MSG_COMPLETE = 'MsgComplete'
    SIGNAL_NOTIFICATION = 'Notification'
    SIGNAL_CONTROLLER_COMMAND = 'ControllerCommand'
    SIGNAL_CONTROLLER_WAITING = 'ControllerWaiting'
    SIGNAL_CONTROLLER_STATS = 'ControllerStats'

    STATE_STOP = 0
    STATE_FAILED = 1
    STATE_RESET = 3
    STATE_STARTED = 5
    STATE_AWAKE = 7
    STATE_READY = 10

    ignoreSubsequent = True
    zwave_command_classes = zwave_command_classes

    def __init__(self, name, options, log=None, auto_start=True):
        """
        Initialize zwave network

        :param options: Options to use with manager
        :type options: ZWaveOption
        :param log: A log file (not used. Deprecated
        :type log:
        :param auto_start: should we start the network.
        :type auto_start: bool
        """

        logger.debug("Creating network object.")
        self._object_id = None
        self.name = name
        self.log = log
        self._started = False
        self._options = options
        self._nodes = dict()
        ZWaveObject.__init__(self, None, self)
        self._controller = ZWaveController(1, self, options)
        logger.debug("Creating network manager object.")
        import time
        time.sleep(0.1)
        self._manager = libopenzwave.PyManager()
        logger.debug("Starting network manager.")
        time.sleep(0.1)

        self._manager.create()

        logger.debug("Network manager object created.")
        time.sleep(0.1)
        self._state = self.STATE_STOP
        self._semaphore_nodes = threading.Semaphore()
        self._id_separator = '.'
        self.network_event = threading.Event()

        self._started = False
        if auto_start:
            self.start()

        logger.debug("Network object created.")

    def __str__(self):
        """
        The string representation of the node.

        :rtype: str
        """
        return (
            u'home_id: [%s] controller: [%s]' %
            (self.home_id_str, self.controller)
        )

    def start(self):
        """
        Start the network object :
            - add a watcher
            - add a driver
        """
        if self._started:
            return
        logger.info(u"Start Openzwave network.")
        self._manager.addWatcher(self.zwcallback)
        self._manager.addDriver(self._options.device)
        self._started = True

    # noinspection PyBroadException,PyPep8
    def stop(self, fire=True):
        """
        Stop the network object.

            - remove the watcher
            - remove the driver
            - clear the nodes
        """
        if not self._started:
            return

        logger.info(u"Stop Openzwave network.")
        if self.controller is not None:
            self.controller.stop()
        self.write_config()
        try:
            self._semaphore_nodes.acquire()
            self._manager.removeWatcher(self.zwcallback)
            try:
                self.network_event.wait(1.0)
            except AssertionError:
                # For gevent AssertionError:
                # Impossible to call blocking function
                # in the event loop callback
                pass
            self._manager.removeDriver(self._options.device)
            try:
                self.network_event.wait(1.0)
            except AssertionError:
                # For gevent AssertionError:
                # Impossible to call blocking function in
                # the event loop callback
                pass
            for i in range(0, 60):
                if self.controller.send_queue_count <= 0:
                    break
                else:
                    try:
                        self.network_event.wait(1.0)
                    except AssertionError:
                        # For gevent AssertionError:
                        # Impossible to call blocking function in the
                        # event loop callback
                        pass
            self.nodes = None
        except:
            logger.exception(u'Stop network : %s')
        finally:
            self._semaphore_nodes.release()
        self._started = False
        self._state = self.STATE_STOP
        try:
            self.network_event.wait(1.0)
        except AssertionError:
            # For gevent AssertionError:
            # Impossible to call blocking function in the event loop callback
            pass
        if fire:
            dispatcher.send(
                self.SIGNAL_NETWORK_STOP,
                sender=self,
                network=self
            )

    def destroy(self):
        """
        Destroy the network and all related stuff.
        """
        self._manager.destroy()
        self._options.destroy()
        self._manager = None
        self._options = None

    @property
    def home_id(self):
        """
        The home_id of the network.

        :rtype: int
        """
        if self._object_id is None:
            return 0
        return self._object_id

    @home_id.setter
    def home_id(self, value):
        """
        The home_id of the network.

        :param value: new home_id
        :type value: int
        """
        if isinstance(value, (str, unicode)):
            value = int(value, 16)

        self._object_id = value

    @property
    def home_id_str(self):
        return '0x' + hex(self.home_id)[2:].upper()

    @property
    def id(self):
        return self.home_id

    @property
    def is_ready(self):
        """
        Says if the network is ready for operations.

        :rtype: bool
        """
        return self._state >= self.STATE_READY

    @property
    def state(self):
        """
        The state of the network. Values may be changed in the future,
        only order is important.
        You can safely ask node information when state >= STATE_READY

        * STATE_STOP = 0
        * STATE_FAILED = 1
        * STATE_RESET = 3
        * STATE_START = 5
        * STATE_AWAKE = 7
        * STATE_READY = 10

        :rtype: int
        """
        return self._state

    @state.setter
    def state(self, value):
        """
        The state of the network. Values may be changed in the future,
        only order is important.

        * STATE_STOP = 0
        * STATE_FAILED = 1
        * STATE_RESET = 3
        * STATE_START = 5
        * STATE_AWAKE = 7
        * STATE_READY = 10

        :param value: new state
        :type value: int
        """
        self._state = value

    @property
    def state_str(self):
        """
        The state of the network. Values may be changed in the future,
        only order is important.
        You can safely ask node information when state >= STATE_AWAKE

        :rtype: int
        """
        if self._state == self.STATE_STOP:
            return "Network is stopped"
        elif self._state == self.STATE_FAILED:
            return "Driver failed"
        elif self._state == self.STATE_STARTED:
            return "Driver initialised"
        elif self._state == self.STATE_RESET:
            return "Driver is reset"
        elif self._state == self.STATE_AWAKE:
            return "Topology loaded"
        elif self._state == self.STATE_READY:
            return "Network ready"
        else:
            return "Unknown state"

    @property
    def manager(self):
        """
        The manager to use to communicate with the lib c++.

        :rtype: ZWaveManager
        """
        return self._manager

    @property
    def controller(self):
        """
        The controller of the network.

        :return: The controller of the network
        :rtype: ZWaveController
        """
        return self._controller

    @property
    def nodes(self):
        """
        The nodes of the network.

        :rtype: dict
        """
        return self._nodes

    def nodes_to_dict(self, *extras):
        """
        Return a dict representation of the network.

        :param extras: The extra information to add
        :type extras: list
        :returns: A dict
        :rtype: dict
        """
        if not extras:
            extras = ('all',)

        return dict(
            (node.node_id, node.to_dict(*extras))
            for node in self._nodes.values()
        )

    def to_dict(self, *_):
        """
        Return a dict representation of the network.

        :returns: A dict
        :rtype: dict
        """
        ret = dict(
            state=self.state,
            state_str=self.state_str,
            home_id=self.home_id_str,
            nodes_count=self.nodes_count,
        )

        return ret

    @nodes.setter
    def nodes(self, value):
        """
        The nodes of the network.

        :param value: The new value
        :type value: dict
        """
        if not isinstance(value, dict):
            value = dict()

        self._nodes = value

    def switch_all(self, state):
        """
        Method for switching all devices on or off together.  The devices must
        support the SwitchAll command class.  The command is first broadcast
        to all nodes, and then followed up with individual commands to each
        node (because broadcasts are not routed, the message might not
        otherwise reach all the nodes).

        :param state: True to turn on the switches, False to turn them off
        :type state: bool
        """
        if state:
            self.manager.switchAllOn(self.home_id)
        else:
            self.manager.switchAllOff(self.home_id)

    def test(self, count=1):
        """
        Send a number of test messages to every node and record results.

        :param count: The number of test messages to send.
        :type count: int
        """
        self.manager.testNetwork(self.home_id, count)

    def heal(self, update_node_route=False):
        """
        Heal network by requesting nodes rediscover their neighbors.
        Sends a ControllerCommand_RequestNodeNeighborUpdate to every node.
        Can take a while on larger networks.

        :param update_node_route: Optional Whether to perform return routes
        initialization. (default = false).
        :type update_node_route: bool
        :return: True is the ControllerCommand ins sent. False otherwise
        :rtype: bool
        """
        if self.network.state < self.network.STATE_AWAKE:
            logger.warning(u'Network must be awake')
            return False
        self.manager.healNetwork(self.home_id, update_node_route)
        return True

    def get_value(self, value_id):
        """
        Retrieve a value on the network.

        Check every nodes to see if it holds the value

        :param value_id: The id of the value to find
        :type value_id: int
        :return: The value or None
        :rtype: ZWaveValue
        """
        for node in self._nodes.values():
            if value_id in node.values:
                return node.values[value_id]
        return None

    @property
    def id_separator(self):
        """
        The separator in id representation.

        :rtype: char
        """
        return self._id_separator

    @id_separator.setter
    def id_separator(self, value):
        """
        The nodes of the network.

        :param value: The new separator
        :type value: char
        """
        self._id_separator = value

    def get_value_from_id_on_network(self, id_on_network):
        """
        Retrieve a value on the network from it's id_on_network.

        Check every nodes to see if it holds the value

        :param id_on_network: The id_on_network of the value to find
        :type id_on_network: str
        :return: The value or None
        :rtype: ZWaveValue
        """
        for node in self._nodes.itervalues():
            for val in node.values.itervalues():
                if val.id_on_network == id_on_network:
                    return val
        return None

    @property
    def scenes(self):
        """
        The scenes of the network.

        Scenes are generated directly from the lib. There is no notification
        support to keep them up to date. So for a batch job, consider
        storing them in a local variable.

        :return: return a dict() (that can be empty) of scene object. Return
        None if betwork is not ready
        :rtype: dict or None
        """
        if self.state < self.STATE_AWAKE:
            return None
        else:
            return self._load_scenes()

    def scenes_to_dict(self, *extras):
        """
        Return a JSONifiable dict representation of the scenes.

        :param extras: The extra information to add
        :type extras: list
        :returns: A dict
        :rtype: dict
        """
        if not extras:
            extras = ('all',)

        return dict(
            (scene.scene_id, scene.to_dict(*extras))
            for scene in self.scenes
        )

    def _load_scenes(self):
        """
        Load the scenes of the network.

        :return: return a dict() (that can be empty) of scene object.
        :rtype: dict()
        """
        set_scenes = self._manager.getAllScenes()
        logger.debug(u'Load Scenes: %s', set_scenes)
        return dict(
            (scene_id, ZWaveScene(scene_id, network=self))
            for scene_id in set_scenes
        )

    def create_scene(self, label=None):
        """
        Create a new scene on the network.
        If label is set, also change the label of the scene

        If you store your scenes on a local variable, get a new one
        to get the scene id

        :param label: The new label
        :type label: str or None
        :return: return the id of scene on the network. Return 0 if fails
        :rtype: int
        """
        scene = ZWaveScene(None, network=self)
        return scene.create(label)

    def scene_exists(self, scene_id):
        """
        Check that the scene exists

        :param scene_id: The id of the scene to check
        :type scene_id: int
        :return: True if the scene exist. False in other cases
        :rtype: bool
        """
        return self._network.manager.sceneExists(scene_id)

    @property
    def scenes_count(self):
        """
        Return the number of scenes

        :return: The number of scenes
        :rtype: int
        """
        return self._network.manager.getNumScenes()

    def remove_scene(self, scene_id):
        """
        Delete the scene on the network.

        :param scene_id: The id of the scene to check
        :type scene_id: int
        :return: True if the scene was removed. False in other cases
        :rtype: bool
        """
        return self._network.manager.removeScene(scene_id)

    @property
    def nodes_count(self):
        """
        The nodes count of the network.

        :rtype: int
        """
        return len(self._nodes)

    @property
    def sleeping_nodes_count(self):
        """
        The count of sleeping nodes on the network.

        :rtype: int
        """
        return len(
            list(node for node in self._nodes.values() if node.is_sleeping)
        )

    def get_poll_interval(self):
        """
        Get the time period between polls of a nodes state

        :return: The number of milliseconds between polls
        :rtype: int
        """
        return self.manager.getPollInterval()

    def set_poll_interval(self, milliseconds=500, interval_between_polls=True):
        """
        Set the time period between polls of a nodes state.

        Due to patent concerns, some devices do not report state changes
        automatically to the controller.  These devices need to have their
        state polled at regular intervals.  The length of the interval is the
        same for all devices.  To even out the Z-Wave network traffic
        generated by polling, OpenZWave divides the polling interval by the
        number of devices that have polling enabled, and polls each in turn.
        It is recommended that if possible, the interval should not be set
        shorter than the number of polled devices in seconds (so that the
        network does not have to cope with more than one poll per second).

        :param milliseconds: The length of the polling interval in
        milliseconds.
        :type milliseconds: int
        :param interval_between_polls: If set to true (via SetPollInterval),
        the pollInterval will be interspersed between each poll
        (so a much smaller m_pollInterval like 100, 500, or 1,000 may be
        appropriate). If false, the library attempts to complete all polls
        within m_pollInterval.
        :type interval_between_polls: bool
        """
        self.manager.setPollInterval(milliseconds, interval_between_polls)

    # noinspection PyPep8,PyBroadException
    def zwcallback(self, kwargs):
        """
        The Callback Handler used with the libopenzwave.

        n['valueId'] = {

            * 'home_id' : v.GetHomeId(),
            * 'node_id' : v.GetNodeId(),
            * 'commandClass' :
            PyManager.COMMAND_CLASS_DESC[v.GetCommandClassId()],
            * 'instance' : v.GetInstance(),
            * 'index' : v.GetIndex(),
            * 'id' : v.GetId(),
            * 'genre' : PyGenres[v.GetGenre()],
            * 'type' : PyValueTypes[v.GetType()],
            * #'value' : value.c_str(),
            * 'value' : getValueFromType(manager,v.GetId()),
            * 'label' : label.c_str(),
            * 'units' : units.c_str(),
            * 'readOnly': manager.IsValueReadOnly(v)
        """
        logger.debug('zwcallback kwargs=%s', kwargs)
        try:
            notify_type = kwargs.pop('notificationType')
            if 'homeId' in kwargs:
                home_id = kwargs['homeId']
                home_id = '0x' + hex(home_id)[2:].upper().replace('L', '')
                kwargs['homeId'] = home_id
            if notify_type == self.SIGNAL_DRIVER_FAILED:
                self._handle_driver_failed(**kwargs)
            elif notify_type == self.SIGNAL_DRIVER_READY:
                self._handle_driver_ready(**kwargs)
            elif notify_type == self.SIGNAL_DRIVER_RESET:
                self._handle_driver_reset(**kwargs)
            elif notify_type == self.SIGNAL_NODE_ADDED:
                self._handle_node_added(**kwargs)
            elif notify_type == self.SIGNAL_NODE_EVENT:
                self._handle_node_event(**kwargs)
            elif notify_type == self.SIGNAL_NODE_NAMING:
                self._handle_node_naming(**kwargs)
            elif notify_type == self.SIGNAL_NODE_NEW:
                self._handle_node_new(**kwargs)
            elif notify_type == self.SIGNAL_NODE_PROTOCOL_INFO:
                self._handle_node_protocol_info(**kwargs)
            elif notify_type == self.SIGNAL_NODE_READY:
                self._handleNodeReady(**kwargs)
            elif notify_type == self.SIGNAL_NODE_REMOVED:
                self._handle_node_removed(**kwargs)
            elif notify_type == self.SIGNAL_GROUP:
                self._handle_group(**kwargs)
            elif notify_type == self.SIGNAL_SCENE_EVENT:
                self._handle_scene_event(**kwargs)
            elif notify_type == self.SIGNAL_VALUE_ADDED:
                self._handle_value_added(**kwargs)
            elif notify_type == self.SIGNAL_VALUE_CHANGED:
                self._handle_value_changed(**kwargs)
            elif notify_type == self.SIGNAL_VALUE_REFRESHED:
                self._handle_value_refreshed(**kwargs)
            elif notify_type == self.SIGNAL_VALUE_REMOVED:
                self._handle_value_removed(**kwargs)
            elif notify_type == self.SIGNAL_POLLING_DISABLED:
                self._handle_polling_disabled(**kwargs)
            elif notify_type == self.SIGNAL_POLLING_ENABLED:
                self._handle_polling_enabled(**kwargs)
            elif notify_type == self.SIGNAL_CREATE_BUTTON:
                self._handle_create_button(**kwargs)
            elif notify_type == self.SIGNAL_DELETE_BUTTON:
                self._handle_delete_button(**kwargs)
            elif notify_type == self.SIGNAL_BUTTON_ON:
                self._handle_button_on(**kwargs)
            elif notify_type == self.SIGNAL_BUTTON_OFF:
                self._handle_button_off(**kwargs)
            elif notify_type == self.SIGNAL_ALL_NODES_QUERIED:
                self._handle_all_nodes_queried(**kwargs)
            elif notify_type == self.SIGNAL_ALL_NODES_QUERIED_SOME_DEAD:
                self._handle_all_nodes_queried_some_dead(**kwargs)
            elif notify_type == self.SIGNAL_AWAKE_NODES_QUERIED:
                self._handle_awake_nodes_queried(**kwargs)
            elif notify_type == self.SIGNAL_ESSENTIAL_NODE_QUERIES_COMPLETE:
                self._handle_essential_node_queries_complete(**kwargs)
            elif notify_type == self.SIGNAL_NODE_QUERIES_COMPLETE:
                self._handle_node_queries_complete(**kwargs)
            elif notify_type == self.SIGNAL_MSG_COMPLETE:
                self._handle_msg_complete(**kwargs)
            elif notify_type == self.SIGNAL_NOTIFICATION:
                self._handle_notification(**kwargs)
            elif notify_type == self.SIGNAL_DRIVER_REMOVED:
                self._handle_driver_removed(**kwargs)
            elif notify_type == self.SIGNAL_CONTROLLER_COMMAND:
                self._handle_controller_command(**kwargs)
            else:
                logger.warning(u'Skipping unhandled notification %s', kwargs)
        except:
            logger.exception(
                u'Error in manager callback %s : %s',
                kwargs,
                traceback.format_exc()
            )

    def _handle_driver_failed(self, **kwargs):
        """
        Driver failed to load.
        """
        logger.warning(u'Z-Wave Notification DriverFailed : %s', kwargs)
        self._manager = None
        self._controller = None
        self.nodes = None
        self._state = self.STATE_FAILED
        dispatcher.send(
            self.SIGNAL_NETWORK_FAILED,
            sender=self,
            network=self,
            **kwargs
        )

    # noinspection PyPep8,PyBroadException
    def _handle_driver_ready(self, homeId=None, nodeId=None, **kwargs):
        """
        A driver for a PC Z-Wave controller has been added and is ready to use.
        The notification will contain the controller's Home ID,
        which is needed to call most of the Manager methods.
        """
        logger.debug(
            u'Z-Wave Notification DriverReady : %s: %s: %s',
            homeId,
            nodeId,
            kwargs
        )
        self._object_id = int(homeId, 16)
        try:
            controller_node = ZWaveNodeInterface(
                nodeId,
                network=self
            )
            self._semaphore_nodes.acquire()
            self.nodes = None
            # self._nodes[nodeId] = controller_node
            self._controller.node = controller_node
            if not controller_node.name.strip():
                controller_node.name = str(
                    controller_node.manufacturer_name +
                    ' ' +
                    controller_node.product_name
                )
            if not controller_node.location.strip():
                controller_node.location = str('Z-Wave Network Controller')

            logger.info(
                u'Driver ready using library %s',
                self._controller.library_description
            )
            logger.info(
                u'home_id 0x%0.8x, controller node id is %d',
                self.home_id,
                self._controller.node_id
            )
            logger.debug(u'Network %s', self)
            # Not needed. Already sent by the lib
            # ~ dispatcher.send(self.SIGNAL_DRIVER_READY, \
            # ~ **{'network': self, 'controller': self._controller})
            self._state = self.STATE_STARTED
            dispatcher.send(
                self.SIGNAL_NETWORK_START,
                sender=self,
                network=self,
                controller=controller_node.name,
            )
        except:
            logger.exception('Z-Wave Notification DriverReady',)
        finally:
            self._semaphore_nodes.release()

    def _handle_driver_reset(self, **kwargs):
        """
        This notification is never fired.

        Look at
            and

        All nodes and values for this driver have been removed.
        This is sent instead of potentially hundreds of individual node
        and value notifications.
        """
        logger.debug(u'Z-Wave Notification DriverReset : %s', kwargs)
        with self._semaphore_nodes:
            logger.debug(u'DriverReset received. Remove all nodes')
            self.nodes = None
            self._state = self.STATE_RESET
            dispatcher.send(
                self.SIGNAL_NETWORK_RESET,
                sender=self,
                network=self,
                **kwargs
            )

    def _handle_driver_removed(self, **kwargs):
        """
        The Driver is being removed. (either due to Error or by request)
        Do Not Call Any Driver Related Methods after receiving this
        """
        logger.debug(u'Z-Wave Notification DriverRemoved : %s', kwargs)
        with self._semaphore_nodes:
            self._state = self.STATE_STOP
            dispatcher.send(
                self.SIGNAL_DRIVER_REMOVED,
                sender=self,
                network=self,
                **kwargs
            )

    def _handle_group(self, nodeId=None, groupIdx=None, **kwargs):
        """
        The associations for the node have changed.
        The application should rebuild any group information
        it holds about the node.
        """
        logger.debug(
            u'Z-Wave Notification Group : %s: %s: %s',
            nodeId,
            groupIdx,
            kwargs
        )
        node = self._nodes[nodeId]
        dispatcher.send(
            self.SIGNAL_GROUP,
            sender=self,
            network=self,
            node=node,
            node_id=nodeId,
            group_id=groupIdx,
            **kwargs
        )

    def _handle_node(self, node):
        """
        Sent when a node is changed, added, removed, ...
        If you don't interest in nodes event details you can listen to this
        signal only.
        """
        logger.debug(u'Z-Wave Notification Node : %s', node)
        dispatcher.send(
            self.SIGNAL_NODE,
            sender=self,
            network=self,
            node=node,
            node_id=node.id
        )

    def _handleNodeReady(self, nodeId=None, **kwargs):
        logger.debug(
            u'Z-Wave Notification NodeReady : %s: %s',
            nodeId,
            kwargs
        )

        if nodeId == self._controller.node.id:
            node = self._controller.node
        else:
            node = self._nodes[nodeId]

        dispatcher.send(
            self.SIGNAL_NODE_READY,
            sender=self,
            network=self,
            node=node,
            node_id=nodeId,
            **kwargs
        )
        self._handle_node(node)

    def _handle_node_added(self, nodeId=None, **kwargs):
        """
        A new node has been added to OpenZWave's set.
        This may be due to a device being added to the Z-Wave network,
        or because the application is initializing itself.
        """

        logger.debug(
            u'Z-Wave Notification NodeAdded : %s: %s',
            nodeId,
            kwargs
        )
        node = ZWaveNodeInterface(nodeId, network=self)

        if not node.location:
            node.location = str('No Room')

        name = node.name

        if not name.strip() or name == 'New Node':
            name = node.manufacturer_name + ' ' + node.product_name

            if not name.strip():
                name = 'New Node'

            node.name = str(name)

        if nodeId != self._controller.node.id:
            with self._semaphore_nodes:
                self._nodes[nodeId] = node

        dispatcher.send(
            self.SIGNAL_NODE_ADDED,
            sender=self,
            network=self,
            node=node,
            node_id=nodeId,
            **kwargs
        )
        self._handle_node(node)

    def _handle_scene_event(self, nodeId=None, sceneId=None, **kwargs):
        """
        Scene Activation Set received

        Not implemented
        """
        logger.debug(
            u'Z-Wave Notification SceneEvent : %s: %s: %s',
            nodeId,
            sceneId,
            kwargs
        )

        if nodeId == self._controller.node.id:
            node = self._controller.node
        else:
            node = self._nodes[nodeId]
        dispatcher.send(
            self.SIGNAL_SCENE_EVENT,
            sender=self,
            network=self,
            node=node,
            node_id=nodeId,
            scene_id=sceneId,
            **kwargs
        )

    def _handle_node_event(self, nodeId=None, event=None, **kwargs):
        """
        A node has triggered an event.  This is commonly caused when a
        node sends a Basic_Set command to the controller.
        The event value is stored in the notification.
        """
        logger.debug(
            u'Z-Wave Notification NodeEvent : %s: %s: %s',
            nodeId,
            event,
            kwargs
        )

        if nodeId == self._controller.node.id:
            node = self._controller.node
        else:
            node = self._nodes[nodeId]

        dispatcher.send(
            self.SIGNAL_NODE_EVENT,
            sender=self,
            network=self,
            node=node,
            node_id=nodeId,
            event=event,
            **kwargs
        )

    def _handle_node_naming(self, nodeId=None, **kwargs):
        """
        One of the node names has changed (name, manufacturer, product).
        """
        logger.debug(
            u'Z-Wave Notification NodeNaming : %s: %s',
            nodeId,
            kwargs
        )

        if nodeId == self._controller.node.id:
            node = self._controller.node
        else:
            node = self._nodes[nodeId]

        dispatcher.send(
            self.SIGNAL_NODE_NAMING,
            sender=self,
            network=self,
            node=node,
            node_id=nodeId,
            **kwargs
        )
        self._handle_node(node)

    def _handle_node_new(self, nodeId=None, **kwargs):
        """
        A new node has been found (not already stored in zwcfg*.xml file).
        """
        logger.debug(
            u'Z-Wave Notification NodeNew : %s: %s',
            nodeId,
            kwargs
        )

        dispatcher.send(
            self.SIGNAL_NODE_NEW,
            sender=self,
            network=self,
            node_id=nodeId,
            **kwargs
        )

    def _handle_node_protocol_info(self, nodeId=None, **kwargs):
        """
        Basic node information has been received, such as whether
        the node is a listening device, a routing device and its baud rate
        and basic, generic and specific types.
        It is after this notification that you can call Manager::GetNodeType
        to obtain a label containing the device description.
        """
        logger.debug(
            u'Z-Wave Notification NodeProtocolInfo : %s: %s',
            nodeId,
            kwargs
        )

        if nodeId == self._controller.node.id:
            node = self._controller.node
        else:
            node = self._nodes[nodeId]
        dispatcher.send(
            self.SIGNAL_NODE_PROTOCOL_INFO,
            sender=self,
            network=self,
            node=node,
            node_id=nodeId,
            **kwargs
        )
        self._handle_node(node)

    def _handle_node_removed(self, nodeId=None, **kwargs):
        """
        A node has been removed from OpenZWave's set.
        This may be due to a device being removed from the Z-Wave network,
        or because the application is closing.
        """
        logger.debug(
            u'Z-Wave Notification NodeRemoved : %s: %s',
            nodeId,
            kwargs
        )

        if nodeId == self._controller.node.id:
            node = self._controller.node
        elif nodeId in self._nodes:
            node = self._nodes[nodeId]
            with self._semaphore_nodes:
                del self._nodes[nodeId]
        else:
            node = None

        dispatcher.send(
            self.SIGNAL_NODE_REMOVED,
            sender=self,
            network=self,
            node=node,
            node_id=nodeId,
            **kwargs
        )

        if node is not None:
            self._handle_node(node)

    def _handle_essential_node_queries_complete(self, nodeId=None, **kwargs):
        """
        The queries on a node that are essential to its operation have
        been completed. The node can now handle incoming messages.
        """
        logger.debug(
            u'Z-Wave Notification EssentialNodeQueriesComplete : %s: %s',
            nodeId,
            kwargs
        )

        if nodeId == self._controller.node.id:
            node = self._controller.node
        else:
            node = self._nodes[nodeId]
        dispatcher.send(
            self.SIGNAL_ESSENTIAL_NODE_QUERIES_COMPLETE,
            sender=self,
            network=self,
            node=node,
            node_id=nodeId,
            **kwargs
        )

    def _handle_node_queries_complete(self, nodeId=None, **kwargs):
        """
        All the initialisation queries on a node have been completed.

        When receiving this value, we consider that the node is ready.
        """
        logger.debug(
            u'Z-Wave Notification NodeQueriesComplete : %s: %s',
            nodeId,
            kwargs
        )

        if nodeId == self._controller.node.id:
            node = self._controller.node
        else:
            node = self._nodes[nodeId]
        node.is_ready = True

        dispatcher.send(
            self.SIGNAL_NODE_QUERIES_COMPLETE,
            sender=self,
            network=self,
            node=node,
            node_id=nodeId,
            **kwargs
        )
        self._handle_node(node)

    def _handle_all_nodes_queried(self, **kwargs):
        """
        All nodes have been queried, so client application can expected
        complete data.
        """
        logger.debug(u'Z-Wave Notification AllNodesQueried : %s', kwargs)
        self._state = self.STATE_READY
        dispatcher.send(
            self.SIGNAL_NETWORK_READY,
            sender=self,
            network=self,
            **kwargs
        )
        dispatcher.send(
            self.SIGNAL_ALL_NODES_QUERIED,
            sender=self,
            network=self,
            **kwargs
        )

    def _handle_all_nodes_queried_some_dead(self, **kwargs):
        """
        All nodes have been queried, but some node ar mark dead, so client
        application can expected complete data.
        """
        logger.debug(
            u'Z-Wave Notification AllNodesQueriedSomeDead : %s',
            kwargs
        )
        self._state = self.STATE_READY
        dispatcher.send(
            self.SIGNAL_NETWORK_READY,
            sender=self,
            network=self,
            **kwargs
        )
        dispatcher.send(
            self.SIGNAL_ALL_NODES_QUERIED_SOME_DEAD,
            sender=self,
            network=self,
            **kwargs
        )

    # noinspection PyPep8,PyBroadException
    def _handle_awake_nodes_queried(self, homeId=None, **kwargs):
        """
        All awake nodes have been queried, so client application can
        expected complete data for these nodes.
        """
        logger.debug(
            u'Z-Wave Notification AwakeNodesQueried : %s: %s',
            homeId,
            kwargs
        )
        self._object_id = int(homeId, 16)
        try:
            if self._state < self.STATE_AWAKE:
                self._state = self.STATE_AWAKE
            dispatcher.send(
                self.SIGNAL_NETWORK_AWAKE,
                sender=self,
                network=self,
                **kwargs
            )
            dispatcher.send(
                self.SIGNAL_AWAKE_NODES_QUERIED,
                sender=self,
                network=self,
                **kwargs
            )
        except:
            logger.error(
                'Z-Wave Notification AwakeNodesQueried : %s',
                traceback.format_exception(*sys.exc_info())
            )

    def _handle_polling_disabled(self, nodeId=None, **kwargs):
        """
        Polling of a node has been successfully turned off by a call
        to Manager::DisablePoll.
        """
        logger.debug(
            u'Z-Wave Notification PollingDisabled : %s: %s',
            nodeId,
            kwargs
        )

        if nodeId == self._controller.node.id:
            node = self._controller.node
        else:
            node = self._nodes[nodeId]
        dispatcher.send(
            self.SIGNAL_POLLING_DISABLED,
            sender=self,
            network=self,
            node=node,
            node_id=nodeId,
            **kwargs
        )

    def _handle_polling_enabled(self, nodeId=None, **kwargs):
        """
        Polling of a node has been successfully turned on by a call
        to Manager::EnablePoll.
        """
        logger.debug(
            u'Z-Wave Notification PollingEnabled : %s: %s',
            nodeId,
            kwargs
        )

        if nodeId == self._controller.node.id:
            node = self._controller.node
        else:
            node = self._nodes[nodeId]
        dispatcher.send(
            self.SIGNAL_POLLING_ENABLED,
            sender=self,
            network=self,
            node=node,
            node_id=nodeId,
            **kwargs
        )

    def _handle_create_button(self, nodeId=None, **kwargs):
        """
        Handheld controller button event created.
        """
        logger.debug(
            u'Z-Wave Notification CreateButton : %s: %s',
            nodeId,
            kwargs
        )

        if nodeId == self._controller.node.id:
            node = self._controller.node
        else:
            node = self._nodes[nodeId]
        dispatcher.send(
            self.SIGNAL_CREATE_BUTTON,
            sender=self,
            network=self,
            node=node,
            node_id=nodeId,
            **kwargs
        )

    def _handle_delete_button(self, nodeId=None, **kwargs):
        """
        Handheld controller button event deleted.
        """
        logger.debug(
            u'Z-Wave Notification DeleteButton : %s: %s',
            nodeId,
            kwargs
        )

        if nodeId == self._controller.node.id:
            node = self._controller.node
        else:
            node = self._nodes[nodeId]
        dispatcher.send(
            self.SIGNAL_DELETE_BUTTON,
            sender=self,
            network=self,
            node=node,
            node_id=nodeId,
            **kwargs
        )

    def _handle_button_on(self, nodeId=None, **kwargs):
        """
        Handheld controller button on pressed event.
        """
        logger.debug(u'Z-Wave Notification ButtonOn : %s: %s', nodeId, kwargs)

        if nodeId == self._controller.node.id:
            node = self._controller.node
        else:
            node = self._nodes[nodeId]
        dispatcher.send(
            self.SIGNAL_BUTTON_ON,
            sender=self,
            network=self,
            node=node,
            node_id=nodeId,
            **kwargs
        )

    def _handle_button_off(self, nodeId=None, **kwargs):
        """
        Handheld controller button off pressed event.
        """

        if nodeId == self._controller.node.id:
            node = self._controller.node
        else:
            node = self._nodes[nodeId]
        logger.debug(u'Z-Wave Notification ButtonOff : %s: %s', nodeId, kwargs)
        dispatcher.send(
            self.SIGNAL_BUTTON_OFF,
            sender=self,
            network=self,
            node=node,
            node_id=nodeId,
            **kwargs
        )

    def _handle_value(self, node=None, value=None):
        """
        Sent when a value is changed, added, removed, ...
        If you don't interest in values event details you can listen to this
        signal only.
        """
        dispatcher.send(
            self.SIGNAL_VALUE,
            sender=self,
            network=self,
            node=node,
            node_id=node.id,
            value=value,
            value_id=value.id,
        )

    def _handle_value_added(self, nodeId=None, valueId=None, **kwargs):
        """
        A new node value has been added to OpenZWave's set.
        These notifications occur after a node has been discovered,
        and details of its command classes have been received.
        Each command class may generate one or more values depending
        on the complexity of the item being represented.
        """
        logger.debug(
            u'Z-Wave Notification ValueAdded : %s: %s: %s',
            nodeId,
            valueId,
            kwargs
        )

        if nodeId == self._controller.node.id:
            node = self._controller.node
        else:
            node = self._nodes[nodeId]
        value = node.add_value(valueId)
        self._handle_value(node=node, value=value)

    def _handle_value_changed(self, nodeId=None, valueId=None, **kwargs):
        """
        A node value has been updated from the Z-Wave network and it is
        different from the previous value.
        """
        logger.debug(
            u'Z-Wave Notification ValueChanged : %s: %s: %s',
            nodeId,
            valueId,
            kwargs
        )

        if nodeId == self._controller.node.id:
            node = self._controller.node
        elif nodeId in self._nodes:
            node = self._nodes[nodeId]
        else:
            logger.warning(
                'Z-Wave Notification ValueChanged (%s) for an unknown node %s',
                valueId,
                nodeId
            )
            return False

        if valueId is not None:
            value = node.change_value(valueId)
            self._handle_value(node=node, value=value)

    def _handle_value_refreshed(self, nodeId=None, valueId=None, **kwargs):
        """
        A node value has been updated from the Z-Wave network.
        """
        logger.debug(
            u'Z-Wave Notification ValueRefreshed : %s: %s: %s',
            nodeId,
            valueId,
            kwargs
        )

        if nodeId == self._controller.node.id:
            node = self._controller.node
        elif nodeId in self._nodes:
            node = self._nodes[nodeId]
        else:
            logger.warning(
                'Z-Wave Notification ValueRefreshed (%s)'
                ' for an unknown node %s',
                valueId,
                nodeId
            )
            return False

        value = node.refresh_value(valueId)
        self._handle_value(node=node, value=value)

    def _handle_value_removed(self, nodeId=None, valueId=None, **kwargs):
        """
        A node value has been removed from OpenZWave's set.
        This only occurs when a node is removed.
        """

        logger.debug(
            u'Z-Wave Notification ValueRemoved : %s: %s: %s',
            nodeId,
            valueId,
            kwargs
        )
        valueId.update(kwargs)

        if nodeId == self._controller.node.id:
            node = self._controller.node
        elif nodeId in self._nodes:
            node = self._nodes[nodeId]
        else:
            logger.warning(
                u'Z-Wave Notification ValueRemoved (%s) '
                u'for an unknown node %s',
                valueId,
                nodeId
            )
            dispatcher.send(
                self.SIGNAL_VALUE_REMOVED,
                sender=self,
                network=self,
                node=None,
                node_id=nodeId,
                **valueId
            )

            return False

        if valueId['id'] not in node.values:
            logger.warning(
                u'Z-Wave Notification ValueRemoved for '
                u'an unknown value (%s) on node %s',
                valueId,
                nodeId
            )
            dispatcher.send(
                self.SIGNAL_VALUE_REMOVED,
                sender=self,
                network=self,
                node=node,
                node_id=nodeId,
                **valueId
            )

            return False

        value = node.values[valueId['id']]
        if node.remove_value(value):
            dispatcher.send(
                self.SIGNAL_VALUE_REMOVED,
                sender=self,
                network=self,
                node=node,
                node_id=nodeId,
                **valueId
            )

            # self._handle_value(node=self._nodes[args['nodeId']], value=val)

        return True

    def _handle_notification(self, **kwargs):
        """
        Called when an error happened, or node changed
        (awake, sleep, death, no operation, timeout).
        """
        logger.debug(u'Z-Wave Notification : %s', kwargs)
        dispatcher.send(
            self.SIGNAL_NOTIFICATION,
            sender=self,
            network=self,
            **kwargs
        )

    # noinspection PyProtectedMember
    def _handle_controller_command(self, **kwargs):
        """
        Called when a message from controller is sent.
        """
        self._controller._handle_controller_command(**kwargs)

    def _handle_msg_complete(self, **kwargs):
        """
        The last message that was sent is now complete.
        """
        logger.debug(u'Z-Wave Notification MsgComplete : %s', kwargs)
        dispatcher.send(
            self.SIGNAL_MSG_COMPLETE,
            sender=self,
            network=self,
            **kwargs
        )

    def write_config(self):
        """
        The last message that was sent is now complete.
        """
        self._manager.writeConfig(self.home_id)
        logger.info(u'ZWave configuration written to user directory.')

    @property
    def switches(self):
        return []

    @property
    def dimmers(self):
        return []

    @property
    def door_locks(self):
        return []

    @property
    def alarm_sensors(self):
        return []


# initialization callback sequence:
#
# [driverReady]
#
# [nodeAdded] <-------------------------+ This cycle is extremely quick,
# well under one second.
#     [nodeProtocolInfo]                |
#     [nodeNaming]                      |
#     [valueAdded] <---------------+    |
#                                  |    |
#     {REPEATS FOR EACH VALUE} ----+    |
#                                       |
#     [group] <--------------------+    |
#                                  |    |
#     {REPEATS FOR EACH GROUP} ----+    |
#                                       |
# {REPEATS FOR EACH NODE} --------------+
#
# [? (no notification)] <---------------+ (no notification announces the
# beginning of this cycle)
#                                       |
#     [valueChanged] <-------------+    | This cycle can take some time,
# especially if some nodes
#                                  |    | are sleeping or slow to respond.
#     {REPEATS FOR EACH VALUE} ----+    |
#                                       |
#     [group] <--------------------+    |
#                                  |    |
#     {REPEATS FOR EACH GROUP} ----+    |
#                                       |
# [nodeQueriesComplete]                 |
#                                       |
# {REPEATS FOR EACH NODE} --------------+
#
# [awakeNodesQueried] or [allNodesQueried] (with node_id 255)
#
# [driverRemoved]
