# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
# Copyright Â© 2005-2016 EventGhost Project <http://www.eventghost.org/>
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

DEBUG = False

# noinspection PyUnresolvedReferences
import eg # NOQA

eg.RegisterPlugin(
    name='ZWave',
    author='K',
    version='0.5.3b',
    description='Z-Wave Control',
    kind='external',
    canMultiLoad=False,
    createMacrosOnAdd=True,
    guid='{06B57C0C-FCFD-4673-8D76-7DF6EF769903}',
    hardwareId='USB\\VID_0658&PID_0200',
    icon=None
)

import threading # NOQA
import os # NOQA
import wx # NOQA
import shutil # NOQA
import dispatcher # NOQA
import logging # NOQA
import zwave_admin # NOQA
import zwave_discovery # NOQA
from logging import NullHandler # NOQA

logger = logging.getLogger('openzwave')
logger.addHandler(NullHandler())
logger.setLevel(logging.DEBUG if DEBUG else logging.NOTSET)

logger = logging.getLogger('libopenzwave')
logger.addHandler(NullHandler())
logger.setLevel(logging.DEBUG if DEBUG else logging.NOTSET)


USER_DIR = os.path.join(
    eg.folderPath.ProgramData,
    eg.APP_NAME,
    'ZWave'
)

ZWAVE_CONFIG = os.path.join(
    USER_DIR,
    'config'
)

SIGNAL_NETWORK_FAILED = None
SIGNAL_NETWORK_START = None
SIGNAL_NETWORK_READY = None
SIGNAL_NETWORK_STOP = None
SIGNAL_NETWORK_RESET = None
SIGNAL_NETWORK_AWAKE = None
SIGNAL_GROUP = None
SIGNAL_NODE_ADDED = None
SIGNAL_NODE_EVENT = None
SIGNAL_NODE_NAMING = None
SIGNAL_NODE_NEW = None
SIGNAL_NODE_PROTOCOL_INFO = None
SIGNAL_NODE_READY = None
SIGNAL_NODE_REMOVED = None
SIGNAL_SCENE_EVENT = None
SIGNAL_VALUE_ADDED = None
SIGNAL_VALUE_CHANGED = None
SIGNAL_VALUE_REFRESHED = None
SIGNAL_VALUE_REMOVED = None
SIGNAL_POLLING_ENABLED = None
SIGNAL_POLLING_DISABLED = None
SIGNAL_CREATE_BUTTON = None
SIGNAL_DELETE_BUTTON = None
SIGNAL_BUTTON_ON = None
SIGNAL_BUTTON_OFF = None
SIGNAL_ESSENTIAL_NODE_QUERIES_COMPLETE = None
SIGNAL_NODE_QUERIES_COMPLETE = None
SIGNAL_AWAKE_NODES_QUERIED = None
SIGNAL_ALL_NODES_QUERIED = None
SIGNAL_ALL_NODES_QUERIED_SOME_DEAD = None
SIGNAL_MSG_COMPLETE = None
SIGNAL_NOTIFICATION = None
SIGNAL_CONTROLLER_COMMAND = None
SIGNAL_CONTROLLER_WAITING = None
SIGNAL_CONTROLLER_STATS = None


class Network(object):

    def __init__(self, com_port, name, poll_interval):

        from zwave_network import ZWaveNetwork
        import zwave_option

        self.startup_event = threading.Event()
        self.com_port = com_port
        self.name = name
        self.poll_interval = poll_interval

        folder_name = name

        for char in list('<>:"/\\|?*') + list(chr(i) for i in range(32)):
            folder_name = folder_name.replace(char, '')

        user_config_dir = os.path.join(USER_DIR, folder_name)

        if os.path.exists(user_config_dir):
            self.initial_setup = False
        else:
            self.initial_setup = True
            os.mkdir(user_config_dir)

        options = zwave_option.ZWaveOption(
            device=str('\\\\.\\' + com_port),
            config_path=str(ZWAVE_CONFIG),
            user_path=str(user_config_dir),
            cmd_line=str('')
        )

        options.set_console_output(DEBUG)
        options.set_logging(DEBUG)
        options.set_save_log_level('Debug' if DEBUG else 'None')
        options.set_save_configuration(True)
        options.set_poll_interval(poll_interval)
        options.set_interval_between_polls(True)
        options.set_suppress_value_refresh(True)
        options.lock()

        self.zwave_network = ZWaveNetwork(name, options, auto_start=False)

    def __getattr__(self, item):
        if item in self.__dict__:
            return self.__dict__[item]

        return getattr(self.zwave_network, item)

    def start(self):
        def do():
            from zwave_network import ZWaveNetwork

            if self.initial_setup:
                self.startup_event.wait(3)

                eg.PrintNotice(
                    '\n\n'
                    'Z-Wave: New network added.\n'
                    'Z-Wave: Scanning network please wait...\n\n'
                )

                self.startup_event.wait(3)

            self.zwave_network.start()

            while (
                not self.startup_event.isSet() and
                (
                    self.zwave_network.state <
                    ZWaveNetwork.STATE_AWAKE
                )
            ):
                self.startup_event.wait(0.001)

            if self.initial_setup:
                self.startup_event.wait(3)

                eg.PrintNotice(
                    '\n\n'
                    'Z-Wave: Finished scanning network.\n'
                    'Z-Wave: Applying changes to the network.\n'
                    'Z-Wave: Stopping network.\n\n'

                )

                self.startup_event.wait(3)
                self.zwave_network.stop()

                while (
                    not self.startup_event.isSet() and
                    (
                        self.zwave_network.state !=
                        ZWaveNetwork.STATE_STOP
                    )
                ):
                    self.startup_event.wait(0.001)

                self.startup_event.wait(3)

                eg.PrintNotice(
                    '\n\n'
                    'Z-Wave: Saving network data.\n'
                    'Z-Wave: Starting network with new parameters.\n\n'
                )

                self.startup_event.wait(3)

                self.zwave_network.start()
                while (
                    not self.startup_event.isSet() and
                    (
                        self.zwave_network.state <
                        ZWaveNetwork.STATE_AWAKE
                    )
                ):
                    self.startup_event.wait(0.001)

                self.startup_event.wait(3)

                eg.PrintNotice(
                    '\n\n'
                    'Z-Wave: Finished initializing new network.\n\n'
                )

            self.zwave_network.set_poll_interval(100, True)

            # for node in self.zwave_network.nodes.values():
            #     for value in node.properties:
            #         value.enable_poll()

        threading.Thread(target=do).start()

    def stop(self):
        self.startup_event.set()
        self.zwave_network.stop()


py = os.path.join(eg.mainDir, 'py.exe')
pyw = os.path.join(eg.mainDir, 'pyw.exe')
dll = os.path.join(eg.mainDir, 'python27.dll')

py_backup = os.path.join(eg.mainDir, 'py.exe.backup')
pyw_backup = os.path.join(eg.mainDir, 'pyw.exe.backup')
dll_backup = os.path.join(eg.mainDir, 'python27.dll.backup')

EG_UPDATED = (
    os.path.exists(py_backup) and
    os.path.exists(pyw_backup) and
    os.path.exists(dll_backup)
)


def rollback_update():
    def restore_file(src, dst):
        try:
            if os.path.exists(src):
                os.remove(dst)
                os.rename(src, dst)
                return ''
            else:
                return ''
        except WindowsError:
            return (
                'del "{dst}"\n'
                'rename "{src}" "{py_file}"\n'
            ).format(
                src=src,
                dst=dst,
                py_file=os.path.split(dst)[1]
            )

    manual_directions = (
        restore_file(py_backup, py) +
        restore_file(pyw_backup, pyw) +
        restore_file(dll_backup, dll)
    )

    if manual_directions:
        eg.PrintError(
            'Z-Wave: Error restoring original core files.\n'
            'Close EventGhost and copy the lines below and past them into '
            'a command prompt.\n' +
            manual_directions
        )
    else:
        eg.PrintNotice(
            'Z-Wave: Successfully restored core files.\n'
            'Please Restart EventGhost.'
        )


def update_core_files():

    def copy_file(src, dst, backup):
        try:
            if not os.path.exists(backup):
                os.rename(dst, backup)
                shutil.copy(src, dst)
                return ''
            else:
                return ''
        except WindowsError:
            return (
                'rename "{dst}" "{backup}"\n'
                'copy "{src}" "{dst}"\n'
            ).format(
                src=src,
                dst=dst,
                backup=os.path.split(backup)[1]

            )

    base_path = os.path.join(os.path.dirname(__file__), 'python_core')

    src_py = os.path.join(base_path, 'py.exe')
    src_pyw = os.path.join(base_path, 'pyw.exe')
    src_dll = os.path.join(base_path, 'python27.dll')

    directions = (
        copy_file(src_py, py, py_backup) +
        copy_file(src_pyw, pyw, pyw_backup) +
        copy_file(src_dll, dll, dll_backup)
    )

    if directions:
        manual_directions = (
            '***MANUAL DIRECTIONS***\n\n'
            'Read ALL instructions before continuing.\n\n'
            '1. Copy the lines below.\n\n\n'
            '{directions}\n\n'
            '2, Press the OK button to finish the plugin installation.\n'
            '3. Close EventGhost.\n'
            '4. Open a command prompt as Administrator.\n'
            '5. Paste the lines you copied into the command prompt.\n'
            '6. Start EventGhost.\n'
        ).format(directions=directions)

        return (
            (
                'Unable to update EventGhost core.\n\n'
                'You can try running EventGhost as Administrator\n'
                'and install the plugin again.\n\n'
                'Or you can perform a manual installation by following\n'
                'the directions below.\n\n'
            ),
            manual_directions
        )

    return (
        (
            'EventGhost core files have been successfully '
            'upgraded.\n\n'
            'Press the OK button to continue installation '
            'of the plugin.\n'
            'Then restart EventGhost.\n'
        ),
        None
    )


# noinspection PyPep8Naming
class ZWave(eg.PluginBase):

    def __init__(self):
        if not EG_UPDATED:
            return

        if not os.path.exists(USER_DIR):
            os.mkdir(USER_DIR)

        if not os.path.exists(ZWAVE_CONFIG):
            shutil.copytree(
                os.path.join(os.path.dirname(__file__), 'ozw_config'),
                ZWAVE_CONFIG
            )

        from zwave_network import ZWaveNetwork

        global SIGNAL_NETWORK_FAILED
        global SIGNAL_NETWORK_START
        global SIGNAL_NETWORK_READY
        global SIGNAL_NETWORK_STOP
        global SIGNAL_NETWORK_RESET
        global SIGNAL_NETWORK_AWAKE
        global SIGNAL_GROUP
        global SIGNAL_NODE_ADDED
        global SIGNAL_NODE_EVENT
        global SIGNAL_NODE_NAMING
        global SIGNAL_NODE_NEW
        global SIGNAL_NODE_PROTOCOL_INFO
        global SIGNAL_NODE_READY
        global SIGNAL_NODE_REMOVED
        global SIGNAL_SCENE_EVENT
        global SIGNAL_VALUE_ADDED
        global SIGNAL_VALUE_CHANGED
        global SIGNAL_VALUE_REFRESHED
        global SIGNAL_VALUE_REMOVED
        global SIGNAL_POLLING_ENABLED
        global SIGNAL_POLLING_DISABLED
        global SIGNAL_CREATE_BUTTON
        global SIGNAL_DELETE_BUTTON
        global SIGNAL_BUTTON_ON
        global SIGNAL_BUTTON_OFF
        global SIGNAL_ESSENTIAL_NODE_QUERIES_COMPLETE
        global SIGNAL_NODE_QUERIES_COMPLETE
        global SIGNAL_AWAKE_NODES_QUERIED
        global SIGNAL_ALL_NODES_QUERIED
        global SIGNAL_ALL_NODES_QUERIED_SOME_DEAD
        global SIGNAL_MSG_COMPLETE
        global SIGNAL_NOTIFICATION
        global SIGNAL_CONTROLLER_COMMAND
        global SIGNAL_CONTROLLER_WAITING
        global SIGNAL_CONTROLLER_STATS

        SIGNAL_NETWORK_FAILED = ZWaveNetwork.SIGNAL_NETWORK_FAILED
        SIGNAL_NETWORK_START = ZWaveNetwork.SIGNAL_NETWORK_START
        SIGNAL_NETWORK_READY = ZWaveNetwork.SIGNAL_NETWORK_READY
        SIGNAL_NETWORK_STOP = ZWaveNetwork.SIGNAL_NETWORK_STOP
        SIGNAL_NETWORK_RESET = ZWaveNetwork.SIGNAL_NETWORK_RESET
        SIGNAL_NETWORK_AWAKE = ZWaveNetwork.SIGNAL_NETWORK_AWAKE
        SIGNAL_GROUP = ZWaveNetwork.SIGNAL_GROUP
        SIGNAL_NODE_ADDED = ZWaveNetwork.SIGNAL_NODE_ADDED
        SIGNAL_NODE_EVENT = ZWaveNetwork.SIGNAL_NODE_EVENT
        SIGNAL_NODE_NAMING = ZWaveNetwork.SIGNAL_NODE_NAMING
        SIGNAL_NODE_NEW = ZWaveNetwork.SIGNAL_NODE_NEW
        SIGNAL_NODE_PROTOCOL_INFO = ZWaveNetwork.SIGNAL_NODE_PROTOCOL_INFO
        SIGNAL_NODE_READY = ZWaveNetwork.SIGNAL_NODE_READY
        SIGNAL_NODE_REMOVED = ZWaveNetwork.SIGNAL_NODE_REMOVED
        SIGNAL_SCENE_EVENT = ZWaveNetwork.SIGNAL_SCENE_EVENT
        SIGNAL_VALUE_ADDED = ZWaveNetwork.SIGNAL_VALUE_ADDED
        SIGNAL_VALUE_CHANGED = ZWaveNetwork.SIGNAL_VALUE_CHANGED
        SIGNAL_VALUE_REFRESHED = ZWaveNetwork.SIGNAL_VALUE_REFRESHED
        SIGNAL_VALUE_REMOVED = ZWaveNetwork.SIGNAL_VALUE_REMOVED
        SIGNAL_POLLING_ENABLED = ZWaveNetwork.SIGNAL_POLLING_ENABLED
        SIGNAL_POLLING_DISABLED = ZWaveNetwork.SIGNAL_POLLING_DISABLED
        SIGNAL_CREATE_BUTTON = ZWaveNetwork.SIGNAL_CREATE_BUTTON
        SIGNAL_DELETE_BUTTON = ZWaveNetwork.SIGNAL_DELETE_BUTTON
        SIGNAL_BUTTON_ON = ZWaveNetwork.SIGNAL_BUTTON_ON
        SIGNAL_BUTTON_OFF = ZWaveNetwork.SIGNAL_BUTTON_OFF
        SIGNAL_ESSENTIAL_NODE_QUERIES_COMPLETE = (
            ZWaveNetwork.SIGNAL_ESSENTIAL_NODE_QUERIES_COMPLETE
        )
        SIGNAL_NODE_QUERIES_COMPLETE = (
            ZWaveNetwork.SIGNAL_NODE_QUERIES_COMPLETE
        )
        SIGNAL_AWAKE_NODES_QUERIED = ZWaveNetwork.SIGNAL_AWAKE_NODES_QUERIED
        SIGNAL_ALL_NODES_QUERIED = ZWaveNetwork.SIGNAL_ALL_NODES_QUERIED
        SIGNAL_ALL_NODES_QUERIED_SOME_DEAD = (
            ZWaveNetwork.SIGNAL_ALL_NODES_QUERIED_SOME_DEAD
        )
        SIGNAL_MSG_COMPLETE = ZWaveNetwork.SIGNAL_MSG_COMPLETE
        SIGNAL_NOTIFICATION = ZWaveNetwork.SIGNAL_NOTIFICATION
        SIGNAL_CONTROLLER_COMMAND = ZWaveNetwork.SIGNAL_CONTROLLER_COMMAND
        SIGNAL_CONTROLLER_WAITING = ZWaveNetwork.SIGNAL_CONTROLLER_WAITING
        SIGNAL_CONTROLLER_STATS = ZWaveNetwork.SIGNAL_CONTROLLER_STATS

        dispatcher.connect(self.signal_network, SIGNAL_NETWORK_FAILED)
        dispatcher.connect(self.signal_network, SIGNAL_NETWORK_START)
        dispatcher.connect(self.signal_network, SIGNAL_NETWORK_READY)
        dispatcher.connect(self.signal_network, SIGNAL_NETWORK_STOP)
        dispatcher.connect(self.signal_network, SIGNAL_NETWORK_RESET)
        dispatcher.connect(self.signal_network, SIGNAL_NETWORK_AWAKE)
        dispatcher.connect(self.signal_group, SIGNAL_GROUP)
        dispatcher.connect(self.signal_node, SIGNAL_NODE_ADDED)
        dispatcher.connect(self.signal_node, SIGNAL_NODE_EVENT)
        dispatcher.connect(self.signal_node, SIGNAL_NODE_NAMING)
        dispatcher.connect(self.signal_node, SIGNAL_NODE_NEW)
        dispatcher.connect(self.signal_node, SIGNAL_NODE_PROTOCOL_INFO)
        dispatcher.connect(self.signal_node, SIGNAL_NODE_READY)
        dispatcher.connect(self.signal_node, SIGNAL_NODE_REMOVED)
        dispatcher.connect(self.signal_scene, SIGNAL_SCENE_EVENT)
        dispatcher.connect(self.signal_value, SIGNAL_VALUE_ADDED)
        dispatcher.connect(self.signal_value, SIGNAL_VALUE_CHANGED)
        dispatcher.connect(self.signal_value, SIGNAL_VALUE_REFRESHED)
        dispatcher.connect(self.signal_value, SIGNAL_VALUE_REMOVED)
        dispatcher.connect(self.signal_button, SIGNAL_CREATE_BUTTON)
        dispatcher.connect(self.signal_button, SIGNAL_DELETE_BUTTON)
        dispatcher.connect(self.signal_button, SIGNAL_BUTTON_ON)
        dispatcher.connect(self.signal_button, SIGNAL_BUTTON_OFF)
        dispatcher.connect(
            self.signal_queries,
            SIGNAL_ESSENTIAL_NODE_QUERIES_COMPLETE
        )
        dispatcher.connect(self.signal_queries, SIGNAL_NODE_QUERIES_COMPLETE)
        dispatcher.connect(self.signal_queries, SIGNAL_AWAKE_NODES_QUERIED)
        dispatcher.connect(self.signal_queries, SIGNAL_ALL_NODES_QUERIED)
        dispatcher.connect(
            self.signal_queries,
            SIGNAL_ALL_NODES_QUERIED_SOME_DEAD
        )

        if DEBUG:
            dispatcher.connect(self.signal_polling, SIGNAL_POLLING_ENABLED)
            dispatcher.connect(self.signal_polling, SIGNAL_POLLING_DISABLED)
            dispatcher.connect(self.signal_msg, SIGNAL_MSG_COMPLETE)
            dispatcher.connect(self.signal_notification, SIGNAL_NOTIFICATION)
            dispatcher.connect(
                self.signal_controller,
                SIGNAL_CONTROLLER_COMMAND
            )
            dispatcher.connect(
                self.signal_controller,
                SIGNAL_CONTROLLER_WAITING
            )
            dispatcher.connect(
                self.signal_controller,
                SIGNAL_CONTROLLER_STATS
            )

        self.networks = []
        self.AddAction(Set)
        self.AddAction(Get)
        self.AddAction(RampDownDimmer)
        self.AddAction(RampUpDimmer)
        self._config_event = threading.Event()
        self._config_event.set()

        self._save = eg.document.Save
        self._save_as = eg.document.SaveAs

    def signal_network(
        self,
        signal,
        network,
        **kwargs
    ):
        del kwargs['sender']
        event = '{0}.{1}'.format(network.name, signal)
        if signal == SIGNAL_NETWORK_FAILED:
            self.TriggerEvent(event, kwargs)
        elif signal == SIGNAL_NETWORK_START:
            self.TriggerEvent(event, kwargs)
        elif signal == SIGNAL_NETWORK_READY:
            self.TriggerEvent(event, kwargs)
        elif signal == SIGNAL_NETWORK_STOP:
            self.TriggerEvent(event, kwargs)
        elif signal == SIGNAL_NETWORK_RESET:
            self.TriggerEvent(event, kwargs)
        elif signal == SIGNAL_NETWORK_AWAKE:
            self.TriggerEvent(event, kwargs)

    def signal_group(
        self,
        signal,
        network,
        node,
        node_id,
        group_id,
        **kwargs
    ):
        del kwargs['sender']
        name = node.name
        if not name:
            name = '0x' + hex(node_id)[2:].upper()

        group_id = '0x' + hex(group_id)[2:].upper()

        try:
            node_room = node.location
        except AttributeError:
            node_room = None

        event = '{0}.{1}.{2}.Group.{3}.{4}'.format(
            network.name,
            node_room + '.' + name if node_room else name,
            node.specific_as_str.replace(' ', ''),
            group_id,
            signal
        )
        if signal == SIGNAL_GROUP:
            self.TriggerEvent(event, kwargs)

    def signal_node(
        self,
        signal,
        network,
        node,
        node_id,
        **kwargs
    ):
        del kwargs['sender']
        name = node.name
        if not name:
            name = '0x' + hex(node_id)[2:].upper()

        try:
            node_room = node.location
        except AttributeError:
            node_room = None

        event = '{0}.{1}.{2}.{3}'.format(
            network.name,
            node_room + '.' + name if node_room else name,
            node.specific_as_str.replace(' ', ''),
            signal
        )

        if signal == SIGNAL_NODE_ADDED:
            self.TriggerEvent(event.replace('NodeAdded', 'Added'), kwargs)
        elif signal == SIGNAL_NODE_EVENT:
            self.TriggerEvent(event, kwargs)
        elif signal == SIGNAL_NODE_NAMING:
            self.TriggerEvent(event, kwargs)
        elif signal == SIGNAL_NODE_NEW:
            self.TriggerEvent(event, kwargs)
        elif signal == SIGNAL_NODE_PROTOCOL_INFO:
            self.TriggerEvent(event, kwargs)
        elif signal == SIGNAL_NODE_READY:
            self.TriggerEvent(event.replace('NodeReady', 'Ready'), kwargs)
        elif signal == SIGNAL_NODE_REMOVED:
            self.TriggerEvent(event.replace('NodeRemoved', 'Removed'), kwargs)

    def signal_scene(
        self,
        signal,
        network,
        node,
        node_id,
        scene_id,
        **kwargs
    ):
        del kwargs['sender']

        name = node.name
        if not name:
            name = '0x' + hex(node_id)[2:].upper()

        scene_id = '0x' + hex(scene_id)[2:].upper()

        try:
            node_room = node.location
        except AttributeError:
            node_room = None

        event = '{0}.{1}.{2}.Scene.{3}.{4}'.format(
            network.name,
            node_room + '.' + name if node_room else name,
            node.specific_as_str.replace(' ', ''),
            scene_id,
            signal
        )
        if signal == SIGNAL_SCENE_EVENT:
            self.TriggerEvent(event, kwargs)

    def signal_value(
        self,
        signal,
        network,
        node,
        node_id,
        value,
        value_id,
        changed_values=None,
        refreshed_values=None,
        **kwargs
    ):
        del kwargs['sender']

        name = node.name
        if not name:
            name = '0x' + hex(node_id)[2:].upper()

        label = value.label.replace(' ', '')

        if not label:
            label = '0x' + hex(value_id)[2:].upper()
        try:
            node_room = node.location
        except AttributeError:
            node_room = None

        event = '{0}.{1}.{2}.Variable.'.format(
            network.name,
            node_room + '.' + name if node_room else name,
            node.specific_as_str.replace(' ', ''),
        )

        if signal == SIGNAL_VALUE_ADDED:
            event += 'Added'
            self.TriggerEvent(event, dict(label=value.label))

        elif signal == SIGNAL_VALUE_CHANGED:
            for attr in changed_values:
                if attr == 'data':
                    self.TriggerEvent(
                        event.replace('Variable', label) + str(value.data)
                    )
                else:
                    self.TriggerEvent(
                        event + 'Changed',
                        dict(
                            label=value.label,
                            property=attr,
                            value=getattr(value, attr)
                        )
                    )

        elif signal == SIGNAL_VALUE_REFRESHED:
            for attr in refreshed_values:
                self.TriggerEvent(
                    event + 'Refreshed',
                    dict(label=value.label, property=attr)
                )

        elif signal == SIGNAL_VALUE_REMOVED:
            event += 'Removed'
            self.TriggerEvent(event, dict(label=value.label))

    def signal_polling(
        self,
        signal,
        network,
        node,
        node_id,
        **kwargs
    ):
        del kwargs['sender']

        name = node.name
        if not name:
            name = '0x' + hex(node_id)[2:].upper()

        try:
            node_room = node.location
        except AttributeError:
            node_room = None

        event = '{0}.{1}.{2}.{3}'.format(
            network.name,
            node_room + '.' + name if node_room else name,
            node.specific_as_str.replace(' ', ''),
            signal
        )

        if signal == SIGNAL_POLLING_ENABLED:
            self.TriggerEvent(event, kwargs)
        elif signal == SIGNAL_POLLING_DISABLED:
            self.TriggerEvent(event, kwargs)

    def signal_button(
        self,
        signal,
        network,
        node,
        node_id,
        **kwargs
    ):
        del kwargs['sender']

        name = node.name
        if not name:
            name = '0x' + hex(node_id)[2:].upper()

        try:
            node_room = node.location
        except AttributeError:
            node_room = None

        event = '{0}.{1}.{2}.{3}'.format(
            network.name,
            node_room + '.' + name if node_room else name,
            node.specific_as_str.replace(' ', ''),
            signal
        )

        if signal == SIGNAL_CREATE_BUTTON:
            self.TriggerEvent(event, kwargs)
        elif signal == SIGNAL_DELETE_BUTTON:
            self.TriggerEvent(event, kwargs)
        elif signal == SIGNAL_BUTTON_ON:
            self.TriggerEvent(event, kwargs)
        elif signal == SIGNAL_BUTTON_OFF:
            self.TriggerEvent(event, kwargs)

    def signal_queries(
        self,
        signal,
        network,
        **kwargs
    ):
        del kwargs['sender']

        if 'node' in kwargs:
            node = kwargs.pop('node')
            node_id = kwargs.pop('node_id')
            name = node.name
            if not name:
                name = '0x' + hex(node_id)[2:].upper()

            try:
                node_room = node.location
            except AttributeError:
                node_room = None

            event = '{0}.{1}.{2}.{3}'.format(
                network.name,
                node_room + '.' + name if node_room else name,
                node.specific_as_str.replace(' ', ''),
                signal
            )
        else:
            event = '{0}.{1}'.format(network.name, signal)

        if signal == SIGNAL_ESSENTIAL_NODE_QUERIES_COMPLETE:
            self.TriggerEvent(event, kwargs)
        elif signal == SIGNAL_NODE_QUERIES_COMPLETE:
            self.TriggerEvent(event, kwargs)
        elif signal == SIGNAL_AWAKE_NODES_QUERIED:
            self.TriggerEvent(event, kwargs)
        elif signal == SIGNAL_ALL_NODES_QUERIED:
            self.TriggerEvent(event, kwargs)
        elif signal == SIGNAL_ALL_NODES_QUERIED_SOME_DEAD:
            self.TriggerEvent(event, kwargs)

    def signal_msg(
        self,
        signal,
        network,
        **kwargs
    ):
        del kwargs['sender']
        event = '{0}.{1}'.format(network.name, signal)
        if signal == SIGNAL_MSG_COMPLETE:
            self.TriggerEvent(event, kwargs)

    def signal_notification(
        self,
        signal,
        network,
        **kwargs
    ):
        del kwargs['sender']
        event = '{0}.{1}'.format(network.name, signal)
        if signal == SIGNAL_NOTIFICATION:
            self.TriggerEvent(event, kwargs)

    def signal_controller(
        self,
        signal,
        network,
        **kwargs
    ):
        del kwargs['sender']
        del kwargs['controller']
        event = '{0}.Controller.{1}'.format(network.name, signal)
        if signal == SIGNAL_CONTROLLER_COMMAND:
            self.TriggerEvent(event, kwargs)

        elif signal == SIGNAL_CONTROLLER_WAITING:
            self.TriggerEvent(event, kwargs)

        elif signal == SIGNAL_CONTROLLER_STATS:
            self.TriggerEvent(event, kwargs['stats'])

    def device_attached(self, _):
        com_ports = zwave_discovery.devices
        for com_port in com_ports:
            for network in self.networks:
                if network.com_port == com_port:
                    break
            else:
                if com_port in self.z_sticks:
                    network = Network(str(com_port), **self.z_sticks[com_port])
                    self.networks += [network]
                    network.start()
        return False

    def device_removed(self, _):
        com_ports = zwave_discovery.devices

        for network in self.networks:
            if network.com_port not in com_ports:
                network.stop()
                self.networks.remove(network)

        return False

    def __start__(self, z_sticks):
        eg.document.Save = self.save
        eg.document.SaveAs = self.save_as

        if EG_UPDATED:
            self.z_sticks = z_sticks

            for comport in zwave_discovery.devices:
                if comport in z_sticks:
                    network = Network(str(comport), **z_sticks[comport])
                    self.networks += [network]
                    network.start()

            eg.Bind('System.DeviceAttached', self.device_attached)
            eg.Bind('System.DeviceRemoved', self.device_removed)

        else:
            if z_sticks:
                eg.PrintError(
                    'Z-Wave: Plugin Error - unable to '
                    'locate modified core files.\n'
                    'Please open the plugin configuration dialog and '
                    'follow the instructions.'
                )
            else:
                eg.PrintNotice('Z-Wave: Restart EventGhost')
            return

    def __stop__(self):
        eg.document.Save = self._save
        eg.document.SaveAs = self._save_as
        if EG_UPDATED:
            eg.Unbind('System.DeviceAttached', self.device_attached)
            eg.Unbind('System.DeviceRemoved', self.device_removed)
            zwave_discovery.stop()
            for network in self.networks:
                network.stop()

            del self.networks[:]

    def save(self):
        eg.document.SaveAs = self._save_as
        if self._save() == wx.ID_YES:
            for network in self.networks:
                network.write_config()
        eg.document.SaveAs = self.save_as

    def save_as(self):
        if self._save_as() == wx.ID_YES:
            for network in self.networks:
                network.write_config()

    # noinspection PyMethodMayBeStatic
    def OnDelete(self):
        rollback_update()

    # noinspection PyDefaultArgument
    def Configure(self, z_sticks=dict()):
        panel = eg.ConfigPanel()

        if EG_UPDATED:
            com_ports = zwave_discovery.devices
            zwave_discovery.stop()

            # noinspection PyPep8
            class DeviceLine(wx.Panel):
                def __init__(
                    self,
                    parent,
                    prt,
                    in_use,
                    nme,
                    poll_int,
                    ntwrk=None,
                    display_led=False
                ):

                    wx.Panel.__init__(self, parent, -1, style=wx.BORDER_SUNKEN)

                    main_sizer = wx.BoxSizer(wx.HORIZONTAL)
                    port_ctrl = wx.CheckBox(self, -1, prt)
                    port_ctrl.SetValue(in_use)

                    name_st = wx.StaticText(self, -1, 'Network Name:')
                    name_ctrl = wx.TextCtrl(self, -1, nme)

                    poll_st = wx.StaticText(self, -1, 'Poll Interval')
                    poll_ctrl = eg.SpinIntCtrl(self, -1, value=poll_int)

                    name_ctrl.Enable(in_use)
                    poll_ctrl.Enable(in_use)

                    main_sizer.Add(port_ctrl, 0, wx.EXPAND | wx.ALL, 5)
                    main_sizer.Add(name_st, 0, wx.EXPAND | wx.ALL, 5)
                    main_sizer.Add(name_ctrl, 0, wx.EXPAND | wx.ALL, 5)
                    main_sizer.Add(poll_st, 0, wx.EXPAND | wx.ALL, 5)
                    main_sizer.Add(poll_ctrl, 0, wx.EXPAND | wx.ALL, 5)

                    def get_values():
                        return (
                            port_ctrl.GetLabel(),
                            name_ctrl.GetValue(),
                            poll_ctrl.GetValue()
                        )

                    def in_use():
                        return port_ctrl.GetValue()

                    self.InUse = in_use

                    self.GetValues = get_values

                    def on_check(evt):
                        name_ctrl.Enable(port_ctrl.GetValue())
                        poll_ctrl.Enable(port_ctrl.GetValue())
                        evt.Skip()

                    port_ctrl.Bind(wx.EVT_CHECKBOX, on_check)

                    if display_led:
                        led_st = wx.StaticText(self, -1, 'LED:')
                        led_ctrl = wx.Choice(
                            self,
                            -1,
                            choices=['', 'On', 'Off']
                        )

                        main_sizer.Add(led_st, 0, wx.EXPAND | wx.ALL, 5)
                        main_sizer.Add(led_ctrl, 0, wx.EXPAND | wx.ALL, 5)

                        # noinspection PyUnusedLocal
                        def on_led(_):
                            items = led_ctrl.GetItems()
                            value = led_ctrl.GetStringSelection()
                            if value and len(items) == 3:
                                items = items[1:]
                                led_ctrl.Clear()
                                led_ctrl.AppendItems(items)
                                led_ctrl.SetStringSelection(value)
                            elif not value:
                                return

                            on = '\x01\x06\x00\xF2\x51\x01\x01\x5A'
                            success = '\x01\x04\x01\xF2\x01\x09'
                            success_reply = '\x06'
                            off = '\x01\x06\x00\xF2\x51\x01\x00\x5B'

                            def send_command():
                                try:
                                    serial = eg.SerialPort()
                                except:
                                    raise eg.Exception(
                                        "Can't open serial port."
                                    )
                                serial.baudrate = 9600
                                serial.timeout = 30.0
                                serial.setDTR(1)
                                serial.setRTS(1)
                                serial.port = int(prt.replace('COM', ''))

                                serial.open()

                                if value == 'On':
                                    serial.write(on)
                                else:
                                    serial.write(off)

                                if serial.read(6) == success:
                                    serial.write(success_reply)

                                serial.close()

                            def callback(signal, **_):
                                if signal == SIGNAL_NETWORK_STOP:

                                    send_command()
                                    ntwrk.start()

                                if signal in (
                                    SIGNAL_ALL_NODES_QUERIED,
                                    SIGNAL_ALL_NODES_QUERIED_SOME_DEAD
                                ):
                                    dispatcher.unset_redirect(network)

                            if ntwrk.state >= ntwrk.STATE_AWAKE:
                                dispatcher.set_redirect(network, callback)
                                ntwrk.stop()
                            else:
                                send_command()

                    self.SetSizer(main_sizer)

            devices = []
            notebook = panel.dialog.notebook

            for port in com_ports:
                if port in z_sticks:
                    for network in self.networks:
                        if network.com_port == port:
                            controller = network.controller.node
                            if (
                                controller.manufacturer_id == int('0x0086', 16)
                                and controller.product_id == int('0x005a', 16)
                            ):
                                display_led_ctrl = True
                            else:
                                display_led_ctrl = False

                            line = DeviceLine(
                                panel,
                                port,
                                True,
                                z_sticks[port]['name'],
                                z_sticks[port]['poll_interval'],
                                network,
                                display_led_ctrl
                            )

                            control_panel = zwave_admin.AdminPanel(
                                notebook,
                                network
                            )
                            notebook.AddPage(control_panel, str(port))
                            break
                    else:
                        line = DeviceLine(
                            panel,
                            port,
                            True,
                            z_sticks[port]['name'],
                            z_sticks[port]['poll_interval']
                        )
                else:
                    line = DeviceLine(
                        panel,
                        port,
                        False,
                        '',
                        0
                    )

                panel.sizer.Add(line, 0, wx.EXPAND | wx.ALL, 5)
                devices += [line]

            while panel.Affirmed():
                z_sticks = {}
                for device in devices:
                    if device.InUse():
                        port, name, poll_interval = device.GetValues()
                        z_sticks[port] = dict(
                            name=name,
                            poll_interval=poll_interval
                        )
                panel.SetResult(z_sticks)
        else:
            message, directions = update_core_files()

            panel.sizer.AddStretchSpacer(1)

            if message is not None:
                st = panel.StaticText(message)
                sizer = wx.BoxSizer(wx.HORIZONTAL)
                sizer.AddStretchSpacer(1)
                sizer.Add(st, 0, wx.EXPAND | wx.ALL, 20)
                panel.sizer.Add(sizer, 0, wx.EXPAND)

            if directions is not None:
                ctrl = panel.TextCtrl(
                    directions,
                    style=wx.TE_READONLY | wx.TE_MULTILINE
                )
                sizer = wx.BoxSizer(wx.HORIZONTAL)
                sizer.AddStretchSpacer(1)
                sizer.Add(ctrl, 0, wx.EXPAND | wx.ALL, 20)
                panel.sizer.Add(sizer, 0, wx.EXPAND)

            panel.sizer.AddStretchSpacer(1)

            if not z_sticks:
                wx.CallAfter(panel.dialog.buttonRow.okButton.Enable, True)

            while panel.Affirmed():
                panel.SetResult(dict())


def h_sizer(st, ctrl):
    sizer = wx.BoxSizer(wx.HORIZONTAL)
    sizer.Add(st, 0, wx.EXPAND | wx.ALL, 5)
    sizer.Add(ctrl, 0, wx.EXPAND | wx.ALL, 5)
    return sizer


# noinspection PyPep8Naming
class ZWavePanel(wx.Panel):

    def __init__(self, parent, networks, command_class=None):
        wx.Panel.__init__(self, parent, -1, style=wx.BORDER_NONE)

        self.networks = networks

        network_ctrl = wx.Choice(
            self,
            -1,
            choices=list(network.name for network in networks)
        )
        room_ctrl = wx.Choice(self, -1, choices=[])
        node_ctrl = wx.Choice(self, -1, choices=[])

        network_st = wx.StaticText(self, -1, 'Network:')
        room_st = wx.StaticText(self, -1, 'Room:')
        node_st = wx.StaticText(self, -1, 'Node:')

        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(h_sizer(network_st, network_ctrl))
        main_sizer.Add(h_sizer(room_st, room_ctrl))
        main_sizer.Add(h_sizer(node_st, node_ctrl))

        def get_static():
            if command_class is None:
                return network_st, room_st, node_st, prop_st
            else:
                return network_st, room_st, node_st

        self.GetStaticTexts = get_static

        def get_ctrls():
            if command_class is None:
                return network_ctrl, room_ctrl, node_ctrl, prop_ctrl
            else:
                return network_ctrl, room_ctrl, node_ctrl

        self.GetControls = get_ctrls

        def on_network(_):
            network_name = network_ctrl.GetStringSelection()
            choices = []
            for network in networks:
                if network.name == network_name:
                    for node in network.nodes.values():
                        try:
                            room = node.location
                        except AttributeError:
                            room = None

                        if not room:
                            room = 'Not Assigned'

                        if room not in choices:
                            choices += [room]
                    break

            room_ctrl.Clear()
            node_ctrl.Clear()
            if command_class is None:
                prop_ctrl.Clear()
            room_ctrl.AppendItems(choices)
            eg.EqualizeWidths(self.GetControls())

        def on_room(_):
            network_name = network_ctrl.GetStringSelection()
            room_name = room_ctrl.GetStringSelection()

            choices = []
            for network in networks:
                if network.name == network_name:
                    for node in network.nodes.values():
                        try:
                            room = node.location
                        except AttributeError:
                            room = None

                        if not room:
                            room = 'Not Assigned'

                        if room == room_name:
                            name = node.name
                            if not name:
                                name = node.object_id_str

                            if command_class is None or node == command_class:
                                choices += [name]
                    break

            node_ctrl.Clear()
            if command_class is None:
                prop_ctrl.Clear()
            node_ctrl.AppendItems(choices)
            eg.EqualizeWidths(self.GetControls())

        def on_node(_):
            node_name = node_ctrl.GetStringSelection()
            network_name = network_ctrl.GetStringSelection()
            choices = []
            for network in networks:
                if network.name == network_name:
                    for node in network.nodes.values():
                        if node_name in (node.name, node.object_id_str):
                            choices += ['Name']
                            try:
                                _ = node.location
                                choices += ['Room']
                            except AttributeError:
                                pass

                            if node.values.values():
                                choices += ['Poll', 'Poll Intensity']

                            for value in node.values.values():
                                choices += [value.label]
                            break

            prop_ctrl.Clear()
            prop_ctrl.AppendItems(choices)
            eg.EqualizeWidths(self.GetControls())

        network_ctrl.Bind(wx.EVT_CHOICE, on_network)
        room_ctrl.Bind(wx.EVT_CHOICE, on_room)
        if command_class is None:
            prop_ctrl = wx.Choice(self, -1, choices=[])
            prop_st = wx.StaticText(self, -1, 'Variable:')
            main_sizer.Add(h_sizer(prop_st, prop_ctrl))
            node_ctrl.Bind(wx.EVT_CHOICE, on_node)
            self.populate_prop = on_node
            self.prop_ctrl = prop_ctrl
        else:
            self.prop_ctrl = None

        self.populate_room = on_network
        self.populate_node = on_room

        self.network_ctrl = network_ctrl
        self.room_ctrl = room_ctrl
        self.node_ctrl = node_ctrl

        self.SetSizer(main_sizer)

    def GetValues(self):
        if self.prop_ctrl is None:
            return (
                self.network_ctrl.GetStringSelection(),
                self.room_ctrl.GetStringSelection(),
                self.node_ctrl.GetStringSelection()
            )
        else:
            return (
                self.network_ctrl.GetStringSelection(),
                self.room_ctrl.GetStringSelection(),
                self.node_ctrl.GetStringSelection(),
                self.prop_ctrl.GetStringSelection()
            )

    def SetNetwork(self, value):
        self.network_ctrl.SetStringSelection(value)
        self.populate_room(None)

    def SetRoom(self, value):
        self.room_ctrl.SetStringSelection(value)
        self.populate_node(None)

    def SetNode(self, value):
        self.node_ctrl.SetStringSelection(value)
        if self.prop_ctrl is not None:
            self.populate_prop(None)

    def SetProperty(self, value):
        if self.prop_ctrl is not None:
            self.prop_ctrl.SetStringSelection(value)


# noinspection PyPep8Naming,PyBroadException
class Set(eg.ActionBase):

    def __call__(self, network_name, room_name, node_name, prop_name, value):

        if isinstance(value, unicode):
            value = str(value)

        for network in self.plugin.networks:
            if network.name == network_name:
                break
        else:
            eg.PrintError('Z-Wave: Network not found.')
            return

        nodes = []
        found_room = False
        for node in network.nodes.values():
            try:
                room = node.location
            except AttributeError:
                room = None

            if not room:
                room = 'Not Assigned'

            if room == room_name:
                nodes += [node]
                found_room = True

        if not found_room:
            eg.PrintError('Z-Wave: Room not found.')
            return

        for node in nodes:
            if node_name in (node.name, node.object_id_str):
                break
        else:
            eg.PrintError('Z-Wave: Node not found.')
            return

        if prop_name == 'Name':
            node.name = value

        elif prop_name == 'Room':
            node.location = value

        elif prop_name == 'Poll Intensity':
            for prop in node.values.values():
                if value:
                    prop.enable_poll(value)
                else:
                    prop.disable_poll()

        elif prop_name == 'Poll':
            for prop in node.values.values():
                if value:
                    prop.enable_poll()
                else:
                    prop.disable_poll()

        else:
            for prop in node.values.values():
                if prop.label == prop_name:
                    break
            else:
                eg.PrintError('Z-Wave: Variable not found.')
                return

            prop.data = value

    def GetLabel(
        self,
        network_name=None,
        room_name=None,
        node_name=None,
        prop_name=None,
        value=None
    ):
        label = '{0}: {1}.{2}.{3}.{4} = {5}'
        return label.format(
            self.__class__.__name__,
            network_name,
            room_name,
            node_name,
            prop_name,
            value
        )

    def Configure(
        self,
        network=None,
        room=None,
        node=None,
        prop=None,
        value=None
    ):
        global value_sizer
        global value_ctrl
        global value_units

        # noinspection PyPep8Naming
        class ValueCtrl:
            @staticmethod
            def GetValue():
                return None

            @staticmethod
            def SetValue(_):
                pass

            @staticmethod
            def Destroy():
                pass

        value_ctrl = ValueCtrl
        value_units = None

        panel = eg.ConfigPanel()
        zwave_panel = ZWavePanel(panel, self.plugin.networks)
        value_st = panel.StaticText('New Value:')
        value_sizer = wx.BoxSizer(wx.HORIZONTAL)

        eg.EqualizeWidths(zwave_panel.GetStaticTexts() + (value_st,))
        eg.EqualizeWidths(zwave_panel.GetControls())

        value_sizer.Add(value_st, 0, wx.EXPAND | wx.ALL, 5)
        panel.sizer.Add(zwave_panel, 0, wx.EXPAND | wx.ALL, 5)
        panel.sizer.Add(value_sizer, 0, wx.EXPAND | wx.ALL, 5)

        def on_prop(evt):
            global value_sizer
            global value_ctrl
            global value_units

            value_ctrl.Destroy()
            if value_units is not None:
                value_units.Destroy()

            network_name, room_name, node_name, prop_name = (
                zwave_panel.GetValues()
            )

            for ntwrk in self.plugin.networks:
                if ntwrk.name == network_name:
                    break
            else:
                return

            nodes = []

            for nod in ntwrk.nodes.values():
                try:
                    rm = nod.location
                except AttributeError:
                    rm = None

                if not rm:
                    rm = 'No Room'

                if rm == room_name:
                    nodes += [nod]

            for nod in nodes:
                if node_name in (nod.object_id_str, nod.name):
                    break
            else:
                return

            if prop_name == 'Name':
                value_st.SetLabel('New Value:')
                value_units = None
                value_ctrl = panel.TextCtrl(value=nod.name)

            elif prop_name == 'Room':
                value_st.SetLabel('New Value:')
                value_units = None
                value_ctrl = panel.TextCtrl(value=nod.location)

            elif prop_name == 'Poll':
                values = node.values.values()
                if values:
                    prp = values[0]
                    value_st.SetLabel('New Value:')
                    value_ctrl = wx.CheckBox(panel, -1, '')
                    value_ctrl.SetValue(prp.is_polled)
                    value_ctrl.SetToolTipString(
                        'Enables or disabled polling for a node.\n'
                        'Enabling this will automatically sets the poll '
                        'intensity to 1'
                    )

            elif prop_name == 'Poll Intensity':
                values = nod.values.values()
                if values:
                    prp = values[0]

                    if prp.is_polled:
                        valu = prop.poll_intensity
                    else:
                        valu = 0

                    value_ctrl = panel.SpinIntCtrl(value=valu)
                    value_ctrl.SetToolTipString(
                        'Sets the poll intensity.\n'
                        'A setting of 0 disables polling for this node.\n'
                        'Each number above 0 is how many polling cycles have '
                        'to pass before this node is polled.\n'
                        '1 = every polling cycle, 2 = every other cycle...\n'
                        'Any setting above 0 will '
                        'enable polling for this node.'
                    )
            else:
                for prp in nod.values.values():
                    if prp.label == prop_name:
                        break
                else:
                    return

                if prp.is_read_only:
                    value_ctrl = panel.StaticText(str(prp.data))

                    value_st.SetLabel('Value:')

                    def get_value():
                        return None

                    value_ctrl.GetValue = get_value

                elif prp.type in (int, bytes):
                    value_st.SetLabel('New Value:')
                    max_val = prp.max
                    min_val = prp.min
                    if max_val == min_val:
                        max_val = None

                    if prp.is_write_only:
                        valu = min_val
                    else:
                        valu = prp.data

                    if valu < min_val:
                        valu = min_val

                    # noinspection PyPep8
                    try:
                        value_ctrl = panel.SpinIntCtrl(
                            max=max_val,
                            min=min_val,
                            value=valu
                        )
                        value_ctrl.numCtrl.SetToolTipString(prp.help)
                    except:
                        value_st.SetLabel('Value:')
                        value_ctrl = panel.StaticText(str(valu))
                        value_ctrl.SetToolTipString(prp.help)

                elif prp.type == float:
                    value_st.SetLabel('New Value:')
                    max_val = prp.max
                    min_val = prp.min
                    increment = prp.precision

                    if max_val == min_val:
                        max_val = None

                    if prp.is_write_only:
                        valu = min_val
                    else:
                        valu = prp.data

                    if valu < min_val:
                        valu = min_val

                    # noinspection PyPep8
                    try:
                        value_ctrl = panel.SpinIntCtrl(
                            max=max_val,
                            min=min_val,
                            value=valu,
                            increment=increment
                        )
                        value_ctrl.numCtrl.SetToolTipString(prp.help)
                    except:
                        value_st.SetLabel('Value:')
                        value_ctrl = panel.StaticText(str(valu))
                        value_ctrl.SetToolTipString(prp.help)

                elif prp.type == str:
                    value_st.SetLabel('New Value:')
                    if prp.is_write_only:
                        valu = ''
                    else:
                        valu = prp.data

                    value_ctrl = panel.TextCtrl(
                        value=valu
                    )

                elif prp.type == list:
                    value_st.SetLabel('New Value:')
                    value_ctrl = wx.Choice(
                        panel,
                        -1,
                        choices=list(item for item in prp)
                    )
                    if not prp.is_write_only:
                        value_ctrl.SetStringSelection(prp.data)
                    value_ctrl.GetValue = value_ctrl.GetStringSelection
                    value_ctrl.SetValue = value_ctrl.SetStringSelection

                else:
                    value_st.SetLabel('New Value:')
                    value_ctrl = wx.CheckBox(panel, -1, '')
                    if not prp.is_write_only:
                        value_ctrl.SetValue(prp.data)

                value_ctrl.SetToolTipString(prp.help)
                if prp.units:
                    value_units = panel.StaticText(prp.units)
                else:
                    value_units = None

            panel.sizer.Remove(value_sizer)
            value_sizer = wx.BoxSizer(wx.HORIZONTAL)
            value_sizer.Add(value_st, 0, wx.EXPAND | wx.ALL, 5)
            value_sizer.Add(value_ctrl, 0, wx.EXPAND | wx.ALL, 5)

            if value_units:
                value_sizer.Add(value_units, 0, wx.EXPAND | wx.ALL, 5)

            panel.sizer.Add(value_sizer, 0, wx.EXPAND | wx.ALL, 5)

            eg.EqualizeWidths(zwave_panel.GetControls() + (value_ctrl,))

            panel.sizer.Layout()
            panel.Refresh()
            panel.Update()

            if evt is not None:
                evt.Skip()

        if network:
            zwave_panel.SetNetwork(network)
            zwave_panel.SetRoom(room)
            zwave_panel.SetNode(node)
            zwave_panel.SetProperty(prop)
            on_prop(None)

            value_ctrl.SetValue(value)

        zwave_panel.Bind(wx.EVT_CHOICE, on_prop)

        while panel.Affirmed():
            network, room, node, prop = zwave_panel.GetValues()
            panel.SetResult(
                network,
                room,
                node,
                prop,
                value_ctrl.GetValue()
            )


# noinspection PyPep8Naming
class Get(eg.ActionBase):

    def __call__(self, network_name, room_name, node_name, prop_name):
        for network in self.plugin.networks:
            if network.name == network_name:
                break
        else:
            eg.PrintError('Z-Wave: Network not found.')
            return

        nodes = []
        found_room = False
        for node in network.nodes.values():
            try:
                room = node.location
            except AttributeError:
                room = None

            if not room:
                room = 'Not Assigned'

            if room == room_name:
                nodes += [node]
                found_room = True

        if not found_room:
            eg.PrintError('Z-Wave: Room not found.')
            return

        for node in nodes:
            if node_name in (node.name, node.object_id_str):
                break
        else:
            eg.PrintError('Z-Wave: Node not found.')
            return

        if prop_name == 'Name':
            return node.name

        elif prop_name == 'Room':
            try:
                room = node.location
            except AttributeError:
                room = None

            if not room:
                room = 'Not Assigned'

            return room

        elif prop_name == 'Poll Intensity':
            values = node.values.values()
            if values:
                prop = values[0]

                if prop.is_polled:
                    value = prop.poll_intensity
                else:
                    value = 0

                return value

        elif prop_name == 'Poll':
            values = node.values.values()
            if values:
                prop = values[0]

                return prop.is_polled

        else:
            for prop in node.values.values():
                if prop.label == prop_name:
                    break
            else:
                eg.PrintError('Z-Wave: Variable not found.')
                return
            return prop.data

    def GetLabel(
        self,
        network_name=None,
        room_name=None,
        node_name=None,
        prop_name=None
    ):
        label = '{0}: {1}.{2}.{3}.{4}'
        return label.format(
            self.__class__.__name__,
            network_name,
            room_name,
            node_name,
            prop_name
        )

    def Configure(self, network=None, room=None, node=None, prop=None):
        panel = eg.ConfigPanel()
        zwave_panel = ZWavePanel(panel, self.plugin.networks)

        eg.EqualizeWidths(zwave_panel.GetStaticTexts())
        eg.EqualizeWidths(zwave_panel.GetControls())

        if network is not None:
            zwave_panel.SetNetwork(network)
            zwave_panel.SetRoom(room)
            zwave_panel.SetNode(node)
            zwave_panel.SetProperty(prop)

        panel.sizer.Add(zwave_panel, 0, wx.EXPAND | wx.ALL, 5)

        while panel.Affirmed():
            panel.SetResult(
                *zwave_panel.GetValues()
            )


# noinspection PyPep8Naming
class RampDownDimmer(eg.ActionBase):
    name = 'Ramp Down Dimmer'

    def __call__(self, network_name, room_name, node_name, level, speed, step):
        import zwave_command_classes

        for network in self.plugin.networks:
            if network.name == network_name:
                break
        else:
            eg.PrintError('Z-Wave: Network not found.')
            return

        nodes = []
        found_room = False
        for node in network.nodes.values():
            try:
                room = node.location
            except AttributeError:
                room = None

            if not room:
                room = 'Not Assigned'

            if room == room_name:
                nodes += [node]
                found_room = True

        if not found_room:
            eg.PrintError('Z-Wave: Room not found.')
            return

        for node in nodes:
            if node_name in (node.name, node.object_id_str):
                break
        else:
            eg.PrintError('Z-Wave: Node not found.')
            return

        if node == zwave_command_classes.COMMAND_CLASS_SWITCH_MULTILEVEL:
            node.ramp_down(level, speed, step)

        else:
            eg.PrintError('Z-Wave: Node is not a dimmable light.')
            return

    def GetLabel(
        self,
        network_name=None,
        room_name=None,
        node_name=None,
        level=None,
        speed=None,
        step=None
    ):
        label = '{0}: {1}.{2}.{3}, {4}% {5}ms {6}%'
        return label.format(
            self.__class__.__name__,
            network_name,
            room_name,
            node_name,
            level,
            speed,
            step
        )

    def Configure(
        self,
        network=None,
        room=None,
        node=None,
        level=0,
        speed=0.17,
        step=1
    ):
        import zwave_command_classes

        panel = eg.ConfigPanel()
        zwave_panel = ZWavePanel(
            panel,
            self.plugin.networks,
            zwave_command_classes.COMMAND_CLASS_SWITCH_MULTILEVEL
        )

        level_st = panel.StaticText('Target level:')
        speed_st = panel.StaticText('Wait between increases:')
        step_st = panel.StaticText('Percentage increase:')

        level_ctrl = panel.SpinIntCtrl(value=level, min=0, max=99)
        speed_ctrl = panel.SpinNumCtrl(value=speed, increment=0.01, min=0.08)
        step_ctrl = panel.SpinIntCtrl(value=step, min=0, max=99)

        eg.EqualizeWidths(
            zwave_panel.GetStaticTexts() + (level_st, speed_st, step_st)
        )
        eg.EqualizeWidths(
            zwave_panel.GetControls() + (level_ctrl, speed_ctrl, step_ctrl)
        )

        if network is not None:
            zwave_panel.SetNetwork(network)
            zwave_panel.SetRoom(room)
            zwave_panel.SetNode(node)

        panel.sizer.Add(zwave_panel, 0, wx.EXPAND | wx.ALL, 5)

        panel.sizer.Add(h_sizer(level_st, level_ctrl))
        panel.sizer.Add(h_sizer(speed_st, speed_ctrl))
        panel.sizer.Add(h_sizer(step_st, step_ctrl))

        while panel.Affirmed():
            network, room, node = zwave_panel.GetValues()

            panel.SetResult(
                network,
                room,
                node,
                level_ctrl.GetValue(),
                speed_ctrl.GetValue(),
                step_ctrl.GetValue()
            )


# noinspection PyPep8Naming
class RampUpDimmer(eg.ActionBase):
    name = 'Ramp Up Dimmer'

    def __call__(self, network_name, room_name, node_name, level, speed, step):
        import zwave_command_classes

        for network in self.plugin.networks:
            if network.name == network_name:
                break
        else:
            eg.PrintError('Z-Wave: Network not found.')
            return

        nodes = []
        found_room = False
        for node in network.nodes.values():
            try:
                room = node.location
            except AttributeError:
                room = None

            if not room:
                room = 'Not Assigned'

            if room == room_name:
                nodes += [node]
                found_room = True

        if not found_room:
            eg.PrintError('Z-Wave: Room not found.')
            return

        for node in nodes:
            if node_name in (node.name, node.object_id_str):
                break
        else:
            eg.PrintError('Z-Wave: Node not found.')
            return

        if node == zwave_command_classes.COMMAND_CLASS_SWITCH_MULTILEVEL:
            node.ramp_up(level, speed, step)

        else:
            eg.PrintError('Z-Wave: Node is not a dimmable light.')
            return

    def GetLabel(
        self,
        network_name=None,
        room_name=None,
        node_name=None,
        level=None,
        speed=None,
        step=None
    ):
        label = '{0}: {1}.{2}.{3}, {4}% {5}ms {6}%'
        return label.format(
            self.__class__.__name__,
            network_name,
            room_name,
            node_name,
            level,
            speed,
            step
        )

    def Configure(
        self,
        network=None,
        room=None,
        node=None,
        level=0,
        speed=0.17,
        step=1.0
    ):
        import zwave_command_classes  # NOQA

        panel = eg.ConfigPanel()
        zwave_panel = ZWavePanel(
            panel,
            self.plugin.networks,
            zwave_command_classes.COMMAND_CLASS_SWITCH_MULTILEVEL
        )

        level_st = panel.StaticText('Target level:')
        speed_st = panel.StaticText('Wait between increases:')
        step_st = panel.StaticText('Percentage increase:')

        level_ctrl = panel.SpinIntCtrl(value=level, min=0, max=99)
        speed_ctrl = panel.SpinNumCtrl(value=speed, increment=0.01, min=0.08)
        step_ctrl = panel.SpinIntCtrl(value=step, min=0, max=99)

        eg.EqualizeWidths(
            zwave_panel.GetStaticTexts() + (level_st, speed_st, step_st))
        eg.EqualizeWidths(
            zwave_panel.GetControls() + (level_ctrl, speed_ctrl, step_ctrl))

        if network is not None:
            zwave_panel.SetNetwork(network)
            zwave_panel.SetRoom(room)
            zwave_panel.SetNode(node)

        panel.sizer.Add(zwave_panel, 0, wx.EXPAND | wx.ALL, 5)

        panel.sizer.Add(h_sizer(level_st, level_ctrl))
        panel.sizer.Add(h_sizer(speed_st, speed_ctrl))
        panel.sizer.Add(h_sizer(step_st, step_ctrl))

        while panel.Affirmed():
            network, room, node = zwave_panel.GetValues()

            panel.SetResult(
                network,
                room,
                node,
                level_ctrl.GetValue(),
                speed_ctrl.GetValue(),
                step_ctrl.GetValue()
            )


