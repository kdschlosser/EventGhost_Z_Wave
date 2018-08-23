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

try:  # Python 2.7+
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        """NullHandler logger for python 2.6"""

        def emit(self, record):
            pass
logger = logging.getLogger('openzwave')
logger.addHandler(NullHandler())


import os # NOQA
import requests # NOQA
import zipfile # NOQA
import tempfile # NOQA
import threading # NOQA
import shutil # NOQA
import time # NOQA
import dispatcher # NOQA
from zwave_object import ZWaveObject # NOQA
from zwave import PyStatDriver, PyControllerState # NOQA


# noinspection PyAbstractClass
class ZWaveController(ZWaveObject):
    """
    The controller manager.

    Allows to retrieve information about the library, statistics, ...
    Also used to send commands to the controller

    Commands :

        - Driver::ControllerCommand_AddController :
        Add a new secondary controller to the Z-Wave network.
        - Driver::ControllerCommand_AddDevice :
        Add a new device (but not a controller) to the Z-Wave network.
        - Driver::ControllerCommand_CreateNewPrimary :
        (Not yet implemented)
        - Driver::ControllerCommand_ReceiveConfiguration :
        - Driver::ControllerCommand_RemoveController :
        remove a controller from the Z-Wave network.
        - Driver::ControllerCommand_RemoveDevice :
        remove a device (but not a controller) from the Z-Wave network.
        - Driver::ControllerCommand_RemoveFailedNode :
        move a node to the controller's list of failed nodes.  The node must
        actually have failed or have been disabled since the command will fail
        if it responds.  A node must be in the controller's failed nodes list
        or ControllerCommand_ReplaceFailedNode to work.
        - Driver::ControllerCommand_HasNodeFailed :
        Check whether a node is in the controller's failed nodes list.
        - Driver::ControllerCommand_ReplaceFailedNode :
        replace a failed device with another. If the node is not in the
        controller's failed nodes list, or the node responds, this command
        will fail.
        - Driver:: ControllerCommand_TransferPrimaryRole :
        (Not yet implemented) - Add a new controller to the network and make
        it the primary.  The existing primary will become a secondary
        controller.
        - Driver::ControllerCommand_RequestNetworkUpdate :
        Update the controller with network information from the SUC/SIS.
        - Driver::ControllerCommand_RequestNodeNeighborUpdate :
        Get a node to rebuild its neighbour list.  This method also does
        ControllerCommand_RequestNodeNeighbors afterwards.
        - Driver::ControllerCommand_AssignReturnRoute :
        Assign a network return route to a device.
        - Driver::ControllerCommand_DeleteAllReturnRoutes :
        Delete all network return routes from a device.
        - Driver::ControllerCommand_CreateButton :
        Create a handheld button id.
        - Driver::ControllerCommand_DeleteButton :
        Delete a handheld button id.

    Callbacks :

        - Driver::ControllerState_Waiting :
        The controller is waiting for a user action.  A notice should be
        displayed to the user at this point, telling them what to do next.
        For the add, remove, replace and transfer primary role commands, the
        user needs to be told to press the inclusion button on the device that
        is going to be added or removed.  For
        ControllerCommand_ReceiveConfiguration, they must set their other
        controller to send its data, and for
        ControllerCommand_CreateNewPrimary, set the other controller to learn
        new data.
        - Driver::ControllerState_InProgress :
        the controller is in the process of adding or removing the chosen
        node.  It is now too late to cancel the command.
        - Driver::ControllerState_Complete :
        the controller has finished adding or removing the node, and the
        command is complete.
        - Driver::ControllerState_Failed :
        will be sent if the command fails for any reason.

    """
    # @deprecated
    SIGNAL_CTRL_NORMAL = 'Normal'
    # @deprecated
    SIGNAL_CTRL_STARTING = 'Starting'
    # @deprecated
    SIGNAL_CTRL_CANCEL = 'Cancel'
    # @deprecated
    SIGNAL_CTRL_ERROR = 'Error'
    # @deprecated
    SIGNAL_CTRL_WAITING = 'Waiting'
    # @deprecated
    SIGNAL_CTRL_SLEEPING = 'Sleeping'
    # @deprecated
    SIGNAL_CTRL_INPROGRESS = 'InProgress'
    # @deprecated
    SIGNAL_CTRL_COMPLETED = 'Completed'
    # @deprecated
    SIGNAL_CTRL_FAILED = 'Failed'
    # @deprecated
    SIGNAL_CTRL_NODEOK = 'NodeOK'
    # @deprecated
    SIGNAL_CTRL_NODEFAILED = 'NodeFailed'

    STATE_NORMAL = 'Normal'
    STATE_STARTING = 'Starting'
    STATE_CANCEL = 'Cancel'
    STATE_ERROR = 'Error'
    STATE_WAITING = 'Waiting'
    STATE_SLEEPING = 'Sleeping'
    STATE_INPROGRESS = 'InProgress'
    STATE_COMPLETED = 'Completed'
    STATE_FAILED = 'Failed'
    STATE_NODEOK = 'NodeOK'
    STATE_NODEFAILED = 'NodeFailed'

    INT_NORMAL = 0
    INT_STARTING = 1
    INT_CANCEL = 2
    INT_ERROR = 3
    INT_WAITING = 4
    INT_SLEEPING = 5
    INT_INPROGRESS = 6
    INT_COMPLETED = 7
    INT_FAILED = 8
    INT_NODEOK = 9
    INT_NODEFAILED = 10

    # @deprecated
    SIGNAL_CONTROLLER = 'Message'

    SIGNAL_CONTROLLER_STATS = 'ControllerStats'

    # @deprecated
    CMD_NONE = 0
    # @deprecated
    CMD_ADDDEVICE = 1
    # @deprecated
    CMD_CREATENEWPRIMARY = 2
    # @deprecated
    CMD_RECEIVECONFIGURATION = 3
    # @deprecated
    CMD_REMOVEDEVICE = 4
    # @deprecated
    CMD_REMOVEFAILEDNODE = 5
    # @deprecated
    CMD_HASNODEFAILED = 6
    # @deprecated
    CMD_REPLACEFAILEDNODE = 7
    # @deprecated
    CMD_TRANSFERPRIMARYROLE = 8
    # @deprecated
    CMD_REQUESTNETWORKUPDATE = 9
    # @deprecated
    CMD_REQUESTNODENEIGHBORUPDATE = 10
    # @deprecated
    CMD_ASSIGNRETURNROUTE = 11
    # @deprecated
    CMD_DELETEALLRETURNROUTES = 12
    # @deprecated
    CMD_SENDNODEINFORMATION = 13
    # @deprecated
    CMD_REPLICATIONSEND = 14
    # @deprecated
    CMD_CREATEBUTTON = 15
    # @deprecated
    CMD_DELETEBUTTON = 16

    def __init__(self, controller_id, network, options=None):
        """
        Initialize controller object

        :param controller_id: The Id of the controller
        :type controller_id: int
        :param network: The network the controller is attached to
        :type network: ZwaveNetwork
        :param options: options of the manager
        :type options: Options

        """

        logger.debug("Creating network controller object.")

        if controller_id is None:
            controller_id = 1
        ZWaveObject.__init__(self, controller_id, network)
        self._node = None
        self._options = options
        self._library_type_name = None
        self._library_version = None
        self._python_library_version = None
        self._timer_statistics = None
        self._interval_statistics = 0.0
        self._ctrl_lock = threading.Lock()
        # ~ self._manager_last = None
        self._ctrl_last_state = self.STATE_NORMAL
        self._ctrl_last_stateint = self.INT_NORMAL
        # ~ self._ctrl_last_message = ""
        self.STATES_LOCKED = [
            self.STATE_STARTING,
            self.STATE_WAITING,
            self.STATE_SLEEPING,
            self.STATE_INPROGRESS
        ]
        self.STATES_UNLOCKED = [
            self.STATE_NORMAL,
            self.STATE_CANCEL,
            self.STATE_ERROR,
            self.STATE_COMPLETED,
            self.STATE_FAILED,
            self.STATE_NODEOK,
            self.STATE_NODEFAILED
        ]
        logger.debug("Network controller object created.")

    def stop(self):
        """
        Stop the controller and all this threads.

        """
        self.cancel_command()
        if self._timer_statistics is not None:
            self._timer_statistics.cancel()
        for i in range(0, 60):
            if self.send_queue_count <= 0:
                break
            else:
                try:
                    self._network.network_event.wait(1.0)
                except AssertionError:
                    # For gevent AssertionError: Impossible to call blocking
                    # function in the event loop callback
                    pass
        else:
            i = 60

        self.kill_command()
        logger.debug(u"Wait for empty send_queue during %s second(s).", i)

    def __str__(self):
        """
        The string representation of the node.

        :rtype: str

        """
        node_name = ""
        product_name = ""

        if self._node is not None:
            node_name = self._node.name
            product_name = self._node.product_name

        return (
            u'home_id: [%s] '
            u'id: [%s] '
            u'name: [%s] '
            u'product: [%s] '
            u'capabilities: %s '
            u'library: [%s]' %
            (
                self._network.home_id_str,
                self._object_id,
                node_name,
                product_name,
                self.capabilities,
                self.library_description
            )
        )

    @property
    def id(self):
        return self._object_id

    @property
    def node(self):
        """
        The node controller on the network.

        :return: The node controller on the network
        :rtype: ZWaveNode
        """
        return self._node

    @node.setter
    def node(self, value):
        """
        The node controller on the network.

        :param value: The node of the controller on the network
        :type value: ZWaveNode

        """
        self._node = value

    @property
    def node_id(self):
        """
        The node Id of the controller on the network.

        :return: The node id of the controller on the network
        :rtype: int

        """
        if self.node is not None:
            return self.node.object_id

    @property
    def name(self):
        """
        The node name of the controller on the network.

        :return: The node's name of the controller on the network
        :rtype: str

        """
        if self.node is not None:
            return self.node.name

    @property
    def library_type_name(self):
        """
        The name of the library.

        :return: The cpp library name
        :rtype: str

        """
        return self._network.manager.getLibraryTypeName(self.home_id)

    @property
    def library_description(self):
        """
        The description of the library.

        :return: The library description (name and version)
        :rtype: str

        """
        return '%s version %s' % (self.library_type_name, self.library_version)

    @property
    def library_version(self):
        """
        The version of the library.

        :return: The cpp library version
        :rtype: str

        """
        return self._network.manager.getLibraryVersion(self.home_id)

    @property
    def python_library_flavor(self):
        """
        The flavor of the python library.

        :return: The python library flavor
        :rtype: str

        """
        return self._network.manager.getPythonLibraryFlavor()

    @property
    def python_library_version(self):
        """
        The version of the python library.

        :return: The python library version
        :rtype: str

        """
        return self._network.manager.getPythonLibraryVersionNumber()

    @property
    def python_library_config_version(self):
        """
        The version of the config for python library.

        :return: The python library config version
        :rtype: str

        """
        tversion = "Original %s" % self.library_version
        fversion = os.path.join(
            self.library_config_path,
            'pyozw_config.version'
        )
        if os.path.isfile(fversion):
            with open(fversion, 'r') as f:
                val = f.read()
            tversion = "Git %s" % val
        return tversion

    @property
    def ozw_library_version(self):
        """
        The version of the openzwave library.

        :return: The openzwave library version
        :rtype: str

        """
        return self._network.manager.getOzwLibraryVersion()

    @property
    def library_config_path(self):
        """
        The library Config path.

        :return: The library config directory
        :rtype: str

        """
        if self._options is not None:
            return self._options.config_path
        else:
            return None

    @property
    def library_user_path(self):
        """
        The library User path.

        :return: The user directory to store user configuration
        :rtype: str

        """
        if self._options is not None:
            return self._options.user_path
        else:
            return None

    @property
    def device(self):
        """
        The device path.

        :return: The device (ie /dev/zwave)
        :rtype: str

        """
        if self._options is not None:
            return self._options.device

    @property
    def options(self):
        """
        The starting options of the manager.

        :return: The options used to start the manager
        :rtype: ZWaveOption

        """
        return self._options

    @property
    def stats(self):
        """
        Retrieve statistics from driver.

        Statistics:

            * s_SOFCnt: SOF bytes received
            * s_ACKWaiting: unsolicited messages while waiting for an ACK
            * s_readAborts:times read were aborted due to timeouts
            * s_badChecksum: bad checksums
            * s_readCnt: messages successfully read
            * s_writeCnt: messages successfully sent
            * s_CANCnt: CAN bytes received
            * s_NAKCnt: NAK bytes received
            * s_ACKCnt: ACK bytes received
            * s_OOFCnt: bytes out of framing
            * s_dropped: messages dropped & not delivered
            * s_retries: messages retransmitted
            * s_controllerReadCnt: controller messages read
            * s_controllerWriteCnt: controller messages sent

        :return: Statistics of the controller
        :rtype: dict()

        """
        return self._network.manager.getDriverStatistics(self.home_id)

    # noinspection PyMethodMayBeStatic
    def get_stats_label(self, stat):
        """
        Retrieve label of the statistic from driver.

        :param stat: The code of the stat label to retrieve.
        :type stat:
        :return: The label or the stat.
        :rtype: str

        """
        # print "stat = %s" % stat
        return PyStatDriver[stat]

    def do_poll_statistics(self):
        """
        Timer based polling system for statistics
        """
        self._timer_statistics = None
        stats = self.stats
        dispatcher.send(
            self.SIGNAL_CONTROLLER_STATS,
            sender=self,
            network=self._network,
            controller=self,
            stats=stats
        )

        self._timer_statistics = threading.Timer(
            self._interval_statistics,
            self.do_poll_statistics
        )
        self._timer_statistics.start()

    @property
    def poll_stats(self):
        """
        The interval for polling statistics

        :return: The interval in seconds
        :rtype: float

        """
        return self._interval_statistics

    @poll_stats.setter
    def poll_stats(self, value):
        """
        The interval for polling statistics

        :return: The interval in seconds
        :rtype: ZWaveNode

        :param value: The interval in seconds
        :type value: float

        """
        if value != self._interval_statistics:
            if self._timer_statistics is not None:
                self._timer_statistics.cancel()
            if value != 0:
                self._interval_statistics = value
                self._timer_statistics = threading.Timer(
                    self._interval_statistics,
                    self.do_poll_statistics
                )
                self._timer_statistics.start()

    @property
    def capabilities(self):
        """
        The capabilities of the controller.

        :return: The capabilities of the controller
        :rtype: set

        """
        caps = set()
        if self.is_primary_controller:
            caps.add('primaryController')
        if self.is_static_update_controller:
            caps.add('staticUpdateController')
        if self.is_bridge_controller:
            caps.add('bridgeController')
        return caps

    @property
    def is_primary_controller(self):
        """
        Is this node a primary controller of the network.

        :rtype: bool

        """
        return self._network.manager.isPrimaryController(self.home_id)

    @property
    def is_static_update_controller(self):
        """
        Is this controller a static update controller (SUC).

        :rtype: bool

        """
        return self._network.manager.isStaticUpdateController(self.home_id)

    @property
    def is_bridge_controller(self):
        """
        Is this controller using the bridge controller library.

        :rtype: bool

        """
        return self._network.manager.isBridgeController(self.home_id)

    @property
    def send_queue_count(self):
        """
        Get count of messages in the outgoing send queue.

        :return: The count of messages in the outgoing send queue.
        :rtype: int

        """
        if self.home_id is not None:
            return self._network.manager.getSendQueueCount(self.home_id)
        return -1

    def hard_reset(self):
        """
        Hard Reset a PC Z-Wave Controller.
        Resets a controller and erases its network configuration settings.
        The controller becomes a primary controller ready to add devices to a
        new network.

        This command fires a lot of louie signals.
        Louie's clients must disconnect from nodes and values signals
        """
        self._network.state = self._network.STATE_RESET
        dispatcher.send(
            self._network.SIGNAL_NETWORK_RESET,
            sender=self,
            network=self._network,
            controller=self
        )
        self._network.manager.resetController(self.home_id)
        try:
            self.network.network_event.wait(5.0)
        except AssertionError:
            # For gevent AssertionError: Impossible to call blocking
            # function in the event loop callback
            pass

    def soft_reset(self):
        """
        Soft Reset a PC Z-Wave Controller.
        Resets a controller without erasing its network configuration settings.

        """
        self._network.manager.softResetController(self.home_id)

    def create_new_primary(self):
        """Create a new primary controller when old primary fails. Requires SUC.

        This command creates a new Primary Controller when the Old Primary has
        Failed. Requires a SUC on the network to function.

        Results of the CreateNewPrimary Command will be send as a Notification
        with the Notification type as
        Notification::Type_ControllerCommand

        :return: True if the request was sent successfully.
        :rtype: bool

        """
        if self._lock_controller():
            logger.debug(u'Send controller command : %s', 'create_new_primary')
            return self._network.manager.createNewPrimary(self.home_id)
        else:
            logger.warning(
                u"Can't lock controller for command : %s",
                'create_new_primary'
            )
            return False

    def transfer_primary_role(self):
        """

        Add a new controller to the network and make it the primary.

        The existing primary will become a secondary controller.

        Results of the TransferPrimaryRole Command will be send as a
        Notification with the Notification type as
        Notification::Type_ControllerCommand

        :return: True if the request was sent successfully.
        :rtype: bool

        """
        if self._lock_controller():
            logger.debug(
                u'Send controller command : %s',
                'transfer_primary_role'
            )
            return self._network.manager.transferPrimaryRole(self.home_id)
        else:
            logger.warning(
                u"Can't lock controller for command : %s",
                'create_new_primary'
            )
            return False

    def receive_configuration(self):
        """
        Receive network configuration information from primary controller.
        Requires secondary.

        This command prepares the controller to recieve Network Configuration
        from a Secondary Controller.

        Results of the ReceiveConfiguration Command will be send as a
        Notification with the Notification type as
        Notification::Type_ControllerCommand

        :return: True if the request was sent successfully.
        :rtype: bool

        """
        if self._lock_controller():
            logger.debug(
                u'Send controller command : %s',
                'receive_configuration'
            )
            return self._network.manager.receiveConfiguration(self.home_id)
        else:
            logger.warning(
                u"Can't lock controller for command : %s",
                'receive_configuration'
            )
            return False

    def add_node(self, do_security=False):
        """Start the Inclusion Process to add a Node to the Network.

        The Status of the Node Inclusion is communicated via Notifications.
        Specifically, you should monitor ControllerCommand Notifications.

        Results of the AddNode Command will be send as a Notification with the
        Notification type as Notification::Type_ControllerCommand

        :param do_security: Whether to initialize the Network Key on the device
        if it supports the Security CC
        :type do_security: bool
        :return: True if the request was sent successfully.
        :rtype: bool

        """
        if self._lock_controller():
            logger.debug(
                u'Send controller command : %s, : secure : %s',
                'add_node',
                do_security
            )
            return self._network.manager.addNode(self.home_id, do_security)
        else:
            logger.warning(
                u"Can't lock controller for command : %s",
                'add_node'
            )
            return False

    def remove_node(self):
        """Remove a Device from the Z-Wave Network

        The Status of the Node Removal is communicated via Notifications.
        Specifically, you should monitor ControllerCommand Notifications.

        Results of the RemoveNode Command will be send as a Notification with
        the Notification type as Notification::Type_ControllerCommand

        :return: True if the request was sent successfully.
        :rtype: bool

        """
        if self._lock_controller():
            logger.debug(
                u'Send controller command : %s',
                'remove_node'
            )
            return self._network.manager.removeNode(self.home_id)
        else:
            logger.warning(
                u"Can't lock controller for command : %s",
                'remove_node'
            )
            return False

    def remove_failed_node(self, node_id):
        """
        Remove a Failed Device from the Z-Wave Network

        This Command will remove a failed node from the network. The Node
        should be on the Controllers Failed Node List, otherwise this command
        will fail. You can use the HasNodeFailed function below to test if the
        Controller believes the Node has Failed.

        The Status of the Node Removal is communicated via Notifications.
        Specifically, you should monitor ControllerCommand Notifications.

        Results of the RemoveFailedNode Command will be send as a Notification
        with the Notification type as Notification::Type_ControllerCommand

        :param node_id: The ID of the node to query.
        :type node_id: int
        :return: True if the request was sent successfully.
        :rtype: bool

        """
        if self._lock_controller():
            logger.debug(
                u'Send controller command : %s, : node : %s',
                'remove_failed_node',
                node_id
            )
            return self._network.manager.removeFailedNode(
                self.home_id,
                node_id
            )
        else:
            logger.warning(
                u"Can't lock controller for command : %s",
                'remove_failed_node'
            )
            return False

    def has_node_failed(self, node_id):
        """
        Check if the Controller Believes a Node has Failed.

         This is different from the IsNodeFailed call in that we test the
         Controllers Failed Node List, whereas the IsNodeFailed is testing
         our list of Failed Nodes, which might be different.

         The Results will be communicated via Notifications. Specifically, you
         should monitor the ControllerCommand notifications

        :param node_id: The ID of the node to query.
        :type node_id: int
        :return: True if the request was sent successfully.
        :rtype: bool

        """
        if self._lock_controller():
            logger.debug(
                u'Send controller command : %s, : node : %s',
                'has_node_failed',
                node_id
            )
            return self._network.manager.hasNodeFailed(self.home_id, node_id)
        else:
            logger.warning(
                u"Can't lock controller for command : %s",
                'has_node_failed'
            )
            return False

    def request_node_neighbor_update(self, node_id):
        """
        Ask a Node to update its Neighbor Tables

        This command will ask a Node to update its Neighbor Tables.

        Results of the RequestNodeNeighborUpdate Command will be send as a
        Notification with the Notification type as
        Notification::Type_ControllerCommand

        :param node_id: The ID of the node to query.
        :type node_id: int
        :return: True if the request was sent successfully.
        :rtype: bool

        """
        if self._lock_controller():
            logger.debug(
                u'Send controller command : %s, : node : %s',
                'request_node_neighbor_update',
                node_id
            )
            return self._network.manager.requestNodeNeighborUpdate(
                self.home_id,
                node_id
            )
        else:
            logger.warning(
                u"Can't lock controller for command : %s",
                'request_node_neighbor_update'
            )
            return False

    def assign_return_route(self, node_id):
        """Ask a Node to update its update its Return Route to the Controller

        This command will ask a Node to update its Return Route to the
        Controller

        Results of the AssignReturnRoute Command will be send as a
        Notification with the Notification type as
        Notification::Type_ControllerCommand

        :param node_id: The ID of the node to query.
        :type node_id: int
        :return: True if the request was sent successfully.
        :rtype: bool

        """
        if self._lock_controller():
            logger.debug(
                u'Send controller command : %s, : node : %s',
                'assign_return_route',
                node_id
            )
            return self._network.manager.assignReturnRoute(
                self.home_id,
                node_id
            )
        else:
            logger.warning(
                u"Can't lock controller for command : %s",
                'assign_return_route'
            )
            return False

    def delete_all_return_routes(self, node_id):
        """
        Ask a Node to delete all Return Route.

        This command will ask a Node to delete all its return routes, and will
        rediscover when needed.

        Results of the DeleteAllReturnRoutes Command will be send as a
        Notification with the Notification type as
        Notification::Type_ControllerCommand

        :param node_id: The ID of the node to query.
        :type node_id: int
        :return: True if the request was sent successfully.
        :rtype: bool

        """
        if self._lock_controller():
            logger.debug(
                u'Send controller command : %s, : node : %s',
                'delete_all_return_routes',
                node_id
            )
            return self._network.manager.deleteAllReturnRoutes(
                self.home_id,
                node_id
            )
        else:
            logger.warning(
                u"Can't lock controller for command : %s",
                'delete_all_return_routes'
            )
            return False

    def send_node_information(self, node_id):
        """
        Send a NIF frame from the Controller to a Node.
        This command send a NIF frame from the Controller to a Node

        Results of the SendNodeInformation Command will be send as a
        Notification with the Notification type as
        Notification::Type_ControllerCommand

        :param node_id: The ID of the node to query.
        :type node_id: int
        :return: True if the request was sent successfully.
        :rtype: bool

        """
        if self._lock_controller():
            logger.debug(
                u'Send controller command : %s, : node : %s',
                'send_node_information',
                node_id
            )
            return self._network.manager.sendNodeInformation(
                self.home_id,
                node_id
            )
        else:
            logger.warning(
                u"Can't lock controller for command : %s",
                'send_node_information'
            )

            return False

    def replace_failed_node(self, node_id):
        """
        Replace a failed device with another.

        If the node is not in the controller's failed nodes list, or the node
        responds, this command will fail.

        You can check if a Node is in the Controllers Failed node list by
        using the HasNodeFailed method.

        Results of the ReplaceFailedNode Command will be send as a
        Notification with the Notification type as
        Notification::Type_ControllerCommand

        :param node_id: The ID of the node to query.
        :type node_id: int
        :return: True if the request was sent successfully.
        :rtype: bool

        """
        if self._lock_controller():
            logger.debug(
                u'Send controller command : %s, : node : %s',
                'replace_failed_node',
                node_id
            )
            return self._network.manager.replaceFailedNode(
                self.home_id,
                node_id
            )
        else:
            logger.warning(
                u"Can't lock controller for command : %s",
                'replace_failed_node'
            )

            return False

    def request_network_update(self, node_id):
        """
        Update the controller with network information from the SUC/SIS.

        Results of the RequestNetworkUpdate Command will be send as a
        Notification with the Notification type as
        Notification::Type_ControllerCommand

        :param node_id: The ID of the node to query.
        :type node_id: int
        :return: True if the request was sent successfully.
        :rtype: bool

        """
        if self._lock_controller():
            logger.debug(
                u'Send controller command : %s, : node : %s',
                'request_network_update',
                node_id
            )
            return self._network.manager.requestNetworkUpdate(
                self.home_id,
                node_id
            )
        else:
            logger.warning(
                u"Can't lock controller for command : %s",
                'request_network_update'
            )
            return False

    def replication_send(self, node_id):
        """
        Send information from primary to secondary

         Results of the ReplicationSend Command will be send as a Notification
         with the Notification type as Notification::Type_ControllerCommand

        :param node_id: The ID of the node to query.
        :type node_id: int
        :return: True if the request was sent successfully.
        :rtype: bool

        """
        if self._lock_controller():
            logger.debug(
                u'Send controller command : %s, : node : %s',
                'replication_send',
                node_id
            )
            return self._network.manager.replicationSend(self.home_id, node_id)
        else:
            logger.warning(
                u"Can't lock controller for command : %s",
                'replication_send'
            )
            return False

    def create_button(self, node_id, button_id):
        """
        Create a handheld button id.

        Only intended for Bridge Firmware Controllers.

        Results of the CreateButton Command will be send as a Notification
        with the Notification type as Notification::Type_ControllerCommand

        :param node_id: The ID of the node to query.
        :type node_id: int
        :param button_id: the ID of the Button to query.
        :type button_id: int
        :return: True if the request was sent successfully.
        :rtype: bool

        """
        if self._lock_controller():
            logger.debug(
                u'Send controller command : %s, : node : %s, button : %s',
                'create_button',
                node_id,
                button_id
            )
            return self._network.manager.createButton(
                self.home_id,
                node_id,
                button_id
            )
        else:
            logger.warning(
                u"Can't lock controller for command : %s",
                'create_button'
            )
            return False

    def delete_button(self, node_id, button_id):
        """
        Delete a handheld button id.

        Only intended for Bridge Firmware Controllers.

        Results of the CreateButton Command will be send as a Notification
        with the Notification type as Notification::Type_ControllerCommand

        :param node_id: The ID of the node to query.
        :type node_id: int
        :param button_id: the ID of the Button to query.
        :type button_id: int
        :return: True if the request was sent successfully.
        :rtype: bool

        """
        if self._lock_controller():
            logger.debug(
                u'Send controller command : %s, : node : %s, button : %s',
                'delete_button',
                node_id,
                button_id
            )
            return self._network.manager.deleteButton(
                self.home_id,
                node_id,
                button_id
            )
        else:
            logger.warning(
                u"Can't lock controller for command : %s",
                'delete_button'
            )
            return False

    def _handle_controller_command(self, **kwargs):
        """
        Called when a message from controller is sent.

        :param args: data sent by the notification
        :type args: dict()

        """
        logger.debug(u'Z-Wave ControllerCommand : %s', kwargs)

        if kwargs['controllerState'] == self.STATE_WAITING:
            dispatcher.send(
                self._network.SIGNAL_CONTROLLER_WAITING,
                sender=self,
                network=self._network,
                controller=self,
                **kwargs
            )

        if kwargs['controllerState'] in self.STATES_UNLOCKED:
            try:
                self._ctrl_lock.release()
            except threading.ThreadError:
                pass
        self._ctrl_last_state = kwargs['controllerState']
        self._ctrl_last_stateint = kwargs['controllerStateInt']

        if kwargs['nodeId'] in self._network.nodes:
            node = self._network.nodes[kwargs['nodeId']]
        else:
            node = None

        dispatcher.send(
            self._network.SIGNAL_CONTROLLER_COMMAND,
            sender=self,
            network=self._network,
            controller=self,
            node=node,
            node_id=kwargs.pop('nodeId'),
            **kwargs
            )

    def _lock_controller(self):
        """Try to lock the controller and generate a notification if fails
        """
        if self._ctrl_lock.acquire(False):
            return True
        else:
            state = PyControllerState[self.INT_INPROGRESS]
            dispatcher.send(
                self._network.SIGNAL_CONTROLLER_COMMAND,
                sender=self,
                network=self._network,
                controller=self,
                node=self,
                node_id=self.node_id,
                state_int=self.INT_INPROGRESS,
                state=state,
                state_full=state.doc,
                error_int=self.STATE_ERROR,
                error='Locked',
                error_full=(
                    "Can't lock controller because a "
                    "command is already in progress"
                ),
            )

    def request_controller_status(self):
        """
        Generate a notification with the current status of the controller.
        You can check the lock in your code using something like this:

            if controllerState in network.controller.STATES_UNLOCKED:
                hide_cancel_button()
                show_command_buttons()
            else:
                show_cancel_button()
                hide_command_buttons()

        """
        dispatcher.send(
            self._network.SIGNAL_CONTROLLER_COMMAND,
            sender=self,
            network=self._network,
            controller=self,
            node=self,
            node_id=self.node_id,
            state_int=self._ctrl_last_stateint,
            state=PyControllerState[self._ctrl_last_stateint],
            state_full=PyControllerState[self._ctrl_last_stateint].doc,
            error_int=0,
            error="None",
            error_full="None",
        )
        return True

    @property
    def is_locked(self):
        """
        Check if the controller is locked or not. Should not be used.
        Listen to notifications and use request_controller_status to retrieve
        the status of the controller
        """
        return self._ctrl_lock.locked()

    def cancel_command(self):
        """
        Cancels any in-progress command running on a controller.
        """
        try:
            self._ctrl_lock.release()
        except threading.ThreadError:
            pass
        if self.home_id is not None:
            return self._network.manager.cancelControllerCommand(self.home_id)
        return False

    def kill_command(self):
        """
        Cancels any in-progress command running on a controller and release
        the lock.
        """
        try:
            self._ctrl_lock.release()
        except threading.ThreadError:
            pass
        if self.home_id is not None:
            return self._network.manager.cancelControllerCommand(self.home_id)
        return False

    def to_dict(self, *extras):
        """Return a dict representation of the controller.

        :param extras: The extra information to add
        :type extras: tuple
        :returns: A dict
        :rtype: dict

        """
        if not extras:
            extras = ('all',)

        ret = self.node.to_dict(extras=extras)
        if 'all' in extras:
            extras = ('capabilities', 'neighbors')
        if 'capabilities' in extras:
            # noinspection PyTypeChecker
            ret['capabilities'].update(dict.fromkeys(self.capabilities, 0))
        ret["zw_version"] = self.library_version
        ret["zw_description"] = self.library_description
        ret["oz_version"] = self.ozw_library_version
        ret["py_version"] = self.python_library_version
        ret["py_config_version"] = self.python_library_config_version
        return ret

    def update_ozw_config(self):
        """
        Update the openzwave config from github.
        Not available for shared flavor as we don't want to update the config
        of the precompiled config.

        """
        if self.python_library_flavor in ['shared']:
            logger.warning(
                u"Can't update_ozw_config for this flavor (%s).",
                self.python_library_flavor
            )
            return
        import traceback

        logger.info(u'Update_ozw_config from github.')
        dest = tempfile.mkdtemp()
        src = os.path.join(dest, 'open-zwave-master', 'config')
        version_file = os.path.join(
            self.library_config_path,
            'pyozw_config.version'
        )
        try:
            response = requests.get(
                'https://codeload.github.com/OpenZWave/open-zwave/zip/master'
            )
        except requests.HTTPError:
            logger.exception("Can't get zip from github. Cancelling")
        else:
            from io import BytesIO

            dest_file = BytesIO(response.content)
            dest_file.seek(0)
            try:
                zip_ref = zipfile.ZipFile(dest_file)
                zip_ref.extractall(dest)
                zip_ref.close()
            except (IOError, WindowsError):
                logger.exception("Unable to unpack config files.")
            else:
                for root, dirs, files in os.walk(src):
                    dest_dir = os.path.join(self.library_config_path, root)
                    src_dir = os.path.join(src, root)
                    if not os.path.exists(dest_dir):
                        try:
                            shutil.copytree(src_dir, dest)
                        except WindowsError:
                            logger.exception(
                                "Can't update config files,"
                                " permission error %s",
                                traceback.format_exc()
                            )
                            break
                    else:
                        try:
                            for f in files:
                                src_file = os.path.join(src_dir, f)
                                dst_file = os.path.join(dest_dir, f)
                                with open(src_file, 'r') as src_file:
                                    src_file = src_file.read()
                                if os.path.exists(dst_file):
                                    with open(dst_file, 'r') as dst_f:
                                        dst_f = dst_f.read()
                                    if src_file == dst_f:
                                        continue

                                with open(dst_file, 'w') as dst_file:
                                    dst_file.write(src_file)
                        except (IOError, WindowsError):
                            logger.exception(
                                "Can't update config files,"
                                " permission error %s",
                                traceback.format_exc()
                            )
                            break
                else:
                    try:
                        with open(version_file, 'w') as f:
                            f.write(time.strftime("%Y-%m-%d %H:%M"))
                    except (IOError, WindowsError):
                        logger.exception("Can't update %s", version_file)

            shutil.rmtree(dest, True)

