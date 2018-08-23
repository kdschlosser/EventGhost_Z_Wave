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


# noinspection PyUnresolvedReferences
import eg
import wx
import dispatcher
import os
import threading
import zwave_utils
import site
from wx.lib.scrolledpanel import ScrolledPanel


LIBS_FOLDER = os.path.join(
    os.path.dirname(__file__),
    'libs'
)

site.addsitedir(LIBS_FOLDER)
NUMPY_LIBS = os.path.join(LIBS_FOLDER, 'numpy', '.libs')

if NUMPY_LIBS not in os.environ['PATH']:
    os.environ['PATH'] += NUMPY_LIBS + ';'

if eg.mainDir not in os.environ['PATH']:
    os.environ['PATH'] += eg.mainDir + ';'


def h_sizer(st, ctrl):
    sizer = wx.BoxSizer(wx.HORIZONTAL)
    sizer.Add(st, 0, wx.EXPAND | wx.ALL, 5)
    sizer.Add(ctrl, 0, wx.EXPAND | wx.ALL, 5)
    return sizer


class Config(eg.PersistentData):
    zoom = 0
    size = (1024, 768)
    pos = (-1, -1)
    image_viewer_size = (600, 600)
    image_viewer_position = wx.DefaultPosition


class ToolTips(object):
    plot = 'Draw a graphical representation of the network.'
    transfer_primary = 'Transfers the primary role to a secondary controller.'
    receive_sync = 'Receives controller data from the primary controller.'
    transmit_sync = (
        'Transmits primary controller data to a secondary controller.'
    )

    rebuild_mesh = (
        'Deletes the return routes on the network.\n'
        'The routes get rebuilt on an as needed basis.'
    )
    factory_reset = (
        'Factory Resets the Z-Stick\n'
        '***WARNING***\n'
        'This resets the z-wave network'
    )
    reboot = 'Reboots the Z-Stick'

    add_node = 'Puts the Z-Stick into "Add Node" mode.'
    remove_node = 'Puts the Z-Stick into "Remove Node" mode.'
    remove_failed_node = 'Removes a failed node from the network.'

    class ValuePanel(object):
        units = 'Unit of measure.'
        poll = (
            'Enables or disabled polling for a node.\n'
            'Enabling this will automatically sets the poll '
            'intensity to 1.'
        )
        poll_intensity = (
            'Sets the poll intensity.\n'
            'A setting of 0 disables polling for this node.\n'
            'Each number above 0 is how many polling cycles have '
            'to pass before this node is polled.\n'
            '  1 = every polling cycle\n'
            '  2 = every other cycle...\n'
            'Any setting above 0 will enable polling for this node.'
        )
        type = (
            'Data Type:\n'
            '  bool = Boolean, True/False\n'
            '  list = List of items, a grocery list\n'
            '  str = String of text, "Hello"\n'
            '  float = Floating point number, decimal number 0.0\n'
            '  int = Integer, whole number 1 2 3...'
        )

        min = 'Minimum allowed value.'
        max = 'Maximum allowed value.'
        read_only = 'Self explanatory.'
        write_only = 'Self explanatory.'


# noinspection PyPep8Naming
class NodePanel(ScrolledPanel):

    def __init__(self, parent, node, controller=False):
        ScrolledPanel.__init__(self, parent, -1, style=wx.BORDER_NONE)
        sizer = wx.BoxSizer(wx.VERTICAL)

        header_ctrl = HeaderPanel(
            self,
            node.name,
            node.id,
            '',
            ('Manufacturer', node.manufacturer_name),
            ('Model', node.product_name),
            ('Category', node.generic_as_str),
            ('Sub Category', node.specific_as_str),
            ('Basic Type', node.basic_as_str),
            ('Device Type', node.device_type_as_str),
            (
                'Command Classes',
                node.command_classes_as_str.replace(', ', ',\n')
            )
        )
        sizer.Add(header_ctrl, 0, wx.EXPAND | wx.ALL, 10)

        extra_st = ()
        extra_ctrl = ()

        if hasattr(node, 'location'):
            location = node.location
            if not location:
                location = 'No Room'
                node.location = str(location)
            room_st = wx.StaticText(self, -1, 'Room:')

            if controller:
                room_ctrl = wx.TextCtrl(
                    self,
                    -1,
                    node.location,
                    size=(len(node.location) * 15, -1),
                    style=wx.TE_READONLY
                )
            else:
                room_ctrl = wx.TextCtrl(
                    self,
                    -1,
                    node.location,
                    size=(len(node.location) * 15, -1)
                )
            sizer.Add(h_sizer(room_st, room_ctrl))
            extra_st += (room_st,)

        attrs = (
            'product_id'
            'product_type'
            'manufacturer_id'
            'version',
            'max_baud_rate',
            'is_listening_device',
            'is_beaming_device',
            'is_frequent_listening_device',
            'is_security_device',
            'is_routing_device',
            'is_zwave_plus',
            'is_locked',
            'is_sleeping',
            'is_awake',
            'is_failed',
            'is_ready',
            'is_info_received'
        )

        for attr in attrs:
            value = getattr(node, attr, None)
            if value is None:
                continue

            st = wx.StaticText(self, -1, attr.replace('_', ' ').title() + ':')
            ctrl = wx.StaticText(self, -1, str(value))
            sizer.Add(h_sizer(st, ctrl), 0, wx.EXPAND)
            extra_st += (st,)
            extra_ctrl += (ctrl,)

        role_st = wx.StaticText(self, -1, 'Role:')
        role_ctrl = wx.StaticText(self, -1, node.role_as_str)

        sizer.Add(h_sizer(role_st, role_ctrl), 0, wx.EXPAND)

        neighbors = ''

        for neighbor_id in node.neighbors:
            if neighbor_id == node.network.controller.node.id:
                neighbor = node.network.controller.node
            else:
                neighbor = node.network.nodes[neighbor_id]

            neighbors += (
                '          ' +
                neighbor.location +
                '.' +
                neighbor.name +
                ',\n'
            )

        neighbor_st = wx.StaticText(self, -1, 'Neighbors:')
        neighbor_ctrl = wx.StaticText(self, -1, 'None')

        if neighbors:
            neighbor_ctrl.SetLabel(neighbors[:-2])

        sizer.Add(h_sizer(neighbor_st, neighbor_ctrl), 0, wx.EXPAND)

        stats_st = wx.StaticText(self, -1, 'Statistics')
        font = stats_st.GetFont()
        font.SetPointSize(10)
        stats_st.SetFont(font)

        rule = wx.StaticLine(self, -1, size=(-1, 3))
        sizer.Add(stats_st, 0, wx.EXPAND | wx.ALL, 10)
        sizer.Add(rule, 0, wx.EXPAND | wx.BOTTOM, 15)

        stat_keys = (
            ('sentCnt', 'Number of messages sent from this node.'),
            ('sentFailed', 'Number of sent messages failed.'),
            ('retries', 'Number of message retries.'),
            ('receivedCnt', 'Number of messages received from this node.'),
            ('receivedDups', 'Number of duplicated messages received.'),
            (
                'receivedUnsolicited',
                'Number of messages received unsolicited.'
            ),
            ('lastRequestRTT', 'Last message request RTT.'),
            ('lastResponseRTT', 'Last message response RTT.'),
            ('sentTS', 'Last message sent time.'),
            ('receivedTS', 'Last message received time.'),
            ('averageRequestRTT', 'Average Request round trip time.'),
            ('averageResponseRTT', 'Average Response round trip time.'),
            ('quality', 'Node quality measure.'),
            ('lastReceivedMessage', 'Place to hold last received message.'),
            ('errors', 'Count errors for dead node detection.'),
        )

        stats = node.stats
        for key, tooltip in stat_keys:
            value = stats.get(key, None)
            if value is None:
                continue

            st = wx.StaticText(self, -1, key + ':')
            ctrl = wx.StaticText(self, -1, str(value))
            ctrl.SetToolTipString(tooltip)
            sizer.Add(h_sizer(st, ctrl))
            extra_st += (st,)
            extra_ctrl += (ctrl,)

        def on_apply():
            if not controller:
                try:
                    loc = str(room_ctrl.GetValue())
                    if not loc.strip():
                        loc = str('No Room')
                except NameError:
                    return
                node.location = loc
                parent.GetParent().move_location(node, loc)

        self.ApplyChanges = on_apply

        self.st = (neighbor_st, role_st) + extra_st
        eg.EqualizeWidths(self.st)

        self.ctrl = (neighbor_ctrl, role_ctrl) + extra_ctrl
        eg.EqualizeWidths(self.ctrl)

        self.SetSizer(sizer)
        self.SetupScrolling()
        self.SetLabel = header_ctrl.SetLabel

        self.header_ctrl = header_ctrl

        def on_size(evt):
            width = evt.GetSize()[0]
            for control in self.ctrl:
                if isinstance(control, wx.StaticText):
                    control.Wrap(width / 2)

            self.Layout()
            self.Update()

        self.Bind(wx.EVT_SIZE, on_size)

    def SetFontSize(self, delta):
        self.header_ctrl.SetFontSize(delta)
        for st in self.st:
            font = st.GetFont()
            point_size = font.GetPointSize()
            point_size += delta
            if point_size < 6:
                point_size = 6
            font.SetPointSize(point_size)
            st.SetFont(font)
            st.Refresh()
            st.Update()

        for ctrl in self.ctrl:
            font = ctrl.GetFont()
            point_size = font.GetPointSize()
            point_size += delta
            if point_size < 6:
                point_size = 6
            font.SetPointSize(point_size)
            ctrl.SetFont(font)
            ctrl.Refresh()
            ctrl.Update()

        eg.EqualizeWidths(self.st)
        eg.EqualizeWidths(self.ctrl)

        self.Layout()
        self.Refresh()
        self.Update()


# noinspection PyPep8Naming
class HeaderPanel(wx.Panel):

    # noinspection PyShadowingBuiltins
    def __init__(self, parent, label, id, network_id, *args):
        wx.Panel.__init__(self, parent, -1, style=wx.BORDER_SUNKEN)

        if not label:
            label = '0x' + hex(id)[2:].upper()

        label_st = wx.StaticText(self, -1, label)
        font = label_st.GetFont()
        font.SetPointSize(14)
        font.SetWeight(wx.FONTWEIGHT_BOLD)
        label_st.SetFont(font)

        id_st = wx.StaticText(self, -1, 'ID:')
        id_ctrl = wx.StaticText(self, -1, '0x' + hex(id)[2:].upper())

        network_st = wx.StaticText(self, -1, 'Network ID:')
        network_ctrl = wx.StaticText(self, -1, network_id)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(label_st, 0, wx.EXPAND | wx.ALL, 20)
        rule = wx.StaticLine(self, -1, size=(-1, 4))
        sizer.Add(rule, 0, wx.EXPAND)
        sizer.Add(h_sizer(id_st, id_ctrl), 0, wx.EXPAND)
        sizer.Add(h_sizer(network_st, network_ctrl), 0, wx.EXPAND)

        extra_ctrls = ()
        extra_sts = ()

        for key, value in args:
            st = wx.StaticText(self, -1, key + ':')
            ctrl = wx.StaticText(self, -1, str(value))
            sizer.Add(h_sizer(st, ctrl), 0, wx.EXPAND)
            extra_ctrls += (ctrl,)
            extra_sts += (st,)

        self.ctrl = (
            id_ctrl,
            network_ctrl
        ) + extra_ctrls

        self.st = (
            label_st,
            id_st,
            network_st
        ) + extra_sts

        self.SetSizer(sizer)
        self.SetLabel = label_st.SetLabel

        def on_size(evt):
            width = self.GetSizeTuple()[0]

            for control in extra_ctrls:
                control.Wrap(width / 4)
            self.Layout()
            self.Update()
            evt.Skip()

        self.Bind(wx.EVT_SIZE, on_size)

    def SetFontSize(self, delta):
        for st in self.st:
            font = st.GetFont()
            point_size = font.GetPointSize()
            point_size += delta
            if point_size < 6:
                point_size = 6
            font.SetPointSize(point_size)
            st.SetFont(font)
            st.Refresh()
            st.Update()

        for ctrl in self.ctrl:
            font = ctrl.GetFont()
            point_size = font.GetPointSize()
            point_size += delta
            if point_size < 6:
                point_size = 6
            font.SetPointSize(point_size)
            ctrl.SetFont(font)
            ctrl.Refresh()
            ctrl.Update()

        eg.EqualizeWidths(self.st)
        eg.EqualizeWidths(self.ctrl)

        self.Layout()
        self.Refresh()
        self.Update()


# noinspection PyPep8Naming,PyBroadException
class ValuePanel(ScrolledPanel):
    def __init__(self, parent, value):

        ScrolledPanel.__init__(self, parent, -1, style=wx.BORDER_NONE)
        sizer = wx.BoxSizer(wx.VERTICAL)

        self.SetBackgroundColour(parent.GetParent().GetBackgroundColour())

        # noinspection PyProtectedMember
        header_ctrl = HeaderPanel(
            self,
            value.label,
            value.id,
            value.id_on_network,
            ('Genre', value.genre),
            ('Index', value.index),
            ('Is Set', value.is_set),
            ('Command Class', value._commandClass)
        )

        sizer.Add(header_ctrl, 0, wx.EXPAND | wx.ALL, 10)

        extra_st = ()
        extra_ctrl = ()

        read_only_st = wx.StaticText(self, -1, 'Read Only:')
        read_only_ctrl = wx.StaticText(self, -1, str(value.is_read_only))
        read_only_ctrl.SetToolTipString(ToolTips.ValuePanel.read_only)

        write_only_st = wx.StaticText(self, -1, 'Write Only:')
        write_only_ctrl = wx.StaticText(self, -1, str(value.is_write_only))
        write_only_ctrl.SetToolTipString(ToolTips.ValuePanel.write_only)

        sizer.Add(h_sizer(read_only_st, read_only_ctrl), 0, wx.EXPAND)
        sizer.Add(h_sizer(write_only_st, write_only_ctrl), 0, wx.EXPAND)

        if value.units:
            units_st = wx.StaticText(self, -1, 'Unit of Measure:')
            units_ctrl = wx.TextCtrl(self, -1, value.units)
            units_ctrl.SetToolTipString(ToolTips.ValuePanel.units)
            sizer.Add(h_sizer(units_st, units_ctrl))
            extra_st += (units_st,)
            extra_ctrl += (units_ctrl,)

        type_st = wx.StaticText(self, -1, 'Data Type:')
        type_ctrl = wx.StaticText(self, -1, str(value.type)[7:-2])
        type_ctrl.SetToolTipString(ToolTips.ValuePanel.type)

        sizer.Add(h_sizer(type_st, type_ctrl))

        if value.type == int:
            min_st = wx.StaticText(self, -1, 'Data Minimum:')
            min_ctrl = wx.StaticText(self, -1, str(value.min))
            min_ctrl.SetToolTipString(ToolTips.ValuePanel.min)

            max_st = wx.StaticText(self, -1, 'Data Maximum:')
            max_ctrl = wx.StaticText(self, -1, str(value.max))
            max_ctrl.SetToolTipString(ToolTips.ValuePanel.max)

            sizer.Add(h_sizer(min_st, min_ctrl), 0, wx.EXPAND)
            sizer.Add(h_sizer(max_st, max_ctrl), 0, wx.EXPAND)

            extra_st += (min_st, max_st)
            extra_ctrl += (min_ctrl, max_ctrl)

        elif value.type == list:
            list_st = wx.StaticText(self, -1, 'Data Choices:')
            list_ctrl = wx.StaticText(
                self,
                -1,
                ', '.join(item for item in value)
            )
            list_ctrl.SetToolTipString('Available data choices.')
            sizer.Add(h_sizer(list_st, list_ctrl), 0, wx.EXPAND)
            extra_st += (list_st,)
            extra_ctrl += (list_ctrl,)

        poll_st = wx.StaticText(self, -1, 'Polling:')
        poll_ctrl = wx.CheckBox(self, -1, '')
        poll_ctrl.SetValue(value.is_polled)
        poll_ctrl.SetToolTipString(ToolTips.ValuePanel.poll)

        if value.is_polled:
            intensity = value.poll_intensity
        else:
            intensity = 0

        poll_inten_st = wx.StaticText(self, -1, 'Polling Intensity:')
        poll_inten_ctrl = eg.SpinIntCtrl(self, -1, value=intensity)
        poll_inten_ctrl.SetToolTipString(ToolTips.ValuePanel.poll_intensity)

        sizer.Add(h_sizer(poll_st, poll_ctrl), 0, wx.EXPAND)
        sizer.Add(h_sizer(poll_inten_st, poll_inten_ctrl), 0, wx.EXPAND)

        data_st = wx.StaticText(self, -1, 'Data:')

        if value.is_read_only:
            data_ctrl = wx.StaticText(self, -1, str(value.data))
            data_ctrl.SetToolTipString(value.help)

        elif value.type == int:
            max_val = value.max
            min_val = value.min

            if max_val == min_val:
                max_val = None

            if value.is_write_only:
                data = min_val

            else:
                data = value.data

            if data < min_val:
                data = min_val

            # noinspection PyPep8
            try:
                data_ctrl = eg.SpinIntCtrl(
                    self, -1,
                    max=max_val,
                    min=min_val,
                    value=data
                )
                data_ctrl.numCtrl.SetToolTipString(value.help)
            except:
                data_ctrl = wx.StaticText(self, -1, str(data))
                data_ctrl.SetToolTipString(value.help)

        elif value.type == float:
            increment = value.precision
            # noinspection PyPep8
            try:
                data_ctrl = eg.SpinIntCtrl(
                    self,
                    -1,
                    value=value.data,
                    increment=increment
                    )
                data_ctrl.numCtrl.SetToolTipString(value.help)
            except:
                data_ctrl = wx.StaticText(self, -1, str(value.data))
                data_ctrl.SetToolTipString(value.help)

        elif value.type == str:
            if value.is_write_only:
                data = ''
            else:
                data = value.data

            data_ctrl = wx.TextCtrl(self, -1, data)
            data_ctrl.SetToolTipString(value.help)

        elif value.type == list:
            data_ctrl = wx.Choice(
                self,
                -1,
                choices=list(item for item in value)
            )
            if not value.is_write_only:
                data_ctrl.SetStringSelection(value.data)

            data_ctrl.SetToolTipString(value.help)

        else:
            data_ctrl = wx.CheckBox(self, -1, '')
            if not value.is_write_only:
                data_ctrl.SetValue(value.data)

            data_ctrl.SetToolTipString(value.help)

        sizer.Add(h_sizer(data_st, data_ctrl), 0, wx.EXPAND)

        def on_poll_ctrl(_):
            if poll_ctrl.GetValue():
                poll_inten_ctrl.Enable(True)
                if not poll_inten_ctrl.GetValue():
                    poll_inten_ctrl.SetValue(1)
            else:
                poll_inten_ctrl.Enable(False)

        poll_ctrl.Bind(wx.EVT_CHECKBOX, on_poll_ctrl)

        on_poll_ctrl(None)

        def on_apply():
            if poll_ctrl.GetValue():
                if not poll_inten_ctrl.GetValue():
                    poll_inten_ctrl.SetValue(1)

                value.enable_poll(poll_inten_ctrl.GetValue())
            else:
                value.disable_poll()

            try:
                value.units = str(units_ctrl.GetValue())
            except NameError:
                pass

            if isinstance(data_ctrl, wx.Choice):
                value.data = str(data_ctrl.GetStringSelection())

            elif isinstance(data_ctrl, wx.TextCtrl):
                value.data = str(data_ctrl.GetValue())

            elif isinstance(
                data_ctrl,
                (eg.SpinNumCtrl, eg.SpinIntCtrl, wx.CheckBox)
            ):
                value.data = data_ctrl.GetValue()

        self.ApplyChanges = on_apply

        self.st = (
            read_only_st,
            write_only_st,
            type_st,
            poll_st,
            poll_inten_st,
            data_st,
        ) + extra_st

        eg.EqualizeWidths(self.st)

        self.ctrl = (
            read_only_ctrl,
            write_only_ctrl,
            type_ctrl,
            poll_ctrl,
            poll_inten_ctrl,
            data_ctrl
        ) + extra_ctrl

        eg.EqualizeWidths(self.ctrl)

        self.SetSizer(sizer)
        self.SetLabel = header_ctrl.SetLabel
        self.SetupScrolling()

        self.header_ctrl = header_ctrl

        def on_size(evt):
            width = evt.GetSize()[0]
            for control in self.ctrl:
                if isinstance(control, wx.StaticText):
                    control.Wrap(width / 2)

            self.Layout()
            self.Update()

        self.Bind(wx.EVT_SIZE, on_size)

    def SetFontSize(self, delta):
        self.header_ctrl.SetFontSize(delta)
        for st in self.st:
            font = st.GetFont()
            point_size = font.GetPointSize()
            point_size += delta
            if point_size < 6:
                point_size = 6
            font.SetPointSize(point_size)
            st.SetFont(font)
            st.Refresh()
            st.Update()

        for ctrl in self.ctrl:
            if isinstance(ctrl, eg.SpinNumCtrl):
                ctrl = ctrl.numCtrl

            font = ctrl.GetFont()
            point_size = font.GetPointSize()
            point_size += delta
            if point_size < 6:
                point_size = 6

            font.SetPointSize(point_size)
            ctrl.SetFont(font)
            ctrl.Refresh()
            ctrl.Update()

        eg.EqualizeWidths(self.st)
        eg.EqualizeWidths(self.ctrl)

        self.Layout()
        self.Refresh()
        self.Update()


# noinspection PyPep8Naming
class NetworkPanel(ScrolledPanel):
    def __init__(self, parent, network):
        ScrolledPanel.__init__(self, parent, -1, style=wx.BORDER_NONE)
        sizer = wx.BoxSizer(wx.VERTICAL)

        extra_st = ()
        extra_ctrl = ()

        controller = network.controller

        header_ctrl = HeaderPanel(
            self,
            network.name,
            network.home_id,
            '',
            ('Controller Name', controller.node.name),
            ('Controller ID', controller.node.object_id_str),
            ('Serial Port', controller.device),
            ('Network State', network.state_str),
            ('Library Version', controller.library_version),
            ('Z-Wave Library Version', controller.ozw_library_version),
        )

        sizer.Add(header_ctrl, 0, wx.EXPAND | wx.ALL, 10)

        type_st = wx.StaticText(self, -1, 'Library Type Name:')
        type_ctrl = wx.StaticText(
            self,
            -1,
            str(controller.library_type_name)
        )
        sizer.Add(h_sizer(type_st, type_ctrl), 0, wx.EXPAND)

        py_lib_st = wx.StaticText(self, -1, 'Python Library Version:')
        py_lib_ctrl = wx.StaticText(
            self,
            -1,
            str(controller.python_library_version)
        )
        sizer.Add(h_sizer(py_lib_st, py_lib_ctrl), 0, wx.EXPAND)

        flavor_st = wx.StaticText(self, -1, 'Python Library Flavor:')
        flavor_ctrl = wx.StaticText(
            self,
            -1,
            str(controller.python_library_flavor)
        )
        sizer.Add(h_sizer(flavor_st, flavor_ctrl), 0, wx.EXPAND)

        config_st = wx.StaticText(self, -1, 'Device Config Data:')
        config_ctrl = wx.StaticText(
            self,
            -1,
            str(controller.library_config_path)
        )
        sizer.Add(h_sizer(config_st, config_ctrl), 0, wx.EXPAND)

        user_st = wx.StaticText(self, -1, 'User Save Data:')
        user_ctrl = wx.StaticText(self, -1, str(controller.library_user_path))
        sizer.Add(h_sizer(user_st, user_ctrl), 0, wx.EXPAND)

        nodes_st = wx.StaticText(self, -1, 'Node Count:')
        nodes_ctrl = wx.StaticText(self, -1, str(network.nodes_count))
        sizer.Add(h_sizer(nodes_st, nodes_ctrl), 0, wx.EXPAND)

        sleep_st = wx.StaticText(self, -1, 'Sleeping Node Count:')
        sleep_ctrl = wx.StaticText(self, -1, str(network.sleeping_nodes_count))
        sizer.Add(h_sizer(sleep_st, sleep_ctrl), 0, wx.EXPAND)

        poll_st = wx.StaticText(self, -1, 'Poll Interval:')
        poll_ctrl = wx.StaticText(self, -1, str(network.get_poll_interval()))
        sizer.Add(h_sizer(poll_st, poll_ctrl), 0, wx.EXPAND)

        ready_st = wx.StaticText(self, -1, 'Is Ready:')
        ready_ctrl = wx.StaticText(self, -1, str(network.is_ready))
        sizer.Add(h_sizer(ready_st, ready_ctrl), 0, wx.EXPAND)

        attrs = (
            'is_primary_controller',
            'is_static_update_controller',
            'is_bridge_controller',
            'is_locked',
            'send_queue_count'
        )

        for attr in attrs:
            value = getattr(network.controller, attr, None)
            if value is None:
                continue
            st = wx.StaticText(self, -1, attr.replace('_', ' ').title() + ':')
            ctrl = wx.StaticText(self, -1, str(value))
            sizer.Add(h_sizer(st, ctrl), 0, wx.EXPAND)
            extra_st += (st,)
            extra_ctrl += (ctrl,)

        stats_st = wx.StaticText(self, -1, 'Statistics')
        font = stats_st.GetFont()
        font.SetPointSize(16)
        stats_st.SetFont(font)

        rule = wx.StaticLine(self, -1, size=(-1, 5))
        sizer.Add(stats_st, 0, wx.EXPAND | wx.ALL, 10)
        sizer.Add(rule, 0, wx.EXPAND | wx.BOTTOM, 15)

        stats = controller.stats

        stats_keys = (
            ('SOFCnt', 'SOF bytes received.'),
            ('ACKWaiting', 'Unsolicited messages while waiting for an ACK.'),
            ('readAborts', 'Times read were aborted due to timeouts.'),
            ('badChecksum', 'Bad checksums.'),
            ('readCnt', 'Messages successfully read.'),
            ('writeCnt', 'Messages successfully sent.'),
            ('CANCnt', 'CAN bytes received.'),
            ('NAKCnt', 'NAK bytes received.'),
            ('ACKCnt', 'ACK bytes received.'),
            ('OOFCnt', 'Bytes out of framing.'),
            ('dropped', 'Messages dropped & not delivered.'),
            ('retries', 'Messages retransmitted.'),
            ('controllerReadCnt', 'Controller messages read.'),
            ('controllerWriteCnt', 'Ccontroller messages sent.')
        )

        for key, tooltip in stats_keys:
            value = stats.get(key, None)
            if value is None:
                continue

            st = wx.StaticText(self, -1, key + ':')
            ctrl = wx.StaticText(self, -1, str(value))
            ctrl.SetToolTipString(tooltip)
            sizer.Add(h_sizer(st, ctrl), 0, wx.EXPAND)
            extra_st += (st,)
            extra_ctrl += (ctrl,)

        self.st = (
            type_st,
            py_lib_st,
            flavor_st,
            config_st,
            user_st,
            nodes_st,
            sleep_st,
            poll_st,
            ready_st
        ) + extra_st

        eg.EqualizeWidths(self.st)

        self.ctrl = (
            type_ctrl,
            py_lib_ctrl,
            flavor_ctrl,
            config_ctrl,
            user_ctrl,
            nodes_ctrl,
            sleep_ctrl,
            poll_ctrl,
            ready_ctrl
        ) + extra_ctrl

        eg.EqualizeWidths(self.ctrl)

        self.SetSizer(sizer)
        self.SetupScrolling()

        self.header_ctrl = header_ctrl

        def on_size(evt):
            width = evt.GetSize()[0]
            for control in self.ctrl:
                if isinstance(control, wx.StaticText):
                    control.Wrap(width / 2)

            self.Layout()
            self.Update()

        self.Bind(wx.EVT_SIZE, on_size)

        def on_apply():
            pass

        self.ApplyChanges = on_apply

    def SetFontSize(self, delta):
        self.header_ctrl.SetFontSize(delta)
        for st in self.st:
            font = st.GetFont()
            point_size = font.GetPointSize()
            point_size += delta
            if point_size < 6:
                point_size = 6

            font.SetPointSize(point_size)
            st.SetFont(font)
            st.Refresh()
            st.Update()

        for ctrl in self.ctrl:
            font = ctrl.GetFont()
            point_size = font.GetPointSize()
            point_size += delta
            if point_size < 6:
                point_size = 6
            font.SetPointSize(point_size)
            ctrl.SetFont(font)
            ctrl.Refresh()
            ctrl.Update()

        eg.EqualizeWidths(self.st)
        eg.EqualizeWidths(self.ctrl)

        self.Layout()
        self.Refresh()
        self.Update()


# noinspection PyPep8Naming
class Panel(wx.Panel):

    def __init__(self, parent, *_):
        wx.Panel.__init__(self, parent, -1, style=wx.NO_BORDER)

    def ApplyChanges(self):
        pass

    def SetFontSize(self, _):
        pass


class PlotFrame(wx.Frame):
    def __init__(self, network):
        self.network = network
        wx.Frame.__init__(
            self,
            None,
            title=network.name,
            size=Config.image_viewer_size,
            pos=Config.image_viewer_position
        )
        self._image = None
        self._cache = {}

        self.Centre()
        self.CreateStatusBar(4)
        self.SetStatusWidths([-1, 70, 50, 150])

        self.SetStatusText('Nodes: ' + str(len(network.nodes.values()) + 1), 0)

        self.cursor = wx.StockCursor(wx.CURSOR_ARROW)
        self.move_cursor = wx.StockCursor(wx.CURSOR_SIZING)
        self.factor = 1.0
        self.rotation = 0
        self.width = 0
        self.height = 0
        self.x = 0
        self.y = 0
        self.move_count = 0
        self.graph_nodes = None
        self.size = 0
        self.mc = False
        self.fs = False
        self.scroll_x = 0
        self.scroll_y = 0
        self.zoom_thread = None
        self.rotate_thread = None
        self.menu_bmp = None
        self.menu_lock = threading.Lock()
        self.menu_event = threading.Event()
        self.menu_pos = (0, 0)
        self.menu_id = None
        self.memory_error = False

        self.mode_choices = [
            'Nearest',
            'Antialias',
            'Bilinear',
            'Bicubic',
            'Box',
            'Hamming',
        ]
        self.mode = 1
        self.SetStatusText(
            'Resampling mode: ' + self.mode_choices[self.mode],
            3
        )

        self.Bind(wx.EVT_SIZE, self.on_size)
        self.Bind(wx.EVT_MOTION, self.on_move)
        self.Bind(wx.EVT_MOUSEWHEEL, self.on_wheel)
        self.Bind(wx.EVT_LEFT_DCLICK, self.on_d_click)
        self.Bind(wx.EVT_KEY_UP, self.on_key_up)
        self.Bind(wx.EVT_LEFT_UP, self.on_left_up)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.on_leave)
        self.SetBackgroundColour((0, 0, 0))

        self.Bind(wx.EVT_CLOSE, self.on_close)
        self.Bind(wx.EVT_WINDOW_DESTROY, self.on_close)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.on_erase_background)
        self.Bind(wx.EVT_PAINT, self.OnPaint)

        client_w, client_h = self.GetClientSizeTuple()
        bmp = wx.EmptyBitmap(client_w, client_h)
        dc = wx.MemoryDC()
        dc.SelectObject(bmp)
        font = self.GetFont()
        font.SetPointSize(16)

        gc = wx.GCDC(dc)
        gc.SetFont(font)
        gc.SetTextBackground(wx.Colour(0, 0, 0))
        gc.SetTextForeground(wx.Colour(0, 255, 0, 180))
        gc.SetPen(wx.Pen(wx.Colour(0, 0, 0), 1))
        gc.SetBrush(wx.Brush(wx.Colour(0, 0, 0)))

        gc.DrawRectangle(0, 0, client_w, client_h)

        line_w, line_h = gc.GetFullTextExtent('Please wait....')[:2]

        x = (client_w / 2) - line_w
        y = (client_h / 2) - line_h

        gc.DrawText('Please wait....', x, y)

        gc.Destroy()
        del gc
        dc.SelectObject(wx.EmptyBitmap(1, 1))
        dc.Destroy()
        del dc

        self._bmp = bmp

        self.Show()
        _ = self.image

    def on_size(self, _):
        self.process_picture(1.0)

    def on_erase_background(self, _):
        pass

    def on_close(self, evt):
        Config.image_viewer_size = self.GetSizeTuple()
        Config.image_viewer_position = self.GetPositionTuple()

        evt.Skip()

    @property
    def image(self):
        if self._image is None:
            import threading

            def do():
                from zwave_cord_diagram import Plot

                plot = Plot(self.network)
                self._image, self.graph_nodes = plot.image

                plot.close()

                del plot
                del Plot

                self.SetStatusText(
                    str(self._image.size[0]) + 'x' + str(self._image.size[1]),
                    1
                )
                self.process_picture(1.0)

            threading.Thread(target=do).start()

        return self._image

    @property
    def orig_image_size(self):
        return self._image.size

    def set_scroll(self, scroll_x, scroll_y):
        self.scroll_x += scroll_x
        self.scroll_y += scroll_y

        image_w, image_h = self._bmp.GetSize()

        if self.scroll_x < -image_w:
            self.scroll_x = -image_w
        elif self.scroll_x > image_w:
            self.scroll_x = image_w

        if self.scroll_y < -image_h:
            self.scroll_y = -image_h
        elif self.scroll_y > image_h:
            self.scroll_y = image_h

    @zwave_utils.thread_call_wait
    def process_picture(
        self,
        factor=None,
        mode=None,
        rotation=None,
        scroll_x=None,
        scroll_y=None,
        x=None,
        y=None,
    ):
        if self._image is None:
            return

        if scroll_x is not None or scroll_y is not None:
            self.set_scroll(scroll_x, scroll_y)
            self.hit_test_nodes()
            self.Refresh()
            self.Update()
            return

        if mode is not None:
            self.mode += mode
            if self.mode < 0:
                self.mode = 5
            if self.mode > 5:
                self.mode = 0

            self.SetStatusText(
                'Resampling mode: ' + self.mode_choices[self.mode],
                3
            )

        if rotation is not None:
            self.rotation += rotation

            if self.rotation > 359:
                self.rotation = 0
            elif self.rotation < 0:
                self.rotation = 359

        orig_w, orig_h = self.orig_image_size

        if factor is not None:
            if factor > 0:
                self.factor = factor * self.factor
            elif factor == 0.0:
                self.factor = 1.0

            last_width = self.width
            last_height = self.height

            win_x, win_y = self.image_box_size

            win_x -= 40
            win_y -= 40

            win_ratio = 1.0 * win_x / win_y
            img_ratio = 1.0 * orig_w / orig_h

            if img_ratio >= win_ratio:
                self.width = self.factor * win_x
                self.height = self.factor * win_x / img_ratio
            else:
                self.height = self.factor * win_y
                self.width = self.factor * win_y * img_ratio

            if int(self.width) <= 0:
                self.width = last_width

            if int(self.height) <= 0:
                self.height = last_height

        img = self.image

        try:
            img = img.resize((int(self.width), int(self.height)), self.mode)
            if self.rotation:
                if self.mode in (0, 2, 3):
                    rotate_mode = self.mode
                else:
                    rotate_mode = 0

                img = img.rotate(self.rotation, rotate_mode)

            last_w, last_h = self._bmp.GetSize()

            self.bmp = wx.BitmapFromBufferRGBA(
                img.size[0],
                img.size[1],
                str(img.tobytes())
            )

            new_w, new_h = self._bmp.GetSize()

            if None not in (x, y):
                scroll_x = int((float(x) * (float(new_w) / float(last_w))) - x)

                scroll_y = int((float(y) * (float(new_h) / float(last_h))) - y)

            else:
                scroll_x = int(
                    (
                        float(self.scroll_x) * (float(new_w) / float(last_w))
                    ) - self.scroll_x
                )
                scroll_y = int(
                    (
                        float(self.scroll_y) * (float(new_h) / float(last_h))
                    ) - self.scroll_y
                )

            if scroll_x != 0 or scroll_y != 0:
                self.set_scroll(scroll_x, scroll_y)

            self.memory_error = False

        except MemoryError:
            self.memory_error = True
            self.Refresh()
            self.Update()
            return

        label = str(int(100 * self.width / orig_w))
        self.SetStatusText(label + '%', 2)

        self.hit_test_nodes()

        self.Refresh()
        self.Update()

    @property
    def bmp(self):
        bmp_w, bmp_h = self._bmp.GetSize()

        client_w, client_h = self.image_box_size
        wx_bmp = wx.EmptyBitmap(client_w, client_h)

        if bmp_w < client_w:
            pos_x = (client_w - bmp_w) / 2
        else:
            pos_x = 0

        pos_x -= self.scroll_x

        if bmp_h < client_h:
            pos_y = (client_h - bmp_h) / 2
        else:
            pos_y = 0

        pos_y -= self.scroll_y

        dc = wx.MemoryDC()
        dc.SelectObject(wx_bmp)
        dc.SetPen(wx.Pen(wx.Colour(0, 0, 0), 1))
        dc.SetBrush(wx.Brush(wx.Colour(0, 0, 0)))
        dc.DrawRectangle(0, 0, client_w, client_h)

        gc = wx.GCDC(dc)
        gc.DrawBitmap(self._bmp, pos_x, pos_y)
        if self.memory_error:
            gc.SetTextForeground(wx.Colour(255, 0, 0))
            gc.SetTextBackground(wx.Colour(0, 0, 0, 0))
            font = self.GetFont()
            font.SetPointSize(20)
            gc.SetFont(font)

            text_w, text_h = gc.GetFullTextExtent('INSUFFICIENT MEMORY')[:2]

            text_x = (client_w - text_w) / 2
            text_y = (client_h - text_h) / 2

            gc.DrawText('INSUFFICIENT MEMORY', text_x, text_y)

        dc.SelectObject(wx.EmptyBitmap(1, 1))

        gc.Destroy()
        del gc

        dc.Destroy()
        del dc

        return wx_bmp

    @bmp.setter
    def bmp(self, bmp):
        self._bmp = bmp

    # noinspection PyMethodOverriding
    def OnPaint(self, _):
        bmp = self.bmp
        dc = wx.PaintDC(self)
        # dc.Clear()
        # dc.SetPen(wx.Pen(wx.Colour(0, 0, 0), 1))
        # dc.SetBrush(wx.Brush(wx.Colour(0, 0, 0)))
        # dc.DrawRectangle(0, 0, *self.image_box_size)

        gc = wx.GCDC(dc)

        gc.DrawBitmap(bmp, 0, 0)

        if self.menu_bmp is not None:
            gc.DrawBitmap(self.menu_bmp, *self.menu_pos)

        gc.Destroy()
        del gc

    def on_wheel(self, evt):
        self.x = evt.GetX()
        self.y = evt.GetY()

        if evt.LeftIsDown():
            if evt.GetWheelRotation() > 0:
                delta = 1
            else:
                delta = -1

            self.process_picture(mode=delta)

        elif evt.RightIsDown():
            if evt.GetWheelRotation() > 0:
                delta = 10
            else:
                delta = -10

            if self.rotate_thread is None or not self.rotate_thread.isAlive():
                self.rotate_thread = self.process_picture(rotation=delta)
        else:
            if evt.GetWheelRotation() > 0:
                factor = 1.02
            else:
                factor = 0.98

            if self.zoom_thread is None or not self.zoom_thread.isAlive():
                current_x = evt.GetX() + self.scroll_x
                current_y = evt.GetY() + self.scroll_y

                self.zoom_thread = self.process_picture(
                    factor,
                    x=current_x,
                    y=current_y
                )

    def on_key_up(self, evt):
        code = evt.GetKeyCode()

        if wx.WXK_NUMPAD0 >= code <= wx.WXK_NUMPAD9:
            factor = zwave_utils.remap(
                float(code),
                float(wx.WXK_NUMPAD0),
                float(wx.WXK_NUMPAD9),
                0.50,
                1.50
            )
            self.process_picture(factor)

        elif ord('0') >= code <= ord('9'):
            factor = zwave_utils.remap(
                float(code),
                float(ord('0')),
                float(ord('9')),
                0.50,
                1.50
            )
            self.process_picture(factor)

        elif code in (wx.WXK_HOME, wx.WXK_NUMPAD_HOME):
            self.process_picture(0.0)

        elif code == wx.WXK_ESCAPE:
            self.process_picture(0.0, rotation=-self.rotation)

        # plus   --   zoom in
        elif code in (wx.WXK_ADD, wx.WXK_NUMPAD_ADD):
            self.process_picture(1.05)

        # minus   --   zoom out
        elif code in (wx.WXK_SUBTRACT, wx.WXK_NUMPAD_SUBTRACT):
            self.process_picture(0.95)
        # less than   --   rotate left
        elif code == ord(','):
            self.process_picture(rotation=-30)

        # greater than   --   rotate right
        elif code == ord('.'):
            self.process_picture(rotation=30)

        # f   --   full screen
        elif code == ord('f'): # f
            wx.CallAfter(self.ShowFullScreen, not self.IsFullScreen())

        # left, up, right, down   --   panning
        elif code in (
            wx.WXK_NUMPAD_LEFT,
            wx.WXK_NUMPAD_UP,
            wx.WXK_NUMPAD_RIGHT,
            wx.WXK_NUMPAD_DOWN,
            wx.WXK_LEFT,
            wx.WXK_UP,
            wx.WXK_RIGHT,
            wx.WXK_DOWN,

        ):
            self.scroll(code)
        # m   --   mode
        elif code == ord('m'):
            self.process_picture(mode=1)
        evt.Skip()

    @property
    def image_box_pos(self):
        return self.GetScreenPositionTuple()

    @property
    def image_box_size(self):
        return self.GetClientSizeTuple()

    @property
    def image_ctrl_pos(self):
        pos_x, pos_y = self.image_box_pos
        return pos_x - self.scroll_x, pos_y - self.scroll_y

    @property
    def image_ctrl_size(self):
        return self.width, self.height

    def scroll(self, code):
        if code in (wx.WXK_NUMPAD_UP, wx.WXK_UP):
            delta = (0, -20)
        elif code in (wx.WXK_NUMPAD_DOWN, wx.WXK_DOWN):
            delta = (0, 20)
        elif code in (wx.WXK_NUMPAD_LEFT, wx.WXK_LEFT):
            delta = (-20, 0)
        elif code in (wx.WXK_NUMPAD_RIGHT, wx.WXK_RIGHT):
            delta = (20, 0)
        else:
            return

        self.scroll_image(*delta)

    def scroll_image(self, x, y):
        self.process_picture(scroll_x=x, scroll_y=y)

    def on_d_click(self, _):
        wx.CallAfter(self.ShowFullScreen, not self.IsFullScreen())

    def on_move(self, evt):
        if evt.LeftIsDown():
            if not self.mc:
                self.SetCursor(self.move_cursor)
                self.mc = True

            if self.move_count == 0:
                self.x = evt.GetX()
                self.y = evt.GetY()

            self.move_count = self.move_count + 1

            if self.move_count > 1:
                self.move_count = 0
                self.scroll_image(
                    -(evt.GetX() - self.x) * 5.5,
                    -(evt.GetY() - self.y) * 5.5
                )
                self.x = evt.GetX()
                self.y = evt.GetY()
        else:
            self.on_left_up(None)
            self.x = evt.GetX()
            self.y = evt.GetY()
            self.hit_test_nodes()

    def hit_test_nodes(self):
        if self.graph_nodes is None:
            return

        x = self.x
        y = self.y

        client_w, client_h = self.image_box_size
        image_w, image_h = self._bmp.GetSize()

        if client_w > image_w:
            x -= (client_w - image_w) / 2
        x += self.scroll_x

        if client_h > image_h:
            y -= (client_h - image_h) / 2
        y += self.scroll_y

        for node in self.graph_nodes:
            if node.id == self.menu_id:
                if node.hit_test(
                    x,
                    y,
                    -self.rotation,
                    *self._bmp.GetSize()
                ):
                    pos_x = self.x
                    pos_y = self.y
                    break

            if node.id != self.menu_id:
                if not node.hit_test(
                    x,
                    y,
                    -self.rotation,
                    *self._bmp.GetSize()
                ):
                    continue

                self.menu_id = node.id
                self.menu_event.set()

                pos_x = self.x
                pos_y = self.y

                # noinspection PyShadowingNames
                def build_menu(n):
                    try:
                        with self.menu_lock:
                            self.menu_event.clear()
                            self.menu_event.wait(0.5)
                            if self.menu_event.isSet():
                                return

                            dc = wx.MemoryDC()
                            dc.SetFont(self.GetFont())

                            node_id = 'Node id - ' + n.node.object_id_str
                            neighbor_text = [node_id]
                            if n.index != 0:
                                num_routes = 'Routes: ' + str(n.num_routes)
                                neighbor_text += [num_routes]

                            neighbor_text += ['---------']
                            label_w, label_h = dc.GetTextExtent('G')
                            height = (
                                4 + ((label_h + 4) * len(neighbor_text))
                            )
                            width = len(node_id) * label_w

                            colors = [(0, 255, 0)] * len(neighbor_text)
                            for neighbor in n.neighbors:
                                if neighbor is None:
                                    continue

                                name = neighbor.name
                                room = neighbor.room
                                label = '{0} {1} ({2})'.format(
                                    room,
                                    name,
                                    neighbor.node.object_id_str
                                )

                                width = max(width, label_w * len(label))
                                height += label_h + 4
                                neighbor_text += [label]
                                colors += [neighbor.color]

                            width += 4

                            bmp = wx.EmptyBitmapRGBA(
                                width,
                                height,
                                0,
                                0,
                                0,
                                0
                            )
                            dc.SelectObject(bmp)
                            gc = wx.GCDC(dc)

                            gc.SetTextBackground(wx.Colour(0, 0, 0, 0))
                            gc.SetPen(wx.Pen(wx.Colour(0, 0, 255, 255), 3))
                            gc.SetBrush(wx.Brush(wx.Colour(0, 0, 0, 180)))

                            text_x = 4
                            text_y = 4

                            gc.DrawRoundedRectangle(0, 0, width, height, 5)

                            for i, text in enumerate(neighbor_text):
                                gc.SetTextForeground(wx.Colour(*colors[i]))
                                gc.DrawText(text, text_x, text_y)
                                text_y += label_h + 4

                            gc.Destroy()
                            del gc

                            dc.SelectObject(wx.EmptyBitmap(1, 1))
                            dc.Destroy()
                            del dc

                            client_w, client_h = self.image_box_size
                            p_x = pos_x
                            p_y = pos_y

                            if p_x + width > client_w:
                                p_x -= width

                            if p_y + height > client_h:
                                p_y -= height

                            self.menu_pos = (p_x, p_y)
                            self.menu_bmp = bmp
                            self.Refresh()
                            self.Update()
                    except wx.PyDeadObjectError:
                        pass

                threading.Thread(
                    target=build_menu,
                    args=(node,)
                ).start()

                break
        else:
            self.menu_id = None
            self.menu_bmp = None
            self.Refresh()
            self.Update()

    def on_leave(self, _):
        self.on_left_up(None)

    def on_left_up(self, _):
        self.move_count = 0
        self.SetCursor(self.cursor)
        self.mc = False


# noinspection PyPep8Naming
class AdminPanel(wx.Panel):

    def __init__(self, parent, network):
        self.parent = parent
        self.zoom_steps = Config.zoom

        self.network = network
        wx.Panel.__init__(self, parent, -1, style=wx.BORDER_RAISED)

        splitter_window = wx.SplitterWindow(self, -1, style=wx.SP_3D)

        tree_ctrl = wx.TreeCtrl(
            splitter_window,
            -1,
            style=(
                wx.TR_EDIT_LABELS |
                wx.TR_HAS_BUTTONS |
                wx.TR_TWIST_BUTTONS |
                wx.TR_ROW_LINES
            )
        )
        self.old_item_label = ''
        self._options_panel = None
        self.options_panel = Panel(splitter_window, None)

        transfer_primary_btn = wx.Button(self, -1, 'Transfer Primary')
        receive_sync_btn = wx.Button(self, -1, 'Sync Receive')
        transmit_sync_btn = wx.Button(self, -1, 'Sync Transmit')

        rebuild_mesh_btn = wx.Button(self, -1, 'Rebuild Network')
        factory_reset_btn = wx.Button(self, -1, 'Factory Reset')
        reboot_btn = wx.Button(self, -1, 'Reboot Z-Stick')

        plot_btn = wx.Button(self, -1, 'Graph Network')
        add_node_btn = wx.Button(self, -1, 'Add Node')
        remove_node_btn = wx.Button(self, -1, 'Remove Node')
        remove_failed_node_btn = wx.Button(self, -1, 'Remove Failed Node')
        apply_btn = wx.Button(self, -1, 'Apply Changes')

        transfer_primary_btn.SetToolTipString(ToolTips.transfer_primary)
        receive_sync_btn.SetToolTipString(ToolTips.receive_sync)
        transmit_sync_btn.SetToolTipString(ToolTips.transmit_sync)

        rebuild_mesh_btn.SetToolTipString(ToolTips.rebuild_mesh)
        factory_reset_btn.SetToolTipString(ToolTips.factory_reset)
        reboot_btn.SetToolTipString(ToolTips.reboot)

        plot_btn.SetToolTipString(ToolTips.plot)
        add_node_btn.SetToolTipString(ToolTips.add_node)
        remove_node_btn.SetToolTipString(ToolTips.remove_node)
        remove_failed_node_btn.SetToolTipString(ToolTips.remove_failed_node)

        transfer_primary_btn.Bind(wx.EVT_BUTTON, self.on_transfer_primary)
        receive_sync_btn.Bind(wx.EVT_BUTTON, self.on_receive_controller_info)
        transmit_sync_btn.Bind(wx.EVT_BUTTON, self.on_send_controller_info)

        rebuild_mesh_btn.Bind(wx.EVT_BUTTON, self.on_rebuild_mesh)
        factory_reset_btn.Bind(wx.EVT_BUTTON, self.on_factory_reset)
        reboot_btn.Bind(wx.EVT_BUTTON, self.on_reboot)

        plot_btn.Bind(wx.EVT_BUTTON, self.on_plot)
        add_node_btn.Bind(wx.EVT_BUTTON, self.on_add_node)
        remove_node_btn.Bind(wx.EVT_BUTTON, self.on_remove_node)
        remove_failed_node_btn.Bind(wx.EVT_BUTTON, self.on_remove_failed_node)
        apply_btn.Bind(wx.EVT_BUTTON, self.on_apply)

        tree_ctrl.Bind(wx.EVT_TREE_SEL_CHANGED, self.on_selection_changed)
        tree_ctrl.Bind(wx.EVT_TREE_BEGIN_LABEL_EDIT, self.on_start_edit_label)
        tree_ctrl.Bind(wx.EVT_TREE_END_LABEL_EDIT, self.on_end_edit_label)

        remove_failed_node_btn.Enable(False)
        if network.controller.is_primary_controller:
            receive_sync_btn.Enable(False)
        else:
            transmit_sync_btn.Enable(False)
            transfer_primary_btn.Enable(False)

        splitter_window.SplitVertically(tree_ctrl, self.options_panel)
        splitter_window.SetSashPosition(self.GetSizeTuple()[0] * 7)

        sizer = wx.BoxSizer(wx.VERTICAL)
        top_sizer = wx.BoxSizer(wx.HORIZONTAL)
        bottom_sizer = wx.BoxSizer(wx.HORIZONTAL)
        left_sizer = wx.BoxSizer(wx.VERTICAL)

        left_sizer.AddStretchSpacer(1)
        left_sizer.Add(transfer_primary_btn, 0, wx.ALL, 5)
        left_sizer.Add(receive_sync_btn, 0, wx.ALL, 5)
        left_sizer.Add(transmit_sync_btn, 0, wx.ALL, 5)
        left_sizer.AddStretchSpacer(1)
        left_sizer.Add(rebuild_mesh_btn, 0, wx.ALL, 5)
        left_sizer.Add(factory_reset_btn, 0, wx.ALL, 5)
        left_sizer.Add(reboot_btn, 0, wx.ALL, 5)
        left_sizer.AddStretchSpacer(1)

        bottom_sizer.AddStretchSpacer(1)
        bottom_sizer.Add(plot_btn, 0, wx.ALL, 5)
        bottom_sizer.AddStretchSpacer(1)
        bottom_sizer.Add(add_node_btn, 0, wx.ALL, 5)
        bottom_sizer.Add(remove_node_btn, 0, wx.ALL, 5)
        bottom_sizer.Add(remove_failed_node_btn, 0, wx.ALL, 5)
        bottom_sizer.AddStretchSpacer(1)
        bottom_sizer.Add(apply_btn, 0, wx.ALL, 5)
        bottom_sizer.AddStretchSpacer(1)

        top_sizer.Add(left_sizer, 0, wx.EXPAND)
        top_sizer.Add(splitter_window, 1, wx.EXPAND | wx.ALL, 10)
        sizer.Add(top_sizer, 1, wx.EXPAND)
        sizer.Add(bottom_sizer, 0, wx.EXPAND)

        from . import zwave_network

        dispatcher.connect(
            self.signal_remove_node,
            zwave_network.ZWaveNetwork.SIGNAL_NODE_REMOVED
        )
        dispatcher.connect(
            self.signal_add_node,
            zwave_network.ZWaveNetwork.SIGNAL_NODE_ADDED
        )
        dispatcher.connect(
            self.signal_add_node,
            zwave_network.ZWaveNetwork.SIGNAL_NODE_NEW
        )
        self.tree_ctrl = tree_ctrl
        self.splitter_window = splitter_window
        self.remove_failed_node_btn = remove_failed_node_btn
        self.plot_btn = plot_btn
        self.plot_frame = None
        self.load_tree()
        self.SetSizer(sizer)
        self.tree_ctrl.Bind(wx.EVT_CHAR_HOOK, self.on_key)

        font = self.tree_ctrl.GetFont()
        point_size = font.GetPointSize()
        point_size += self.zoom_steps * 2
        if point_size < 6:
            point_size = 6

        font.SetPointSize(point_size)
        self.tree_ctrl.SetFont(font)

        parent.GetParent().Bind(wx.EVT_CLOSE, self.on_close)

        def do():
            parent.GetParent().SetSize(Config.size)

            if Config.pos is not None:
                parent.GetParent().SetPosition(Config.pos)

        wx.CallAfter(do)

    @property
    def options_panel(self):
        return self._options_panel

    @options_panel.setter
    def options_panel(self, panel):
        panel.Bind(wx.EVT_CHAR_HOOK, self.on_key)
        zoom = self.zoom_steps * 2
        if zoom:
            panel.SetFontSize(zoom)
        self._options_panel = panel

    def on_key(self, evt):
        key_code = evt.GetKeyCode()

        if (
            wx.GetKeyState(wx.WXK_CONTROL) and
            key_code != wx.WXK_CONTROL and
            key_code in (wx.WXK_NUMPAD_ADD, wx.WXK_NUMPAD_SUBTRACT)
        ):
            font = self.tree_ctrl.GetFont()
            point_size = font.GetPointSize()

            if key_code == wx.WXK_NUMPAD_ADD:
                self.zoom_steps += 1
                delta = 2
            else:
                self.zoom_steps -= 1
                delta = -2

            point_size += delta
            if point_size < 6:
                point_size = 6

            font.SetPointSize(point_size)
            self.options_panel.SetFontSize(delta)
            self.tree_ctrl.SetFont(font)
            self.Refresh()
            self.Update()
        else:
            evt.Skip()

    def on_plot(self, _):
        if self.plot_frame is None:
            self.plot_frame = PlotFrame(self.network)

            def on_destroy(_):
                self.plot_btn.Enable()
                self.plot_frame = None

            self.plot_frame.Bind(wx.EVT_WINDOW_DESTROY, on_destroy)
            self.plot_frame.Show()
        else:
            self.plot_frame.Raise()

    def on_apply(self, _):
        self.options_panel.ApplyChanges()

    def on_start_edit_label(self, evt):
        item_id = evt.GetItem()

        data = self.tree_ctrl.GetPyData(item_id)
        if not data['panel'] in (NodePanel, Panel) or 'controller' in data:
            evt.Veto()

        self.old_item_label = self.tree_ctrl.GetItemText(item_id)

    def on_end_edit_label(self, evt):
        """
        Handles wx.EVT_TREE_END_LABEL_EDIT
        """
        if evt.IsEditCancelled():
            return

        item_id = evt.GetItem()
        data = self.tree_ctrl.GetPyData(item_id)
        new_label = str(evt.GetLabel())
        obj = data['obj']
        panel = data['panel']

        if panel == ValuePanel:
            if not new_label.strip():
                self.tree_ctrl.SetItemText(item_id, self.old_item_label)
                return

            obj.label = new_label
            if self.tree_ctrl.GetSelection() == item_id:
                self.options_panel.SetLabel(new_label)

        elif panel == NodePanel:
            if not new_label.strip():
                self.tree_ctrl.SetItemText(item_id, self.old_item_label)
                return
            obj.name = new_label
            if self.tree_ctrl.GetSelection() == item_id:
                self.options_panel.SetLabel(new_label)
        else:
            if not new_label.strip():
                new_label = str('No Room')
                self.tree_ctrl.SetItemText(item_id, new_label)
            nodes = {}
            self.get_nodes(item_id, nodes)

            for node in data['nodes']:
                try:
                    node.location = new_label
                    if self.tree_ctrl.GetSelection() == nodes[node]:
                        self.options_panel.SetLabel(new_label)
                except AttributeError:
                    pass

    def clear_node_from_room(self, item_id, node):
        parent_id = self.tree_ctrl.GetItemParent(item_id)
        parent_data = self.tree_ctrl.GetPyData(parent_id)
        parent_data['nodes'].remove(node)
        if not parent_data['nodes']:
            self.tree_ctrl.DeleteChildren(parent_id)
            self.tree_ctrl.Delete(parent_id)
            return False

        self.tree_ctrl.SetPyData(
            parent_id,
            parent_data
        )
        return True

    def move_location(self, node, location):
        root = self.tree_ctrl.GetRootItem()
        nodes = {}
        self.get_nodes(root, nodes)

        item_id = nodes[node]

        child_id, cookie = self.tree_ctrl.GetFirstChild(root)

        while child_id.IsOk():
            room_name = self.tree_ctrl.GetItemText(child_id)
            if room_name == location:
                child_id = self.add_node(child_id, node)
                self.tree_ctrl.SelectItem(child_id)

                if self.clear_node_from_room(item_id, node):
                    self.tree_ctrl.DeleteChildren(item_id)
                    self.tree_ctrl.Delete(item_id)
                return

            child_id, cookie = self.tree_ctrl.GetNextChild(child_id, cookie)

        parent_id = self.tree_ctrl.AppendItem(root, location)
        self.tree_ctrl.SetPyData(
            parent_id,
            dict(obj=None, panel=Panel, nodes=[])
        )

        child_id = self.add_node(parent_id, node)
        self.tree_ctrl.SelectItem(child_id)
        if self.clear_node_from_room(item_id, node):
            self.tree_ctrl.DeleteChildren(item_id)
            self.tree_ctrl.Delete(item_id)

    def on_close(self, evt=None):
        Config.pos = self.parent.GetParent().GetPositionTuple()
        Config.size = self.parent.GetParent().GetSizeTuple()
        Config.zoom = self.zoom_steps

        import zwave_network

        dispatcher.disconnect(
            self.signal_remove_node,
            zwave_network.ZWaveNetwork.SIGNAL_NODE_REMOVED
        )
        dispatcher.disconnect(
            self.signal_add_node,
            zwave_network.ZWaveNetwork.SIGNAL_NODE_ADDED
        )
        dispatcher.disconnect(
            self.signal_add_node,
            zwave_network.ZWaveNetwork.SIGNAL_NODE_NEW
        )

        if self.plot_frame is not None:
            self.plot_frame.Hide()
            self.plot_frame.Destroy()

        if evt is not None:
            evt.Skip()

    # noinspection PyMethodOverriding
    def Destroy(self):
        self.on_close(None)
        wx.Panel.Destroy(self)

    def load_tree(self):
        panel = Panel(self.splitter_window, None)

        self.options_panel.Hide()
        self.splitter_window.ReplaceWindow(self.options_panel, panel)

        self.options_panel.Destroy()
        self.options_panel = panel

        self.tree_ctrl.DeleteAllItems()

        root = self.tree_ctrl.AddRoot(self.network.name)

        self.tree_ctrl.SetPyData(
            root,
            dict(obj=self.network, panel=NetworkPanel)
        )

        controller_room_id = self.tree_ctrl.AppendItem(
            root,
            self.network.controller.node.location
        )
        self.tree_ctrl.SetPyData(
            controller_room_id,
            dict(obj=None, panel=Panel, nodes=[], controller=True)
        )

        controller_id = self.add_node(
            controller_room_id,
            self.network.controller.node
        )
        data = self.tree_ctrl.GetPyData(controller_id)
        data['controller'] = True

        self.tree_ctrl.SetPyData(
            controller_id,
            data
        )

        rooms = {}
        for node in self.network.nodes.values():
            try:
                room = node.location
            except AttributeError:
                room = None

            if not room:
                room = 'No Room'

            if room not in rooms:
                rooms[room] = []

            rooms[room] += [node]

        for room in sorted(rooms.keys()):
            parent_id = self.tree_ctrl.AppendItem(root, room)

            self.tree_ctrl.SetPyData(
                parent_id,
                dict(obj=None, panel=Panel, nodes=[])
            )

            for node in rooms[room]:
                self.add_node(parent_id, node)

        self.tree_ctrl.Expand(root)
        self.tree_ctrl.SelectItem(root)

    def add_node(self, parent_id, node):
        name = node.name

        if not name:
            name = node.object_id_str

        data = self.tree_ctrl.GetPyData(parent_id)
        data['nodes'] += [node]

        self.tree_ctrl.SetPyData(
            parent_id,
            data
        )

        child_id = self.tree_ctrl.AppendItem(parent_id, name)

        self.tree_ctrl.SetPyData(
            child_id,
            dict(obj=node, panel=NodePanel)
        )

        for value in node.values.values():

            label = value.label
            if not label:
                label = value.object_id_str

            value_id = self.tree_ctrl.AppendItem(child_id, label)

            self.tree_ctrl.SetPyData(
                value_id,
                dict(obj=value, panel=ValuePanel)
            )

        return child_id

    def on_selection_changed(self, _):
        item_id = self.tree_ctrl.GetSelection()
        if item_id.IsOk():
            data = self.tree_ctrl.GetPyData(item_id)
            obj = data['obj']
            panel = data['panel']
            if panel == NodePanel:
                if self.network.controller.has_node_failed(obj.id):
                    self.remove_failed_node_btn.Enable(True)
                else:
                    self.remove_failed_node_btn.Enable(False)
            else:
                self.remove_failed_node_btn.Enable(False)

            if 'controller' in data:
                panel = panel(self.splitter_window, obj, True)
            else:
                panel = panel(self.splitter_window, obj)

            self.options_panel.Hide()
            self.splitter_window.ReplaceWindow(self.options_panel, panel)
            self.options_panel.Destroy()
            self.options_panel = panel

    def signal_add_node(self, network, node, node_id, **_):
        if network != self.network:
            return

        root = self.tree_ctrl.GetRootItem()

        nodes = {}
        self.get_nodes(root, nodes)

        for tree_node in nodes.keys():
            if node_id == tree_node.id:
                return

        try:
            room = node.location
        except AttributeError:
            room = None

        if not room:
            room = 'No Room'

        child_id, cookie = self.tree_ctrl.GetFirstChild(root)

        while child_id.IsOk():
            room_name = self.tree_ctrl.GetItemText(child_id)
            if room_name == room:
                child_id = self.add_node(child_id, node)
                self.tree_ctrl.SelectItem(child_id)
                return
            child_id, cookie = self.tree_ctrl.GetNextChild(child_id, cookie)

        parent_id = self.tree_ctrl.AppendItem(root, room)

        self.tree_ctrl.SetPyData(
            parent_id,
            dict(obj=None, panel=Panel, nodes=[])
        )

        self.add_node(parent_id, node)

    def get_nodes(self, parent_id, nodes):
        child_id, cookie = self.tree_ctrl.GetFirstChild(parent_id)

        while child_id.IsOk():
            data = self.tree_ctrl.GetPyData(child_id)

            if data['panel'] == NodePanel:
                nodes[data['obj']] = child_id

            elif self.tree_ctrl.ItemHasChildren(child_id):
                self.get_nodes(child_id, nodes)

            child_id, cookie = self.tree_ctrl.GetNextChild(child_id, cookie)

    def signal_remove_node(self, network, node_id, **_):
        if network != self.network:
            return
        root = self.tree_ctrl.GetRootItem()

        nodes = {}
        self.get_nodes(root, nodes)

        for node in nodes.keys():
            if node_id == node.id:
                item_id = nodes.pop(node)
                if self.tree_ctrl.GetSelection() == item_id:
                    data = self.tree_ctrl.GetPyData(root)
                    obj = data['obj']
                    panel = data['panel']
                    panel = panel(self.splitter_window, obj)
                    self.options_panel.Hide()
                    self.splitter_window.ReplaceWindow(
                        self.options_panel,
                        panel
                    )
                    self.options_panel.Destroy()
                    self.options_panel = panel
                    self.tree_ctrl.SelectItem(root)

                if self.clear_node_from_room(item_id, node):
                    self.tree_ctrl.DeleteChildren(item_id)
                    self.tree_ctrl.Delete(item_id)

                break

    def on_add_node(self, _):
        # places controller into add mode.
        self.network.controller.add_node()

    def on_remove_node(self, _):
        # places controller into remove mode
        self.network.controller.remove_node()

    def on_remove_failed_node(self, _):
        item_id = self.tree_ctrl.GetSelection()
        if item_id.IsOk():
            root = self.tree_ctrl.GetRootItem()
            node = self.tree_ctrl.GetPyData(item_id)['obj']
            # removes failed node
            data = self.tree_ctrl.GetPyData(root)
            obj = data['obj']
            panel = data['panel']
            panel = panel(self.splitter_window, obj)
            self.options_panel.Hide()
            self.splitter_window.ReplaceWindow(
                self.options_panel,
                panel
            )
            self.options_panel.Destroy()
            self.options_panel = panel
            self.tree_ctrl.SelectItem(root)

            self.network.controller.remove_failed_node(node.id)

            if self.clear_node_from_room(item_id, node):
                self.tree_ctrl.DeleteChildren(item_id)
                self.tree_ctrl.Delete(item_id)

    def on_factory_reset(self, _):
        # Factory resets controller
        self.network.controller.hard_reset()

    def on_reboot(self, _):
        # Reboots controller
        self.network.controller.soft_reset()
        self.load_tree()

    def on_receive_controller_info(self, _):
        # receives controller data
        self.network.controller.receive_configuration()

    def on_rebuild_mesh(self, _):
        # Resets network mesh. routes will get remade as needed
        self.network.controller.delete_all_return_routes()

    def on_transfer_primary(self, _):
        # transfers primary role to a secondary controller
        self.network.controller.transfer_primary_role()

    def on_send_controller_info(self, _):
        # Pushes controller data to a secondary controller
        self.network.controller.replication_send()
