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


import threading
import time


# ------------- ACTIVE -------------

# Alarm Silence Command Class - Active
# Application
COMMAND_CLASS_SILENCE_ALARM = 0x9D

# Anti-theft Command Class - Active
# Application
COMMAND_CLASS_ANTITHEFT = 0x5D

# Application Status Command Class - Active
# Management
# This Command Class MUST always be in the NIF if supported
COMMAND_CLASS_APPLICATION_STATUS = 0x22

# Association Command Class - Active
# Management
COMMAND_CLASS_ASSOCIATION = 0x85

# Association Command Configuration Command Class - Active
# Management
COMMAND_CLASS_ASSOCIATION_COMMAND_CONFIGURATION = 0x9B

# Association Group Information (AGI) Command Class - Active
# Management
COMMAND_CLASS_ASSOCIATION_GRP_INFO = 0x59

# Barrier Operator Command Class - Active
# Application
COMMAND_CLASS_BARRIER_OPERATOR = 0x66

# Basic Command Class - Active
# Application
COMMAND_CLASS_BASIC = 0x20

# Basic Tariff Information Command Class - Active
# Application
COMMAND_CLASS_BASIC_TARIFF_INFO = 0x36

# Battery Command Class - Active
# Management
COMMAND_CLASS_BATTERY = 0x80

# Binary Switch Command Class - Active
# Application
COMMAND_CLASS_SWITCH_BINARY = 0x25

# Central Scene Command Class - Active
# Application
COMMAND_CLASS_CENTRAL_SCENE = 0x5B

# Clock Command Class - Active
# Application
COMMAND_CLASS_CLOCK = 0x81

# Color Switch Command Class - Active
# Application
COMMAND_CLASS_SWITCH_COLOR = 0x33

# Configuration Command Class - Active
# Application
COMMAND_CLASS_CONFIGURATION = 0x70

# Controller Replication Command Class - Active
# Application
COMMAND_CLASS_CONTROLLER_REPLICATION = 0x21

# Demand Control Plan Configuration Command Class - Active
# Application
COMMAND_CLASS_DCP_CONFIG = 0x3A

# Demand Control Plan Monitor Command Class - Active
# Application
COMMAND_CLASS_DCP_MONITOR = 0x3B

# Device Reset Locally Command Class - Active
# Management
COMMAND_CLASS_DEVICE_RESET_LOCALLY = 0x5A

# Door Lock Command Class - Active
# Application
COMMAND_CLASS_DOOR_LOCK = 0x62

# Door Lock Logging Command Class - Active
# Application
COMMAND_CLASS_DOOR_LOCK_LOGGING = 0x4C

# Energy Production Command Class - Active
# Application
COMMAND_CLASS_ENERGY_PRODUCTION = 0x90

# Entry Control Command Class - Active
# Application
COMMAND_CLASS_ENTRY_CONTROL = 0x6F

# Firmware Update Meta Data Command Class - Active
# Management
COMMAND_CLASS_FIRMWARE_UPDATE_MD = 0x7A

# Geographic Location Command Class - Active
# Application
COMMAND_CLASS_GEOGRAPHIC_LOCATION = 0x8C

# HRV Status Command Class - Active
# Application
COMMAND_CLASS_HRV_STATUS = 0x37

# HRV Control Command Class - Active
# Application
COMMAND_CLASS_HRV_CONTROL = 0x39

# Humidity Control Mode Command Class - Active
# Application
COMMAND_CLASS_HUMIDITY_CONTROL_MODE = 0x6D

# Humidity Control Operating State Command Class - Active
# Application
COMMAND_CLASS_HUMIDITY_CONTROL_OPERATING_STATE = 0x6E

# Humidity Control Setpoint Command Class - Active
# Application
COMMAND_CLASS_HUMIDITY_CONTROL_SETPOINT = 0x64

# Inclusion Controller Command Class - Active
# Network-Protocol
# This Command Class MUST always be in the NIF if supported
COMMAND_CLASS_INCLUSION_CONTROLLER = 0x74

# Indicator Command Class - Active
# Management
COMMAND_CLASS_INDICATOR = 0x87

# IP Association Command Class - Active
# Management
COMMAND_CLASS_IP_ASSOCIATION = 0x5C

# Irrigation Command Class - Active
# Application
COMMAND_CLASS_IRRIGATION = 0x6B

# Language Command Class - Active
# Application
COMMAND_CLASS_LANGUAGE = 0x89

# Mailbox Command Class - Active
# Network-Protocol
COMMAND_CLASS_MAILBOX = 0x69

# Manufacturer proprietary Command Class - Active
# Application
COMMAND_CLASS_MANUFACTURER_PROPRIETARY = 0x91

# Manufacturer Specific Command Class - Active
# Management
# Nodes MUST reply to Manufacturer Specific Get Commands received non-securely
# if S0 is the highest granted key (CC:0072.01.00.41.004)
COMMAND_CLASS_MANUFACTURER_SPECIFIC = 0x72

# Mark (Support/Control Mark) - Active
# N/A
# This marker is not an actual Command Class
COMMAND_CLASS_MARK = 0xEF

# Meter Command Class - Active
# Application
COMMAND_CLASS_METER = 0x32

# Meter Table Configuration Command Class - Active
# Application
COMMAND_CLASS_METER_TBL_CONFIG = 0x3C

# Meter Table Monitor Command Class - Active
# Application
COMMAND_CLASS_METER_TBL_MONITOR = 0x3D

# Meter Table Push Configuration Command Class - Active
# Application
COMMAND_CLASS_METER_TBL_PUSH = 0x3E

# Multi Channel Command Class - Active
# Transport-Encapsulation
COMMAND_CLASS_MULTI_CHANNEL = 0x60

# Multi Channel Association Command Class - Active
# Management
COMMAND_CLASS_MULTI_CHANNEL_ASSOCIATION = 0x8E

# Multi Command Command Class - Active
# Transport-Encapsulation
# This Command Class MUST always be in the NIF if supported
COMMAND_CLASS_MULTI_CMD = 0x8F

# Multilevel Sensor Command Class - Active
# Application
COMMAND_CLASS_SENSOR_MULTILEVEL = 0x31

# Multilevel Switch Command Class - Active
# Application
COMMAND_CLASS_SWITCH_MULTILEVEL = 0x26

# Network Management Basic Node Command Class - Active
# Network-Protocol
COMMAND_CLASS_NETWORK_MANAGEMENT_BASIC = 0x4D

# Network Management Inclusion Command Class - Active
# Network-Protocol
COMMAND_CLASS_NETWORK_MANAGEMENT_INCLUSION = 0x34

# Network Management Installation and Maintenance Command Class - Active
# Network-Protocol
NETWORK_MANAGEMENT_INSTALLATION_MAINTENANCE = 0x67

# Network Management Proxy Command Class - Active
# Network-Protocol
COMMAND_CLASS_NETWORK_MANAGEMENT_PROXY = 0x52

# No Operation Command Class - Active
# Network-Protocol
COMMAND_CLASS_NO_OPERATION = 0x00

# Node Naming and Location Command Class - Active
# Management
COMMAND_CLASS_NODE_NAMING = 0x77

# Node Provisioning Command Class - Active
# Network-Protocol
COMMAND_CLASS_NODE_PROVISIONING = 0x78

# Notification Command Class - Active
# Application
COMMAND_CLASS_NOTIFICATION = 0x71

# Powerlevel Command Class - Active
# Network-Protocol
COMMAND_CLASS_POWERLEVEL = 0x73

# Prepayment Command Class - Active
# Application
COMMAND_CLASS_PREPAYMENT = 0x3F

# Prepayment Encapsulation Command Class - Active
# Application
COMMAND_CLASS_PREPAYMENT_ENCAPSULATION = 0x41

# Protection Command Class - Active
# Application
COMMAND_CLASS_PROTECTION = 0x75

# Rate Table Configuration Command Class - Active
# Application
COMMAND_CLASS_RATE_TBL_CONFIG = 0x48

# Rate Table Monitor Command Class - Active
# Application
COMMAND_CLASS_RATE_TBL_MONITOR = 0x49

# Scene Activation Command Class - Active
# Application
COMMAND_CLASS_SCENE_ACTIVATION = 0x2B

# Scene Actuator Configuration Command Class - Active
# Application
COMMAND_CLASS_SCENE_ACTUATOR_CONF = 0x2C

# Scene Controller Configuration Command Class - Active
# Application
COMMAND_CLASS_SCENE_CONTROLLER_CONF = 0x2D

# Schedule Command Class - Active
# Application
COMMAND_CLASS_SCHEDULE = 0x53

# Screen Attributes Command Class - Active
# Application
COMMAND_CLASS_SCREEN_ATTRIBUTES = 0x93

# Screen Meta Data Command Class - Active
# Application
COMMAND_CLASS_SCREEN_MD = 0x92

# Security 0 Command Class - Active
# Transport-Encapsulation
COMMAND_CLASS_SECURITY = 0x98

# Security 2 Command Class - Active
# Transport-Encapsulation
# This Command Class MUST always be in the NIF if supported
COMMAND_CLASS_SECURITY_2 = 0x9F

# Security Mark (Unsecure/Secure Mark) - Active
# N/A
# This marker is not an actual Command Class
COMMAND_CLASS_SECURITY_SCHEME0_MARK = 0xF100

# Simple AV Control Command Class - Active
# Application
COMMAND_CLASS_SIMPLE_AV_CONTROL = 0x94

# Sound Switch Command Class - Active
# Application
COMMAND_CLASS_SOUND_SWITCH = 0x79

# Supervision Command Class - Active
# Transport-Encapsulation
# This Command Class MUST always be in the NIF if supported
COMMAND_CLASS_SUPERVISION = 0x6C

# Tariff Table Configuration Command Class - Active
# Application
COMMAND_CLASS_TARIFF_CONFIG = 0x4A

# Tariff Table Monitor Command Class - Active
# Application
COMMAND_CLASS_TARIFF_TBL_MONITOR = 0x4B

# Thermostat Fan Mode Command Class - Active
# Application
COMMAND_CLASS_THERMOSTAT_FAN_MODE = 0x44

# Thermostat Fan State Command Class - Active
# Application
COMMAND_CLASS_THERMOSTAT_FAN_STATE = 0x45

# Thermostat Mode Command Class - Active
# Application
COMMAND_CLASS_THERMOSTAT_MODE = 0x40

# Thermostat Operating State Command Class - Active
# Application
COMMAND_CLASS_THERMOSTAT_OPERATING_STATE = 0x42

# Thermostat Setback Command Class - Active
# Application
COMMAND_CLASS_THERMOSTAT_SETBACK = 0x47

# Thermostat Setpoint Command Class - Active
# Application
COMMAND_CLASS_THERMOSTAT_SETPOINT = 0x43

# Time Command Class - Active
# Application
# This Command Class MUST always be in the NIF if supported
COMMAND_CLASS_TIME = 0x8A

# Time Parameters Command Class - Active
# Application
COMMAND_CLASS_TIME_PARAMETERS = 0x8B

# Transport Service Command Class - Active
# Transport-Encapsulation
# This Command Class MUST always be in the NIF if supported
COMMAND_CLASS_TRANSPORT_SERVICE = 0x55

# User Code Command Class - Active
# Application
COMMAND_CLASS_USER_CODE = 0x63

# Version Command Class - Active
# Management
COMMAND_CLASS_VERSION = 0x86

# Wake Up Command Class - Active
# Management
COMMAND_CLASS_WAKE_UP = 0x84

# Window Covering Command Class - Active
# Application
COMMAND_CLASS_WINDOW_COVERING = 0x6A

# Z/IP Command Class - Active
# Network-Protocol
COMMAND_CLASS_ZIP = 0x23

# Z/IP 6LoWPAN Command Class - Active
# Network-Protocol
COMMAND_CLASS_ZIP_6LOWPAN = 0x4F

# Z/IP Gateway Command Class - Active
# Network-Protocol
COMMAND_CLASS_ZIP_GATEWAY = 0x5F

# Z/IP Naming and Location Command Class - Active
# Management
COMMAND_CLASS_ZIP_NAMING = 0x68

# Z/IP ND Command Class - Active
# Network-Protocol
COMMAND_CLASS_ZIP_ND = 0x58

# Z/IP Portal Command Class - Active
# Network-Protocol
COMMAND_CLASS_ZIP_PORTAL = 0x61

# Z-Wave Plus Info Command Class - Active
# Management
# This Command Class MUST always be in the NIF if supported
COMMAND_CLASS_ZWAVEPLUS_INFO = 0x5E

# ----------- DEPRECIATED ----------

# Alarm Command Class - Depreciated
# Application
# Alarm has been renamed/overloaded by the Notification Command Class
COMMAND_CLASS_ALARM = 0x71

# Alarm Sensor Command Class - Depreciated
# Application
COMMAND_CLASS_SENSOR_ALARM = 0x9C

# Binary Sensor Command Class - Depreciated
# Application
COMMAND_CLASS_SENSOR_BINARY = 0x30

# Climate Control Schedule Command Class - Depreciated
# Application
COMMAND_CLASS_CLIMATE_CONTROL_SCHEDULE = 0x46

# CRC-16 Encapsulation Command Class - Depreciated
# Transport-Encapsulation
# This Command Class MUST always be in the NIF if supported
COMMAND_CLASS_CRC_16_ENCAP = 0x56

# Grouping Name Command Class - Depreciated
# Management
COMMAND_CLASS_GROUPING_NAME = 0x7B

# Lock Command Class - Depreciated
# Application
COMMAND_CLASS_LOCK = 0x76

# Multilevel Toggle Switch Command Class - Depreciated
# Application
COMMAND_CLASS_SWITCH_TOGGLE_MULTILEVEL = 0x29

# Proprietary Command Class - Depreciated
# Application
COMMAND_CLASS_PROPRIETARY = 0x88

# Pulse Meter Command Class - Depreciated
# Application
COMMAND_CLASS_METER_PULSE = 0x35

# Schedule Entry Lock Command Class - Depreciated
# Application
COMMAND_CLASS_SCHEDULE_ENTRY_LOCK = 0x4E

# ------------ OBSOLETE ------------

# All Switch Command Class - Obsolete
# Application
COMMAND_CLASS_SWITCH_ALL = 0x27

# Application Capability Command Class - Obsolete
# Management
COMMAND_CLASS_APPLICATION_CAPABILITY = 0x57

# Basic Window Covering Command Class - Obsolete
# Application
COMMAND_CLASS_BASIC_WINDOW_COVERING = 0x50

# Binary Toggle Switch Command Class - Obsolete
# Application
COMMAND_CLASS_SWITCH_TOGGLE_BINARY = 0x28

# Hail Command Class - Obsolete
# Management
COMMAND_CLASS_HAIL = 0x82

# IP Configuration Command Class - Obsolete
# Management
COMMAND_CLASS_IP_CONFIGURATION = 0x9A

# Move To Position Window Covering Command Class - Obsolete
# Application
COMMAND_CLASS_MTP_WINDOW_COVERING = 0x51

# Network Management Primary Command Class - Obsolete
# Network-Protocol
COMMAND_CLASS_NETWORK_MANAGEMENT_PRIMARY = 0x54

# Remote Association Activation Command Class - Obsolete
# Management
COMMAND_CLASS_REMOTE_ASSOCIATION_ACTIVATE = 0x7C

# Remote Association Configuration Command Class - Obsolete
# Management
COMMAND_CLASS_REMOTE_ASSOCIATION = 0x7D

# Sensor Configuration Command Class - Obsolete
# Application
COMMAND_CLASS_SENSOR_CONFIGURATION = 0x9E


ALARM = COMMAND_CLASS_ALARM
ANTITHEFT = COMMAND_CLASS_ANTITHEFT
APPLICATION_CAPABILITY = COMMAND_CLASS_APPLICATION_CAPABILITY
APPLICATION_STATUS = COMMAND_CLASS_APPLICATION_STATUS
ASSOCIATION = COMMAND_CLASS_ASSOCIATION
ASSOCIATION_COMMAND_CONFIGURATION = (
    COMMAND_CLASS_ASSOCIATION_COMMAND_CONFIGURATION
)
ASSOCIATION_GRP_INFO = COMMAND_CLASS_ASSOCIATION_GRP_INFO
BARRIER_OPERATOR = COMMAND_CLASS_BARRIER_OPERATOR
BASIC = COMMAND_CLASS_BASIC
BASIC_TARIFF_INFO = COMMAND_CLASS_BASIC_TARIFF_INFO
BASIC_WINDOW_COVERING = COMMAND_CLASS_BASIC_WINDOW_COVERING
BATTERY = COMMAND_CLASS_BATTERY
CENTRAL_SCENE = COMMAND_CLASS_CENTRAL_SCENE
CLIMATE_CONTROL_SCHEDULE = COMMAND_CLASS_CLIMATE_CONTROL_SCHEDULE
CLOCK = COMMAND_CLASS_CLOCK
CONFIGURATION = COMMAND_CLASS_CONFIGURATION
CONTROLLER_REPLICATION = COMMAND_CLASS_CONTROLLER_REPLICATION
CRC_16_ENCAP = COMMAND_CLASS_CRC_16_ENCAP
DCP_CONFIG = COMMAND_CLASS_DCP_CONFIG
DCP_MONITOR = COMMAND_CLASS_DCP_MONITOR
DEVICE_RESET_LOCALLY = COMMAND_CLASS_DEVICE_RESET_LOCALLY
DOOR_LOCK = COMMAND_CLASS_DOOR_LOCK
DOOR_LOCK_LOGGING = COMMAND_CLASS_DOOR_LOCK_LOGGING
ENERGY_PRODUCTION = COMMAND_CLASS_ENERGY_PRODUCTION
ENTRY_CONTROL = COMMAND_CLASS_ENTRY_CONTROL
FIRMWARE_UPDATE_MD = COMMAND_CLASS_FIRMWARE_UPDATE_MD
GEOGRAPHIC_LOCATION = COMMAND_CLASS_GEOGRAPHIC_LOCATION
GROUPING_NAME = COMMAND_CLASS_GROUPING_NAME
HAIL = COMMAND_CLASS_HAIL
HRV_CONTROL = COMMAND_CLASS_HRV_CONTROL
HRV_STATUS = COMMAND_CLASS_HRV_STATUS
HUMIDITY_CONTROL_MODE = COMMAND_CLASS_HUMIDITY_CONTROL_MODE
HUMIDITY_CONTROL_OPERATING_STATE = (
    COMMAND_CLASS_HUMIDITY_CONTROL_OPERATING_STATE
)
HUMIDITY_CONTROL_SETPOINT = COMMAND_CLASS_HUMIDITY_CONTROL_SETPOINT
INCLUSION_CONTROLLER = COMMAND_CLASS_INCLUSION_CONTROLLER
INDICATOR = COMMAND_CLASS_INDICATOR
IP_ASSOCIATION = COMMAND_CLASS_IP_ASSOCIATION
IP_CONFIGURATION = COMMAND_CLASS_IP_CONFIGURATION
IRRIGATION = COMMAND_CLASS_IRRIGATION
LANGUAGE = COMMAND_CLASS_LANGUAGE
LOCK = COMMAND_CLASS_LOCK
MAILBOX = COMMAND_CLASS_MAILBOX
MANUFACTURER_PROPRIETARY = COMMAND_CLASS_MANUFACTURER_PROPRIETARY
MANUFACTURER_SPECIFIC = COMMAND_CLASS_MANUFACTURER_SPECIFIC
MARK = COMMAND_CLASS_MARK
METER = COMMAND_CLASS_METER
METER_PULSE = COMMAND_CLASS_METER_PULSE
METER_TBL_CONFIG = COMMAND_CLASS_METER_TBL_CONFIG
METER_TBL_MONITOR = COMMAND_CLASS_METER_TBL_MONITOR
METER_TBL_PUSH = COMMAND_CLASS_METER_TBL_PUSH
MTP_WINDOW_COVERING = COMMAND_CLASS_MTP_WINDOW_COVERING
MULTI_CHANNEL = COMMAND_CLASS_MULTI_CHANNEL
MULTI_CHANNEL_ASSOCIATION = COMMAND_CLASS_MULTI_CHANNEL_ASSOCIATION
MULTI_CMD = COMMAND_CLASS_MULTI_CMD
NETWORK_MANAGEMENT_BASIC = COMMAND_CLASS_NETWORK_MANAGEMENT_BASIC
NETWORK_MANAGEMENT_INCLUSION = COMMAND_CLASS_NETWORK_MANAGEMENT_INCLUSION
NETWORK_MANAGEMENT_PRIMARY = COMMAND_CLASS_NETWORK_MANAGEMENT_PRIMARY
NETWORK_MANAGEMENT_PROXY = COMMAND_CLASS_NETWORK_MANAGEMENT_PROXY
NODE_NAMING = COMMAND_CLASS_NODE_NAMING
NODE_PROVISIONING = COMMAND_CLASS_NODE_PROVISIONING
NOTIFICATION = COMMAND_CLASS_NOTIFICATION
NO_OPERATION = COMMAND_CLASS_NO_OPERATION
POWERLEVEL = COMMAND_CLASS_POWERLEVEL
PREPAYMENT = COMMAND_CLASS_PREPAYMENT
PREPAYMENT_ENCAPSULATION = COMMAND_CLASS_PREPAYMENT_ENCAPSULATION
PROPRIETARY = COMMAND_CLASS_PROPRIETARY
PROTECTION = COMMAND_CLASS_PROTECTION
RATE_TBL_CONFIG = COMMAND_CLASS_RATE_TBL_CONFIG
RATE_TBL_MONITOR = COMMAND_CLASS_RATE_TBL_MONITOR
REMOTE_ASSOCIATION = COMMAND_CLASS_REMOTE_ASSOCIATION
REMOTE_ASSOCIATION_ACTIVATE = COMMAND_CLASS_REMOTE_ASSOCIATION_ACTIVATE
SCENE_ACTIVATION = COMMAND_CLASS_SCENE_ACTIVATION
SCENE_ACTUATOR_CONF = COMMAND_CLASS_SCENE_ACTUATOR_CONF
SCENE_CONTROLLER_CONF = COMMAND_CLASS_SCENE_CONTROLLER_CONF
SCHEDULE = COMMAND_CLASS_SCHEDULE
SCHEDULE_ENTRY_LOCK = COMMAND_CLASS_SCHEDULE_ENTRY_LOCK
SCREEN_ATTRIBUTES = COMMAND_CLASS_SCREEN_ATTRIBUTES
SCREEN_MD = COMMAND_CLASS_SCREEN_MD
SECURITY = COMMAND_CLASS_SECURITY
SECURITY_2 = COMMAND_CLASS_SECURITY_2
SECURITY_SCHEME0_MARK = COMMAND_CLASS_SECURITY_SCHEME0_MARK
SENSOR_ALARM = COMMAND_CLASS_SENSOR_ALARM
SENSOR_BINARY = COMMAND_CLASS_SENSOR_BINARY
SENSOR_CONFIGURATION = COMMAND_CLASS_SENSOR_CONFIGURATION
SENSOR_MULTILEVEL = COMMAND_CLASS_SENSOR_MULTILEVEL
SILENCE_ALARM = COMMAND_CLASS_SILENCE_ALARM
SIMPLE_AV_CONTROL = COMMAND_CLASS_SIMPLE_AV_CONTROL
SOUND_SWITCH = COMMAND_CLASS_SOUND_SWITCH
SUPERVISION = COMMAND_CLASS_SUPERVISION
SWITCH_ALL = COMMAND_CLASS_SWITCH_ALL
SWITCH_BINARY = COMMAND_CLASS_SWITCH_BINARY
SWITCH_COLOR = COMMAND_CLASS_SWITCH_COLOR
SWITCH_MULTILEVEL = COMMAND_CLASS_SWITCH_MULTILEVEL
SWITCH_TOGGLE_BINARY = COMMAND_CLASS_SWITCH_TOGGLE_BINARY
SWITCH_TOGGLE_MULTILEVEL = COMMAND_CLASS_SWITCH_TOGGLE_MULTILEVEL
TARIFF_CONFIG = COMMAND_CLASS_TARIFF_CONFIG
TARIFF_TBL_MONITOR = COMMAND_CLASS_TARIFF_TBL_MONITOR
THERMOSTAT_FAN_MODE = COMMAND_CLASS_THERMOSTAT_FAN_MODE
THERMOSTAT_FAN_STATE = COMMAND_CLASS_THERMOSTAT_FAN_STATE
THERMOSTAT_MODE = COMMAND_CLASS_THERMOSTAT_MODE
THERMOSTAT_OPERATING_STATE = COMMAND_CLASS_THERMOSTAT_OPERATING_STATE
THERMOSTAT_SETBACK = COMMAND_CLASS_THERMOSTAT_SETBACK
THERMOSTAT_SETPOINT = COMMAND_CLASS_THERMOSTAT_SETPOINT
TIME = COMMAND_CLASS_TIME
TIME_PARAMETERS = COMMAND_CLASS_TIME_PARAMETERS
TRANSPORT_SERVICE = COMMAND_CLASS_TRANSPORT_SERVICE
USER_CODE = COMMAND_CLASS_USER_CODE
VERSION = COMMAND_CLASS_VERSION
WAKE_UP = COMMAND_CLASS_WAKE_UP
WINDOW_COVERING = COMMAND_CLASS_WINDOW_COVERING
ZIP_6LOWPAN = COMMAND_CLASS_ZIP_6LOWPAN
ZIP_GATEWAY = COMMAND_CLASS_ZIP_GATEWAY
ZIP_NAMING = COMMAND_CLASS_ZIP_NAMING
ZIP_ND = COMMAND_CLASS_ZIP_ND
ZIP_PORTAL = COMMAND_CLASS_ZIP_PORTAL
ZWAVEPLUS_INFO = COMMAND_CLASS_ZWAVEPLUS_INFO


VALUE_TEMPLATE = (
    'Label: {label}\n'
    'Min: {min}\n'
    'Max: {max}\n'
    'Data: {data}\n'
    'Data String: {data_str}\n'
    'Type: {type}\n'
    'Index: {index}\n'
    'Is Polled: {is_polled}\n'
    'Genre: {genre}\n'
    'Units: {units}\n'
    'Read Only: {read_only}\n'
    'Write Only: {write_only}\n'
    'Help: {help}\n'

)


def print_not_implemented(*_): # cmd_cls, device):
    # print ((
    #     '{0}: This command class has not been implemented if you would\n'
    #     'please private message the following data to the user kgschlosser '
    #     'on the EventGhost forums\n'
    # ).format(cmd_cls))
    #
    # c_cls = getattr(cc, cmd_cls)
    #
    # values = list(
    #     value for value in device.values.values()
    #     if value == c_cls
    # )
    #
    # for value in values:
    #     print(VALUE_TEMPLATE.format(
    #         label=repr(value.label),
    #         min=repr(value.min),
    #         max=repr(value.max),
    #         data=repr(value.data),
    #         data_str=repr(value.data_as_string),
    #         type=value.type,
    #         index=value.index,
    #         is_polled=value.is_polled,
    #         genre=repr(value.genre),
    #         units=repr(value.units),
    #         read_only=value.is_read_only,
    #         write_only=value.is_write_only,
    #         help=repr(value.help),
    #     ))
    pass


class CommandClassBase(object):

    def __init__(self):
        self.values = {}


class Alarm(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)

        if not hasattr(self, '_cls_ids'):
            self._cls_ids = []

        self._cls_ids += [COMMAND_CLASS_ALARM]
        print_not_implemented('COMMAND_CLASS_ALARM', self)


class Antitheft(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)

        if not hasattr(self, '_cls_ids'):
            self._cls_ids = []

        self._cls_ids += [COMMAND_CLASS_ANTITHEFT]
        print_not_implemented('COMMAND_CLASS_ANTITHEFT', self)


class ApplicationCapability(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)

        if not hasattr(self, '_cls_ids'):
            self._cls_ids = []

        self._cls_ids += [COMMAND_CLASS_APPLICATION_CAPABILITY]
        print_not_implemented(
            'COMMAND_CLASS_APPLICATION_CAPABILITY',
            self
        )


class ApplicationStatus(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)

        if not hasattr(self, '_cls_ids'):
            self._cls_ids = []

        self._cls_ids += [COMMAND_CLASS_APPLICATION_STATUS]
        print_not_implemented('COMMAND_CLASS_APPLICATION_STATUS', self)


class Association(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)

        if not hasattr(self, '_cls_ids'):
            self._cls_ids = []

        self._cls_ids += [COMMAND_CLASS_ASSOCIATION]
        print_not_implemented('COMMAND_CLASS_ASSOCIATION', self)

    def get_max_associations(self, groupidx):
        return self.get_max_associations(groupidx)


class AssociationCommandConfiguration(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)

        if not hasattr(self, '_cls_ids'):
            self._cls_ids = []

        self._cls_ids += [COMMAND_CLASS_ASSOCIATION_COMMAND_CONFIGURATION]
        print_not_implemented(
            'COMMAND_CLASS_ASSOCIATION_COMMAND_CONFIGURATION',
            self
        )


class AssociationGrpInfo(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)

        if not hasattr(self, '_cls_ids'):
            self._cls_ids = []

        self._cls_ids += [COMMAND_CLASS_ASSOCIATION_GRP_INFO]
        print_not_implemented(
            'COMMAND_CLASS_ASSOCIATION_GRP_INFO',
            self
        )

    @property
    def groups(self):
        return self.groups()

    def groups_to_dict(self, extras=('all',)):
        return self.groups_to_dict(extras)


class BarrierOperator(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)

        if not hasattr(self, '_cls_ids'):
            self._cls_ids = []

        self._cls_ids += [COMMAND_CLASS_BARRIER_OPERATOR]
        print_not_implemented('COMMAND_CLASS_BARRIER_OPERATOR', self)


class Basic(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)

        if not hasattr(self, '_cls_ids'):
            self._cls_ids = []

        self._cls_ids += [COMMAND_CLASS_BASIC]
        print_not_implemented('COMMAND_CLASS_BASIC', self)


class BasicTariffInfo(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)

        if not hasattr(self, '_cls_ids'):
            self._cls_ids = []

        self._cls_ids += [COMMAND_CLASS_BASIC_TARIFF_INFO]
        print_not_implemented('COMMAND_CLASS_BASIC_TARIFF_INFO', self)


class BasicWindowCovering(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)

        if not hasattr(self, '_cls_ids'):
            self._cls_ids = []

        self._cls_ids += [COMMAND_CLASS_BASIC_WINDOW_COVERING]
        print_not_implemented(
            'COMMAND_CLASS_BASIC_WINDOW_COVERING',
            self
        )


class Battery(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)

        if not hasattr(self, '_cls_ids'):
            self._cls_ids = []

        self._cls_ids += [COMMAND_CLASS_BATTERY]

    @property
    def batteries(self):
        res = []
        for value in self.values.values():
            if value == COMMAND_CLASS_BATTERY:
                res += [self.Battery(value)]
        return res


    class Battery(object):

        def __init__(self, battery):
            self._battery = battery

        def __getattr__(self, item):
            if item in self.__dict__:
                return self.__dict__[item]

            if hasattr(self._battery, item):
                return getattr(self._battery, item)

            raise AttributeError(item)

        @property
        def level(self):
            return self._battery.data


class CentralScene(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)

        if not hasattr(self, '_cls_ids'):
            self._cls_ids = []

        self._cls_ids += [COMMAND_CLASS_CENTRAL_SCENE]
        print_not_implemented('COMMAND_CLASS_CENTRAL_SCENE', self)


class ClimateControlSchedule(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)

        if not hasattr(self, '_cls_ids'):
            self._cls_ids = []

        self._cls_ids += [COMMAND_CLASS_CLIMATE_CONTROL_SCHEDULE]
        print_not_implemented(
            'COMMAND_CLASS_CLIMATE_CONTROL_SCHEDULE',
            self
        )


class Clock(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)

        if not hasattr(self, '_cls_ids'):
            self._cls_ids = []

        self._cls_ids += [COMMAND_CLASS_CLOCK]
        print_not_implemented('COMMAND_CLASS_CLOCK', self)


class Configuration(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)

        if not hasattr(self, '_cls_ids'):
            self._cls_ids = []

        self._cls_ids += [COMMAND_CLASS_CONFIGURATION]

    @property
    def settings(self):
        res = []
        for value in self.values.values():
            if (
                value == COMMAND_CLASS_CONFIGURATION and
                value.genre == 'Config'
            ):
                res += [self.Configuration(value)]
        return res


    class Configuration(object):

        def __init__(self, setting):
            self._setting = setting

        @property
        def id(self):
            return self._setting.value_id

        @property
        def value(self):
            return self._setting.data

        @value.setter
        def value(self, value):
            self._setting.data = value

        def __getattr__(self, item):
            if item in self.__dict__:
                return self.__dict__[item]

            if hasattr(self._setting, item):
                return getattr(self._setting, item)

            raise AttributeError(item)


class ControllerReplication(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)

        if not hasattr(self, '_cls_ids'):
            self._cls_ids = []

        self._cls_ids += [COMMAND_CLASS_CONTROLLER_REPLICATION]
        print_not_implemented(
            'COMMAND_CLASS_CONTROLLER_REPLICATION',
            self
        )


class Crc16Encap(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)

        if not hasattr(self, '_cls_ids'):
            self._cls_ids = []

        self._cls_ids += [COMMAND_CLASS_CRC_16_ENCAP]
        print_not_implemented('COMMAND_CLASS_CRC_16_ENCAP', self)


class DcpConfig(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)

        if not hasattr(self, '_cls_ids'):
            self._cls_ids = []

        self._cls_ids += [COMMAND_CLASS_DCP_CONFIG]
        print_not_implemented('COMMAND_CLASS_DCP_CONFIG', self)


class DcpMonitor(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)

        if not hasattr(self, '_cls_ids'):
            self._cls_ids = []

        self._cls_ids += [COMMAND_CLASS_DCP_MONITOR]
        print_not_implemented('COMMAND_CLASS_DCP_MONITOR', self)


class DeviceResetLocally(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)

        if not hasattr(self, '_cls_ids'):
            self._cls_ids = []

        self._cls_ids += [COMMAND_CLASS_DEVICE_RESET_LOCALLY]
        print_not_implemented(
            'COMMAND_CLASS_DEVICE_RESET_LOCALLY',
            self
        )


class DoorLock(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)

        if not hasattr(self, '_cls_ids'):
            self._cls_ids = []

        self._cls_ids += [COMMAND_CLASS_DOOR_LOCK]
        print_not_implemented('COMMAND_CLASS_DOOR_LOCK', self)

    @property
    def status(self):
        for value in self.values.values():
            if (
                value == COMMAND_CLASS_DOOR_LOCK and
                value.label == 'Status'
            ):
                return value.data

    @status.setter
    def status(self, value):
        for val in self.values.values():
            if (
                val == COMMAND_CLASS_DOOR_LOCK and
                val.label == 'Status'
            ):
                val.data = value
                break


class DoorLockLogging(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)

        if not hasattr(self, '_cls_ids'):
            self._cls_ids = []

        self._cls_ids += [COMMAND_CLASS_DOOR_LOCK_LOGGING]
        print_not_implemented('COMMAND_CLASS_DOOR_LOCK_LOGGING', self)

    @property
    def doorlock_logs(self):
        res = []
        for value in self.values.values():
            if value == COMMAND_CLASS_DOOR_LOCK_LOGGING:
                res += [value.data]
        return res


class EnergyProduction(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)

        if not hasattr(self, '_cls_ids'):
            self._cls_ids = []

        self._cls_ids += [COMMAND_CLASS_ENERGY_PRODUCTION]
        print_not_implemented('COMMAND_CLASS_ENERGY_PRODUCTION', self)


class EntryControl(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)

        if not hasattr(self, '_cls_ids'):
            self._cls_ids = []

        self._cls_ids += [COMMAND_CLASS_ENTRY_CONTROL]
        print_not_implemented('COMMAND_CLASS_ENTRY_CONTROL', self)


class FirmwareUpdateMd(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)

        if not hasattr(self, '_cls_ids'):
            self._cls_ids = []

        self._cls_ids += [COMMAND_CLASS_FIRMWARE_UPDATE_MD]
        print_not_implemented('COMMAND_CLASS_FIRMWARE_UPDATE_MD', self)


class GeographicLocation(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)

        if not hasattr(self, '_cls_ids'):
            self._cls_ids = []

        self._cls_ids += [COMMAND_CLASS_GEOGRAPHIC_LOCATION]
        print_not_implemented(
            'COMMAND_CLASS_GEOGRAPHIC_LOCATION',
            self
        )


class GroupingName(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)

        if not hasattr(self, '_cls_ids'):
            self._cls_ids = []

        self._cls_ids += [COMMAND_CLASS_GROUPING_NAME]
        print_not_implemented('COMMAND_CLASS_GROUPING_NAME', self)


class Hail(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)

        if not hasattr(self, '_cls_ids'):
            self._cls_ids = []

        self._cls_ids += [COMMAND_CLASS_HAIL]
        print_not_implemented('COMMAND_CLASS_HAIL', self)


class HrvControl(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)

        if not hasattr(self, '_cls_ids'):
            self._cls_ids = []

        self._cls_ids += [COMMAND_CLASS_HRV_CONTROL]
        print_not_implemented('COMMAND_CLASS_HRV_CONTROL', self)


class HrvStatus(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)

        if not hasattr(self, '_cls_ids'):
            self._cls_ids = []

        self._cls_ids += [COMMAND_CLASS_HRV_STATUS]
        print_not_implemented('COMMAND_CLASS_HRV_STATUS', self)


class HumidityControlMode(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)

        if not hasattr(self, '_cls_ids'):
            self._cls_ids = []

        self._cls_ids += [COMMAND_CLASS_HUMIDITY_CONTROL_MODE]
        print_not_implemented(
            'COMMAND_CLASS_HUMIDITY_CONTROL_MODE',
            self
        )


class HumidityControlOperatingState(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)

        if not hasattr(self, '_cls_ids'):
            self._cls_ids = []

        self._cls_ids += [COMMAND_CLASS_HUMIDITY_CONTROL_OPERATING_STATE]
        print_not_implemented(
            'COMMAND_CLASS_HUMIDITY_CONTROL_OPERATING_STATE',
            self
        )


class HumidityControlSetpoint(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)

        if not hasattr(self, '_cls_ids'):
            self._cls_ids = []

        self._cls_ids += [COMMAND_CLASS_HUMIDITY_CONTROL_SETPOINT]
        print_not_implemented(
            'COMMAND_CLASS_HUMIDITY_CONTROL_SETPOINT',
            self
        )


class InclusionController(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)

        if not hasattr(self, '_cls_ids'):
            self._cls_ids = []

        self._cls_ids += [COMMAND_CLASS_INCLUSION_CONTROLLER]
        print_not_implemented(
            'COMMAND_CLASS_INCLUSION_CONTROLLER',
            self
        )


class Indicator(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)

        if not hasattr(self, '_cls_ids'):
            self._cls_ids = []

        self._cls_ids += [COMMAND_CLASS_INDICATOR]
        print_not_implemented('COMMAND_CLASS_INDICATOR', self)

    @property
    def indicators(self):
        indicators = list(
            value for value in self.values.values()
            if value == COMMAND_CLASS_INDICATOR
        )
        if indicators:
            return self.Indicators(indicators)


    class Indicators(object):

        def __init__(self, indicators):
            self._indicators = indicators

        def __contains__(self, item):
            return hasattr(self, item)

        def __iter__(self):
            for indicator in self._indicators:
                yield indicator

        def __getattr__(self, item):
            if item in self.__dict__:
                return self.__dict__[item]

            label = item.replace('_', ' ').title()
            for indicator in self._indicators:
                if label == indicator.label:
                    return indicator.data

            raise AttributeError(item)

        def __setattr__(self, key, value):
            if key.startswith('_'):
                object.__setattr__(self, key, value)
            else:
                if key in self:
                    label = key.replace('_', ' ').title()
                    for indicator in self._indicators:
                        if (
                            indicator.label == label and
                            not indicator.readonly
                        ):
                            indicator.data = value
                else:
                    raise AttributeError(key)


class IpAssociation(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)

        if not hasattr(self, '_cls_ids'):
            self._cls_ids = []

        self._cls_ids += [COMMAND_CLASS_IP_ASSOCIATION]
        print_not_implemented('COMMAND_CLASS_IP_ASSOCIATION', self)


class IpConfiguration(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)

        if not hasattr(self, '_cls_ids'):
            self._cls_ids = []

        self._cls_ids += [COMMAND_CLASS_IP_CONFIGURATION]
        print_not_implemented('COMMAND_CLASS_IP_CONFIGURATION', self)


class Irrigation(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)

        if not hasattr(self, '_cls_ids'):
            self._cls_ids = []

        self._cls_ids += [COMMAND_CLASS_IRRIGATION]
        print_not_implemented('COMMAND_CLASS_IRRIGATION', self)


class Language(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)

        if not hasattr(self, '_cls_ids'):
            self._cls_ids = []

        self._cls_ids += [COMMAND_CLASS_LANGUAGE]
        print_not_implemented('COMMAND_CLASS_LANGUAGE', self)


class Lock(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)

        if not hasattr(self, '_cls_ids'):
            self._cls_ids = []

        self._cls_ids += [COMMAND_CLASS_LOCK]
        print_not_implemented('COMMAND_CLASS_LOCK', self)


class Mailbox(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)

        if not hasattr(self, '_cls_ids'):
            self._cls_ids = []

        self._cls_ids += [COMMAND_CLASS_MAILBOX]
        print_not_implemented('COMMAND_CLASS_MAILBOX', self)


class ManufacturerProprietary(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)

        if not hasattr(self, '_cls_ids'):
            self._cls_ids = []

        self._cls_ids += [COMMAND_CLASS_MANUFACTURER_PROPRIETARY]
        print_not_implemented(
            'COMMAND_CLASS_MANUFACTURER_PROPRIETARY',
            self
        )


class ManufacturerSpecific(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)

        if not hasattr(self, '_cls_ids'):
            self._cls_ids = []

        self._cls_ids += [COMMAND_CLASS_MANUFACTURER_SPECIFIC]
        print_not_implemented(
            'COMMAND_CLASS_MANUFACTURER_SPECIFIC',
            self
        )


class Mark(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)

        if not hasattr(self, '_cls_ids'):
            self._cls_ids = []

        self._cls_ids += [COMMAND_CLASS_MARK]
        print_not_implemented('COMMAND_CLASS_MARK', self)


class Meter(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)

        if not hasattr(self, '_cls_ids'):
            self._cls_ids = []

        self._cls_ids += [COMMAND_CLASS_METER]
        print_not_implemented('COMMAND_CLASS_METER', self)

    @property
    def meter_sensors(self):
        res = []
        for value in self.values.values():
            if value == COMMAND_CLASS_METER:
                res += [self.Meter(value)]
        return res


    class Meter(object):

        def __init__(self, sensor):
            self._sensor = sensor

        @property
        def value(self):
            return self._sensor.data

        def __getattr__(self, item):
            if item in self.__dict__:
                return self.__dict__[item]

            if hasattr(self._sensor, item):
                return getattr(self._sensor, item)

            raise AttributeError(item)


class MeterPulse(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)

        if not hasattr(self, '_cls_ids'):
            self._cls_ids = []

        self._cls_ids += [COMMAND_CLASS_METER_PULSE]
        print_not_implemented('COMMAND_CLASS_METER_PULSE', self)


class MeterTblConfig(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)

        if not hasattr(self, '_cls_ids'):
            self._cls_ids = []

        self._cls_ids += [COMMAND_CLASS_METER_TBL_CONFIG]
        print_not_implemented('COMMAND_CLASS_METER_TBL_CONFIG', self)


class MeterTblMonitor(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)

        if not hasattr(self, '_cls_ids'):
            self._cls_ids = []

        self._cls_ids += [COMMAND_CLASS_METER_TBL_MONITOR]
        print_not_implemented('COMMAND_CLASS_METER_TBL_MONITOR', self)


class MeterTblPush(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)

        if not hasattr(self, '_cls_ids'):
            self._cls_ids = []

        self._cls_ids += [COMMAND_CLASS_METER_TBL_PUSH]
        print_not_implemented('COMMAND_CLASS_METER_TBL_PUSH', self)


class MtpWindowCovering(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)

        if not hasattr(self, '_cls_ids'):
            self._cls_ids = []

        self._cls_ids += [COMMAND_CLASS_MTP_WINDOW_COVERING]
        print_not_implemented(
            'COMMAND_CLASS_MTP_WINDOW_COVERING',
            self
        )


class MultiChannel(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)

        if not hasattr(self, '_cls_ids'):
            self._cls_ids = []

        self._cls_ids += [COMMAND_CLASS_MULTI_CHANNEL]
        print_not_implemented('COMMAND_CLASS_MULTI_CHANNEL', self)


class MultiChannelAssociation(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)

        if not hasattr(self, '_cls_ids'):
            self._cls_ids = []

        self._cls_ids += [COMMAND_CLASS_MULTI_CHANNEL_ASSOCIATION]
        print_not_implemented(
            'COMMAND_CLASS_MULTI_CHANNEL_ASSOCIATION',
            self
        )


class MultiCmd(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)

        if not hasattr(self, '_cls_ids'):
            self._cls_ids = []

        self._cls_ids += [COMMAND_CLASS_MULTI_CMD]
        print_not_implemented('COMMAND_CLASS_MULTI_CMD', self)


class NetworkManagementBasic(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)

        if not hasattr(self, '_cls_ids'):
            self._cls_ids = []

        self._cls_ids += [COMMAND_CLASS_NETWORK_MANAGEMENT_BASIC]
        print_not_implemented(
            'COMMAND_CLASS_NETWORK_MANAGEMENT_BASIC',
            self
        )


class NetworkManagementInclusion(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)

        if not hasattr(self, '_cls_ids'):
            self._cls_ids = []

        self._cls_ids += [COMMAND_CLASS_NETWORK_MANAGEMENT_INCLUSION]
        print_not_implemented(
            'COMMAND_CLASS_NETWORK_MANAGEMENT_INCLUSION',
            self
        )


class NetworkManagementPrimary(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)

        if not hasattr(self, '_cls_ids'):
            self._cls_ids = []

        self._cls_ids += [COMMAND_CLASS_NETWORK_MANAGEMENT_PRIMARY]
        print_not_implemented(
            'COMMAND_CLASS_NETWORK_MANAGEMENT_PRIMARY',
            self
        )


class NetworkManagementProxy(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)

        if not hasattr(self, '_cls_ids'):
            self._cls_ids = []

        self._cls_ids += [COMMAND_CLASS_NETWORK_MANAGEMENT_PROXY]
        print_not_implemented(
            'COMMAND_CLASS_NETWORK_MANAGEMENT_PROXY',
            self
        )


class NodeNaming(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)

        if not hasattr(self, '_cls_ids'):
            self._cls_ids = []

        self._cls_ids += [COMMAND_CLASS_NODE_NAMING]
        print_not_implemented('COMMAND_CLASS_NODE_NAMING', self)


class NodeProvisioning(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)

        if not hasattr(self, '_cls_ids'):
            self._cls_ids = []

        self._cls_ids += [COMMAND_CLASS_NODE_PROVISIONING]
        print_not_implemented('COMMAND_CLASS_NODE_PROVISIONING', self)


class Notification(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)

        if not hasattr(self, '_cls_ids'):
            self._cls_ids = []

        self._cls_ids += [COMMAND_CLASS_NOTIFICATION]
        print_not_implemented('COMMAND_CLASS_NOTIFICATION', self)


class NoOperation(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)

        if not hasattr(self, '_cls_ids'):
            self._cls_ids = []

        self._cls_ids += [COMMAND_CLASS_NO_OPERATION]
        print_not_implemented('COMMAND_CLASS_NO_OPERATION', self)


class Powerlevel(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)

        if not hasattr(self, '_cls_ids'):
            self._cls_ids = []

        self._cls_ids += [COMMAND_CLASS_POWERLEVEL]
        print_not_implemented('COMMAND_CLASS_POWERLEVEL', self)

    @property
    def power_level(self):
        for value in self.values.values():
            if (
                value == COMMAND_CLASS_POWERLEVEL and
                value.label == 'Test Powerlevel'
            ):
                return value.data

    @power_level.setter
    def power_level(self, value):
        for val in self.values.values():
            if (
                val == COMMAND_CLASS_POWERLEVEL and
                val.label == 'Powerlevel'
            ):
                val.data = value

    def test_power_level(self, db):
        for value in self.values.values():
            if (
                value == COMMAND_CLASS_POWERLEVEL and
                value.label == 'Test Powerlevel'
            ):
                value.data = db
                break

    def test_node(self):
        for val in self.values.values():
            if (
                val == COMMAND_CLASS_POWERLEVEL and
                val.label == 'Test Node'
            ):
                val.data = 1

    @property
    def acked_frames(self):
        for value in self.values.values():
            if (
                value == COMMAND_CLASS_POWERLEVEL and
                value.label == 'Acked Frames'
            ):
                return value.data

    @property
    def frame_count(self):
        for value in self.values.values():
            if (
                value == COMMAND_CLASS_POWERLEVEL and
                value.label == 'Frame Count'
            ):
                return value.data


class Prepayment(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)

        if not hasattr(self, '_cls_ids'):
            self._cls_ids = []

        self._cls_ids += [COMMAND_CLASS_PREPAYMENT]
        print_not_implemented('COMMAND_CLASS_PREPAYMENT', self)


class PrepaymentEncapsulation(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)

        if not hasattr(self, '_cls_ids'):
            self._cls_ids = []

        self._cls_ids += [COMMAND_CLASS_PREPAYMENT_ENCAPSULATION]
        print_not_implemented(
            'COMMAND_CLASS_PREPAYMENT_ENCAPSULATION',
            self
        )


class Proprietary(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)

        if not hasattr(self, '_cls_ids'):
            self._cls_ids = []

        self._cls_ids += [COMMAND_CLASS_PROPRIETARY]
        print_not_implemented('COMMAND_CLASS_PROPRIETARY', self)


class Protection(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)

        if not hasattr(self, '_cls_ids'):
            self._cls_ids = []

        self._cls_ids += [COMMAND_CLASS_PROTECTION]
        print_not_implemented('COMMAND_CLASS_PROTECTION', self)

    @property
    def protections(self):
        res = []
        for value in self.values.values():
            if value == COMMAND_CLASS_PROTECTION:
                res += [self.Protection(value)]

        return res


    class Protection(object):

        def __init__(self, protection):
            self._protection = protection

        @property
        def value(self):
            return self._protection.data

        def __getattr__(self, item):
            if item in self.__dict__:
                return self.__dict__[item]

            if hasattr(self._sensor, item):
                return getattr(self._protection, item)

            raise AttributeError(item)


class RateTblConfig(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)

        if not hasattr(self, '_cls_ids'):
            self._cls_ids = []

        self._cls_ids += [COMMAND_CLASS_RATE_TBL_CONFIG]
        print_not_implemented('COMMAND_CLASS_RATE_TBL_CONFIG', self)


class RateTblMonitor(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)

        if not hasattr(self, '_cls_ids'):
            self._cls_ids = []

        self._cls_ids += [COMMAND_CLASS_RATE_TBL_MONITOR]
        print_not_implemented('COMMAND_CLASS_RATE_TBL_MONITOR', self)


class RemoteAssociation(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)

        if not hasattr(self, '_cls_ids'):
            self._cls_ids = []

        self._cls_ids += [COMMAND_CLASS_REMOTE_ASSOCIATION]
        print_not_implemented('COMMAND_CLASS_REMOTE_ASSOCIATION', self)


class RemoteAssociationActivate(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)

        if not hasattr(self, '_cls_ids'):
            self._cls_ids = []

        self._cls_ids += [COMMAND_CLASS_REMOTE_ASSOCIATION_ACTIVATE]
        print_not_implemented(
            'COMMAND_CLASS_REMOTE_ASSOCIATION_ACTIVATE',
            self
        )


class SceneActivation(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)

        if not hasattr(self, '_cls_ids'):
            self._cls_ids = []

        self._cls_ids += [COMMAND_CLASS_SCENE_ACTIVATION]
        print_not_implemented('COMMAND_CLASS_SCENE_ACTIVATION', self)


class SceneActuatorConf(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)

        if not hasattr(self, '_cls_ids'):
            self._cls_ids = []

        self._cls_ids += [COMMAND_CLASS_SCENE_ACTUATOR_CONF]
        print_not_implemented(
            'COMMAND_CLASS_SCENE_ACTUATOR_CONF',
            self
        )


class SceneControllerConf(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)

        if not hasattr(self, '_cls_ids'):
            self._cls_ids = []

        self._cls_ids += [COMMAND_CLASS_SCENE_CONTROLLER_CONF]
        print_not_implemented(
            'COMMAND_CLASS_SCENE_CONTROLLER_CONF',
            self
        )


class Schedule(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)

        if not hasattr(self, '_cls_ids'):
            self._cls_ids = []

        self._cls_ids += [COMMAND_CLASS_SCHEDULE]
        print_not_implemented('COMMAND_CLASS_SCHEDULE', self)


class ScheduleEntryLock(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)

        if not hasattr(self, '_cls_ids'):
            self._cls_ids = []

        self._cls_ids += [COMMAND_CLASS_SCHEDULE_ENTRY_LOCK]
        print_not_implemented(
            'COMMAND_CLASS_SCHEDULE_ENTRY_LOCK',
            self
        )


class ScreenAttributes(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)

        if not hasattr(self, '_cls_ids'):
            self._cls_ids = []

        self._cls_ids += [COMMAND_CLASS_SCREEN_ATTRIBUTES]
        print_not_implemented('COMMAND_CLASS_SCREEN_ATTRIBUTES', self)


class ScreenMd(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)

        if not hasattr(self, '_cls_ids'):
            self._cls_ids = []

        self._cls_ids += [COMMAND_CLASS_SCREEN_MD]
        print_not_implemented('COMMAND_CLASS_SCREEN_MD', self)


class Security(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)

        if not hasattr(self, '_cls_ids'):
            self._cls_ids = []

        self._cls_ids += [COMMAND_CLASS_SECURITY]
        print_not_implemented('COMMAND_CLASS_SECURITY', self)


class Security2(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)

        if not hasattr(self, '_cls_ids'):
            self._cls_ids = []

        self._cls_ids += [COMMAND_CLASS_SECURITY_2]
        print_not_implemented('COMMAND_CLASS_SECURITY_2', self)


class SecurityScheme0Mark(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)

        if not hasattr(self, '_cls_ids'):
            self._cls_ids = []

        self._cls_ids += [COMMAND_CLASS_SECURITY_SCHEME0_MARK]
        print_not_implemented(
            'COMMAND_CLASS_SECURITY_SCHEME0_MARK',
            self
        )


class SensorAlarm(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)

        if not hasattr(self, '_cls_ids'):
            self._cls_ids = []

        self._cls_ids += [COMMAND_CLASS_SENSOR_ALARM]
        print_not_implemented('COMMAND_CLASS_SENSOR_ALARM', self)


class SensorBinary(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)

        if not hasattr(self, '_cls_ids'):
            self._cls_ids = []

        self._cls_ids += [COMMAND_CLASS_SENSOR_BINARY]
        print_not_implemented('COMMAND_CLASS_SENSOR_BINARY', self)

    @property
    def binary_sensors(self):
        res = []
        for value in self.values.values():
            if value == COMMAND_CLASS_SENSOR_BINARY:
                res += [self.SensorBinary(value)]
        return res


    class SensorBinary(object):

        def __init__(self, sensor):
            self._sensor = sensor

        @property
        def value(self):
            return self._sensor.data

        def __getattr__(self, item):
            if item in self.__dict__:
                return self.__dict__[item]

            if hasattr(self._sensor, item):
                return getattr(self._sensor, item)

            raise AttributeError(item)


class SensorConfiguration(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)

        if not hasattr(self, '_cls_ids'):
            self._cls_ids = []

        self._cls_ids += [COMMAND_CLASS_SENSOR_CONFIGURATION]
        print_not_implemented(
            'COMMAND_CLASS_SENSOR_CONFIGURATION',
            self
        )


class SensorMultilevel(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)

        if not hasattr(self, '_cls_ids'):
            self._cls_ids = []

        self._cls_ids += [COMMAND_CLASS_SENSOR_MULTILEVEL]
        print_not_implemented('COMMAND_CLASS_SENSOR_MULTILEVEL', self)

    @property
    def multilevel_sensors(self):
        res = []
        for value in self.values.values():
            if value == COMMAND_CLASS_SENSOR_MULTILEVEL:
                res += [self.SensorMultilevel(value)]
        return res


    class SensorMultilevel(object):

        def __init__(self, sensor):
            self._sensor = sensor

        @property
        def value(self):
            return self._sensor.data

        def __getattr__(self, item):
            if item in self.__dict__:
                return self.__dict__[item]

            if hasattr(self._sensor, item):
                return getattr(self._sensor, item)

            raise AttributeError(item)


class SilenceAlarm(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)

        if not hasattr(self, '_cls_ids'):
            self._cls_ids = []

        self._cls_ids += [COMMAND_CLASS_SILENCE_ALARM]
        print_not_implemented('COMMAND_CLASS_SILENCE_ALARM', self)


class SimpleAvControl(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)

        if not hasattr(self, '_cls_ids'):
            self._cls_ids = []

        self._cls_ids += [COMMAND_CLASS_SIMPLE_AV_CONTROL]
        print_not_implemented('COMMAND_CLASS_SIMPLE_AV_CONTROL', self)


class SoundSwitch(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)

        if not hasattr(self, '_cls_ids'):
            self._cls_ids = []

        self._cls_ids += [COMMAND_CLASS_SOUND_SWITCH]
        print_not_implemented('COMMAND_CLASS_SOUND_SWITCH', self)


class Supervision(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)

        if not hasattr(self, '_cls_ids'):
            self._cls_ids = []

        self._cls_ids += [COMMAND_CLASS_SUPERVISION]
        print_not_implemented('COMMAND_CLASS_SUPERVISION', self)


class SwitchAll(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)

        if not hasattr(self, '_cls_ids'):
            self._cls_ids = []

        self._cls_ids += [COMMAND_CLASS_SWITCH_ALL]
        print_not_implemented('COMMAND_CLASS_SWITCH_ALL', self)

    @property
    def switch_all(self):
        switch_all = list(
            value for value in self.values.values()
            if value == COMMAND_CLASS_SWITCH_ALL
        )
        if switch_all:
            return self.SwitchAll(switch_all)


    class SwitchAll(object):

        def __init__(self, switch_all):
            self._switch_all = switch_all

        def __contains__(self, item):
            return hasattr(self, item)

        def __iter__(self):
            for switch in self._switch_all:
                yield switch

        def __getattr__(self, item):
            if item in self.__dict__:
                return self.__dict__[item]

            label = item.replace('_', ' ').title()
            for switch in self._switch_all:
                if label == switch.label:
                    return switch.data

            raise AttributeError(item)

        def __setattr__(self, key, value):
            if key.startswith('_'):
                object.__setattr__(self, key, value)
            else:
                if key in self:
                    label = key.replace('_', ' ').title()
                    for switch in self._switch_all:
                        if (
                            switch.label == label and
                            not switch.readonly
                        ):
                            switch.data = value
                else:
                    raise AttributeError(key)


class SwitchBinary(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)

        if not hasattr(self, '_cls_ids'):
            self._cls_ids = []

        self._cls_ids += [COMMAND_CLASS_SWITCH_BINARY]
        print_not_implemented('COMMAND_CLASS_SWITCH_BINARY', self)

    @property
    def status(self):
        for value in self.values.values():
            if (
                value == COMMAND_CLASS_SWITCH_BINARY and
                value.label == 'Status'
            ):
                return value.data

    @status.setter
    def status(self, value):
        for val in self.values.values():
            if (
                val == COMMAND_CLASS_SWITCH_BINARY and
                val.label == 'Status'
            ):
                    val.data = value
                    break


class SwitchColor(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)

        if not hasattr(self, '_cls_ids'):
            self._cls_ids = []

        self._cls_ids += [COMMAND_CLASS_SWITCH_COLOR]
        print_not_implemented('COMMAND_CLASS_SWITCH_COLOR', self)

    @property
    def color(self):
        for value in self.values.values():
            if value == COMMAND_CLASS_SWITCH_COLOR:
                return value.data

    @color.setter
    def color(self, value):
        for val in self.values.values():
            if val == COMMAND_CLASS_SWITCH_COLOR:
                val.data = value
                break


class SwitchMultilevel(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)

        if not hasattr(self, '_cls_ids'):
            self._cls_ids = []

        self._cls_ids += [COMMAND_CLASS_SWITCH_MULTILEVEL]
        print_not_implemented('COMMAND_CLASS_SWITCH_MULTILEVEL', self)
        self._ramping_event = threading.Event()
        self._ramping_lock = threading.Lock()

    @property
    def status(self):
        for value in self.values.values():
            if (
                value == COMMAND_CLASS_SWITCH_MULTILEVEL and
                value.label == 'Level'
            ):
                return value.data > value.min

    @status.setter
    def status(self, value):
        value = bool(value)
        for val in self.values.values():
            if val == COMMAND_CLASS_SWITCH_MULTILEVEL:
                if val.label == 'Bright' and value:
                    val.data = value
                    break
                elif val.label == 'Dim' and value:
                    val.data = value
                    break
        else:
            for val in self.values.values():
                if (
                    val == COMMAND_CLASS_SWITCH_MULTILEVEL and
                    val.label == 'Level'
                ):
                    if value and val.data == val.min:
                        val.data = val.max
                    elif not value and val.data > val.min:
                        val.data = val.min
                    break

    def ramp_up(self, level, speed=0.17, step=1):
        for value in self.values.values():
            if (
                value == COMMAND_CLASS_SWITCH_MULTILEVEL and
                value.label == 'Level'
            ):
                break
        else:
            return

        self._ramping_event.set()

        def do(val, stp, spd, lvl):
            with self._ramping_lock:
                self._ramping_event.clear()

                while not self._ramping_event.isSet():

                    new_level = val.data + stp
                    start = time.time()

                    with val as event:
                        val.data = new_level
                        event.wait(spd)

                    if val.data >= lvl:
                        break

                    stop = time.time()

                    finish = (stop - start) * 1000
                    if finish < spd * 1000:
                        self._ramping_event.wait(
                            ((spd * 1000) - finish) / 1000)

        t = threading.Thread(target=do, args=(value, step, speed, level))
        t.daemon = True
        t.start()

    def ramp_down(self, level, speed=0.17, step=1):

        for value in self.values.values():
            if (
                value == COMMAND_CLASS_SWITCH_MULTILEVEL and
                value.label == 'Level'
            ):
                break
        else:
            return

        self._ramping_event.set()

        def do(val, stp, spd, lvl):
            with self._ramping_lock:
                self._ramping_event.clear()

                while not self._ramping_event.isSet():

                    new_level = val.data - stp
                    start = time.time()

                    with val as event:
                        val.data = new_level
                        event.wait(spd)

                    if val.data <= lvl:
                        break

                    stop = time.time()

                    finish = (stop - start) * 1000
                    if finish < spd * 1000:
                        self._ramping_event.wait(
                            ((spd * 1000) - finish) / 1000)

        t = threading.Thread(target=do, args=(value, step, speed, level))
        t.daemon = True
        t.start()

    def bright(self):
        for value in self.values.values():
            if (
                value == COMMAND_CLASS_SWITCH_MULTILEVEL and
                value.label == 'Bright'
            ):
                value.data = True
                break

    def dim(self):
        for value in self.values.values():
            if (
                value == COMMAND_CLASS_SWITCH_MULTILEVEL and
                value.label == 'Dim'
            ):
                value.data = True
                break

    @property
    def level(self):
        for value in self.values.values():
            if (
                value == COMMAND_CLASS_SWITCH_MULTILEVEL and
                value.label == 'Level'
            ):
                return value.data

    @level.setter
    def level(self, value):
        for val in self.values.values():
            if (
                val == COMMAND_CLASS_SWITCH_MULTILEVEL and
                val.label == 'Level'
            ):
                if 99 >= value >= 0 or value == 255:
                    val.data = value
                    break
                else:
                    raise ValueError(
                        'Value {0} not within range {1} - {2}'.format(
                            value,
                            val.min,
                            val.max
                        )
                    )

    @property
    def start_level(self):
        for value in self.values.values():
            if (
                value == COMMAND_CLASS_SWITCH_MULTILEVEL and
                value.label == 'Start Level'
            ):
                return value.data

    @start_level.setter
    def start_level(self, value):
        for val in self.values.values():
            if (
                val == COMMAND_CLASS_SWITCH_MULTILEVEL and
                val.label == 'Start Level'
            ):
                if val.max >= value >= val.min:
                    val.data = value
                    break
                else:
                    raise ValueError(
                        'Value {0} not within range {1} - {2}'.format(
                            value,
                            val.min,
                            val.max
                        )
                    )

    @property
    def ignore_start_level(self):
        for value in self.values.values():
            if (
                value == COMMAND_CLASS_SWITCH_MULTILEVEL and
                value.label == 'Ignore Start Level'
            ):
                return value.data

    @ignore_start_level.setter
    def ignore_start_level(self, value):
        for val in self.values.values():
            if (
                val == COMMAND_CLASS_SWITCH_MULTILEVEL and
                val.label == 'Ignore Start Level'
            ):
                val.data = value
                break


class SwitchToggleBinary(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)

        if not hasattr(self, '_cls_ids'):
            self._cls_ids = []

        self._cls_ids += [COMMAND_CLASS_SWITCH_TOGGLE_BINARY]
        print_not_implemented(
            'COMMAND_CLASS_SWITCH_TOGGLE_BINARY',
            self
        )

    def toggle(self):
        for value in self.values.values():
            if (
                value == COMMAND_CLASS_SWITCH_BINARY and
                value.label == 'Status'
            ):
                value.data = ~value.data
                return

    def toggle_all(self):
        if COMMAND_CLASS_MULTI_CHANNEL in self._cls_ids:
            for value in self.values.values():
                if (
                    value == COMMAND_CLASS_SWITCH_BINARY and
                    value.label == 'Status'
                ):
                    value.data = ~value.data


class SwitchToggleMultilevel(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)

        if not hasattr(self, '_cls_ids'):
            self._cls_ids = []

        self._cls_ids += [COMMAND_CLASS_SWITCH_TOGGLE_MULTILEVEL]
        print_not_implemented(
            'COMMAND_CLASS_SWITCH_TOGGLE_MULTILEVEL',
            self
        )

    def toggle(self):
        for value in self.values.values():
            if (
                value == COMMAND_CLASS_SWITCH_MULTILEVEL and
                value.label == 'Level'
            ):
                if value.data > value.min:
                    value.data = value.min
                else:
                    value.data = value.max
                return

    def toggle_all(self):
        if COMMAND_CLASS_MULTI_CHANNEL in self._cls_ids:
            for value in self.values.values():
                if (
                    value == COMMAND_CLASS_SWITCH_MULTILEVEL and
                    value.label == 'Level'
                ):
                    if value.data > value.min:
                        value.data = value.min
                    else:
                        value.data = value.max


class TariffConfig(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)

        if not hasattr(self, '_cls_ids'):
            self._cls_ids = []

        self._cls_ids += [COMMAND_CLASS_TARIFF_CONFIG]
        print_not_implemented('COMMAND_CLASS_TARIFF_CONFIG', self)


class TariffTblMonitor(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)

        if not hasattr(self, '_cls_ids'):
            self._cls_ids = []

        self._cls_ids += [COMMAND_CLASS_TARIFF_TBL_MONITOR]
        print_not_implemented('COMMAND_CLASS_TARIFF_TBL_MONITOR', self)


class ThermostatFanMode(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)

        if not hasattr(self, '_cls_ids'):
            self._cls_ids = []

        self._cls_ids += [COMMAND_CLASS_THERMOSTAT_FAN_MODE]

    @property
    def fan_mode(self):
        for value in self.values.values():
            if (
                value == COMMAND_CLASS_THERMOSTAT_FAN_MODE and
                value.label == 'Fan Mode'
            ):
                return value.data

    @fan_mode.setter
    def fan_mode(self, value):
        for val in self.values.values():
            if (
                val == COMMAND_CLASS_THERMOSTAT_FAN_MODE and
                val.label == 'Fan Mode'
            ):
                val.data = value


class ThermostatFanState(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)

        if not hasattr(self, '_cls_ids'):
            self._cls_ids = []

        self._cls_ids += [COMMAND_CLASS_THERMOSTAT_FAN_STATE]

    @property
    def fan_state(self):
        for value in self.values.values():
            if (
                value == COMMAND_CLASS_THERMOSTAT_FAN_STATE and
                value.label == 'Fan State'
            ):
                return value.data


class ThermostatMode(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)

        if not hasattr(self, '_cls_ids'):
            self._cls_ids = []

        self._cls_ids += [COMMAND_CLASS_THERMOSTAT_MODE]

    @property
    def operating_mode(self):
        for value in self.values.values():
            if (
                value == COMMAND_CLASS_THERMOSTAT_MODE
                and value.label == 'Mode'
            ):
                return value.data

    @operating_mode.setter
    def operating_mode(self, value):
        for val in self.values.values():
            if (
                val == COMMAND_CLASS_THERMOSTAT_MODE
                and val.label == 'Mode'
            ):
                val.data = value


class ThermostatOperatingState(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)

        if not hasattr(self, '_cls_ids'):
            self._cls_ids = []

        self._cls_ids += [COMMAND_CLASS_THERMOSTAT_OPERATING_STATE]

    @property
    def operating_state(self):
        for value in self.values.values():
            if (
                value == COMMAND_CLASS_THERMOSTAT_OPERATING_STATE
                and value.label == 'Operating State'
            ):
                return value.data


class ThermostatSetback(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)

        if not hasattr(self, '_cls_ids'):
            self._cls_ids = []

        self._cls_ids += [COMMAND_CLASS_THERMOSTAT_SETBACK]
        print_not_implemented('COMMAND_CLASS_THERMOSTAT_SETBACK', self)


class ThermostatSetpoint(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)

        if not hasattr(self, '_cls_ids'):
            self._cls_ids = []

        self._cls_ids += [COMMAND_CLASS_THERMOSTAT_SETPOINT]

    @property
    def heat_setpoint(self):
        for value in self.values.values():
            if (
                value == COMMAND_CLASS_THERMOSTAT_SETPOINT and
                value.label == 'Heating 1'
            ):
                return value.data

    @heat_setpoint.setter
    def heat_setpoint(self, value):

        for val in self.values.values():
            if (
                val == COMMAND_CLASS_THERMOSTAT_SETPOINT and
                val.label == 'Heating 1'
            ):
                val.data = value

    @property
    def cool_setpoint(self):
        for value in self.values.values():
            if (
                value == COMMAND_CLASS_THERMOSTAT_SETPOINT and
                value.label == 'Cooling 1'
            ):
                return value.data

    @cool_setpoint.setter
    def cool_setpoint(self, value):

        for val in self.values.values():
            if (
                val == COMMAND_CLASS_THERMOSTAT_SETPOINT and
                val.label == 'Cooling 1'
            ):
                val.data = value


class Time(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)

        if not hasattr(self, '_cls_ids'):
            self._cls_ids = []

        self._cls_ids += [COMMAND_CLASS_TIME]
        print_not_implemented('COMMAND_CLASS_TIME', self)


class TimeParameters(CommandClassBase):
    VALUE_INDEX_TIME_PARAMETERS_DATE = 0x0
    VALUE_INDEX_TIME_PARAMETERS_TIME = 0x1
    VALUE_INDEX_TIME_PARAMETERS_SET = 0x3
    VALUE_INDEX_TIME_PARAMETERS_REFRESH = 0x4

    def __init__(self):
        CommandClassBase.__init__(self)

        if not hasattr(self, '_cls_ids'):
            self._cls_ids = []

        self._cls_ids += [COMMAND_CLASS_TIME_PARAMETERS]
        print_not_implemented('COMMAND_CLASS_TIME_PARAMETERS', self)


class TransportService(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)

        if not hasattr(self, '_cls_ids'):
            self._cls_ids = []

        self._cls_ids += [COMMAND_CLASS_TRANSPORT_SERVICE]
        print_not_implemented('COMMAND_CLASS_TRANSPORT_SERVICE', self)


class UserCode(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)

        if not hasattr(self, '_cls_ids'):
            self._cls_ids = []

        self._cls_ids += [COMMAND_CLASS_USER_CODE]
        print_not_implemented('COMMAND_CLASS_USER_CODE', self)


class Version(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)

        if not hasattr(self, '_cls_ids'):
            self._cls_ids = []

        self._cls_ids += [COMMAND_CLASS_VERSION]


class WakeUp(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)

        if not hasattr(self, '_cls_ids'):
            self._cls_ids = []

        self._cls_ids += [COMMAND_CLASS_WAKE_UP]
        print_not_implemented('COMMAND_CLASS_WAKE_UP', self)

    @property
    def can_wake_up(self):
        for value in self.values.values():
            if value == COMMAND_CLASS_WAKE_UP:
                return True

        return False


class WindowCovering(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)

        if not hasattr(self, '_cls_ids'):
            self._cls_ids = []

        self._cls_ids += [COMMAND_CLASS_WINDOW_COVERING]
        print_not_implemented('COMMAND_CLASS_WINDOW_COVERING', self)


class ZIP(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)

        if not hasattr(self, '_cls_ids'):
            self._cls_ids = []

        self._cls_ids += [COMMAND_CLASS_ZIP]
        print_not_implemented('COMMAND_CLASS_ZIP', self)


class ZIP6Lowpan(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)

        if not hasattr(self, '_cls_ids'):
            self._cls_ids = []

        self._cls_ids += [COMMAND_CLASS_ZIP_6LOWPAN]
        print_not_implemented('COMMAND_CLASS_ZIP_6LOWPAN', self)


class ZIPGateway(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)

        if not hasattr(self, '_cls_ids'):
            self._cls_ids = []

        self._cls_ids += [COMMAND_CLASS_ZIP_GATEWAY]
        print_not_implemented('COMMAND_CLASS_ZIP_GATEWAY', self)


class ZIPNaming(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)

        if not hasattr(self, '_cls_ids'):
            self._cls_ids = []

        self._cls_ids += [COMMAND_CLASS_ZIP_NAMING]
        print_not_implemented('COMMAND_CLASS_ZIP_NAMING', self)


class ZIPND(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)

        if not hasattr(self, '_cls_ids'):
            self._cls_ids = []

        self._cls_ids += [COMMAND_CLASS_ZIP_ND]
        print_not_implemented('COMMAND_CLASS_ZIP_ND', self)


class ZIPPortal(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)

        if not hasattr(self, '_cls_ids'):
            self._cls_ids = []

        self._cls_ids += [COMMAND_CLASS_ZIP_PORTAL]
        print_not_implemented('COMMAND_CLASS_ZIP_PORTAL', self)


class ZwaveplusInfo(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)

        if not hasattr(self, '_cls_ids'):
            self._cls_ids = []

        self._cls_ids += [COMMAND_CLASS_ZWAVEPLUS_INFO]
        print_not_implemented('COMMAND_CLASS_ZWAVEPLUS_INFO', self)


class NetworkManagementInstallationMaintenance(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)

        if not hasattr(self, '_cls_ids'):
            self._cls_ids = []

        self._cls_ids += [NETWORK_MANAGEMENT_INSTALLATION_MAINTENANCE]
        print_not_implemented(
            'NETWORK_MANAGEMENT_INSTALLATION_MAINTENANCE',
            self
        )


class EmptyCommandClass(CommandClassBase):
    pass


class CommandClasses(dict):

    def __init__(self):

        import sys
        mod = sys.modules[__name__]

        kwargs = {
            COMMAND_CLASS_ALARM: Alarm,
            COMMAND_CLASS_ANTITHEFT: Antitheft,
            COMMAND_CLASS_APPLICATION_CAPABILITY: ApplicationCapability,
            COMMAND_CLASS_APPLICATION_STATUS: ApplicationStatus,
            COMMAND_CLASS_ASSOCIATION: Association,
            COMMAND_CLASS_ASSOCIATION_COMMAND_CONFIGURATION: (
                AssociationCommandConfiguration
            ),
            COMMAND_CLASS_ASSOCIATION_GRP_INFO: AssociationGrpInfo,
            COMMAND_CLASS_BARRIER_OPERATOR: BarrierOperator,
            COMMAND_CLASS_BASIC: Basic,
            COMMAND_CLASS_BASIC_TARIFF_INFO: BasicTariffInfo,
            COMMAND_CLASS_BASIC_WINDOW_COVERING: BasicWindowCovering,
            COMMAND_CLASS_BATTERY: Battery,
            COMMAND_CLASS_CENTRAL_SCENE: CentralScene,
            COMMAND_CLASS_CLIMATE_CONTROL_SCHEDULE: ClimateControlSchedule,
            COMMAND_CLASS_CLOCK: Clock,
            COMMAND_CLASS_CONFIGURATION: Configuration,
            COMMAND_CLASS_CONTROLLER_REPLICATION: ControllerReplication,
            COMMAND_CLASS_CRC_16_ENCAP: Crc16Encap,
            COMMAND_CLASS_DCP_CONFIG: DcpConfig,
            COMMAND_CLASS_DCP_MONITOR: DcpMonitor,
            COMMAND_CLASS_DEVICE_RESET_LOCALLY: DeviceResetLocally,
            COMMAND_CLASS_DOOR_LOCK: DoorLock,
            COMMAND_CLASS_DOOR_LOCK_LOGGING: DoorLockLogging,
            COMMAND_CLASS_ENERGY_PRODUCTION: EnergyProduction,
            COMMAND_CLASS_ENTRY_CONTROL: EntryControl,
            COMMAND_CLASS_FIRMWARE_UPDATE_MD: FirmwareUpdateMd,
            COMMAND_CLASS_GEOGRAPHIC_LOCATION: GeographicLocation,
            COMMAND_CLASS_GROUPING_NAME: GroupingName,
            COMMAND_CLASS_HAIL: Hail,
            COMMAND_CLASS_HRV_CONTROL: HrvControl,
            COMMAND_CLASS_HRV_STATUS: HrvStatus,
            COMMAND_CLASS_HUMIDITY_CONTROL_MODE: HumidityControlMode,
            COMMAND_CLASS_HUMIDITY_CONTROL_OPERATING_STATE: (
                HumidityControlOperatingState
            ),
            COMMAND_CLASS_HUMIDITY_CONTROL_SETPOINT: HumidityControlSetpoint,
            COMMAND_CLASS_INCLUSION_CONTROLLER: InclusionController,
            COMMAND_CLASS_INDICATOR: Indicator,
            COMMAND_CLASS_IP_ASSOCIATION: IpAssociation,
            COMMAND_CLASS_IP_CONFIGURATION: IpConfiguration,
            COMMAND_CLASS_IRRIGATION: Irrigation,
            COMMAND_CLASS_LANGUAGE: Language,
            COMMAND_CLASS_LOCK: Lock,
            COMMAND_CLASS_MAILBOX: Mailbox,
            COMMAND_CLASS_MANUFACTURER_PROPRIETARY: ManufacturerProprietary,
            COMMAND_CLASS_MANUFACTURER_SPECIFIC: ManufacturerSpecific,
            COMMAND_CLASS_MARK: Mark,
            COMMAND_CLASS_METER: Meter,
            COMMAND_CLASS_METER_PULSE: MeterPulse,
            COMMAND_CLASS_METER_TBL_CONFIG: MeterTblConfig,
            COMMAND_CLASS_METER_TBL_MONITOR: MeterTblMonitor,
            COMMAND_CLASS_METER_TBL_PUSH: MeterTblPush,
            COMMAND_CLASS_MTP_WINDOW_COVERING: MtpWindowCovering,
            COMMAND_CLASS_MULTI_CHANNEL: MultiChannel,
            COMMAND_CLASS_MULTI_CHANNEL_ASSOCIATION: MultiChannelAssociation,
            COMMAND_CLASS_MULTI_CMD: MultiCmd,
            COMMAND_CLASS_NETWORK_MANAGEMENT_BASIC: NetworkManagementBasic,
            COMMAND_CLASS_NETWORK_MANAGEMENT_INCLUSION: (
                NetworkManagementInclusion
            ),
            COMMAND_CLASS_NETWORK_MANAGEMENT_PRIMARY: NetworkManagementPrimary,
            COMMAND_CLASS_NETWORK_MANAGEMENT_PROXY: NetworkManagementProxy,
            COMMAND_CLASS_NODE_NAMING: NodeNaming,
            COMMAND_CLASS_NODE_PROVISIONING: NodeProvisioning,
            COMMAND_CLASS_NOTIFICATION: Notification,
            COMMAND_CLASS_NO_OPERATION: NoOperation,
            COMMAND_CLASS_POWERLEVEL: Powerlevel,
            COMMAND_CLASS_PREPAYMENT: Prepayment,
            COMMAND_CLASS_PREPAYMENT_ENCAPSULATION: PrepaymentEncapsulation,
            COMMAND_CLASS_PROPRIETARY: Proprietary,
            COMMAND_CLASS_PROTECTION: Protection,
            COMMAND_CLASS_RATE_TBL_CONFIG: RateTblConfig,
            COMMAND_CLASS_RATE_TBL_MONITOR: RateTblMonitor,
            COMMAND_CLASS_REMOTE_ASSOCIATION: RemoteAssociation,
            COMMAND_CLASS_REMOTE_ASSOCIATION_ACTIVATE: (
                RemoteAssociationActivate
            ),
            COMMAND_CLASS_SCENE_ACTIVATION: SceneActivation,
            COMMAND_CLASS_SCENE_ACTUATOR_CONF: SceneActuatorConf,
            COMMAND_CLASS_SCENE_CONTROLLER_CONF: SceneControllerConf,
            COMMAND_CLASS_SCHEDULE: Schedule,
            COMMAND_CLASS_SCHEDULE_ENTRY_LOCK: ScheduleEntryLock,
            COMMAND_CLASS_SCREEN_ATTRIBUTES: ScreenAttributes,
            COMMAND_CLASS_SCREEN_MD: ScreenMd,
            COMMAND_CLASS_SECURITY: Security,
            COMMAND_CLASS_SECURITY_2: Security2,
            COMMAND_CLASS_SECURITY_SCHEME0_MARK: SecurityScheme0Mark,
            COMMAND_CLASS_SENSOR_ALARM: SensorAlarm,
            COMMAND_CLASS_SENSOR_BINARY: SensorBinary,
            COMMAND_CLASS_SENSOR_CONFIGURATION: SensorConfiguration,
            COMMAND_CLASS_SENSOR_MULTILEVEL: SensorMultilevel,
            COMMAND_CLASS_SILENCE_ALARM: SilenceAlarm,
            COMMAND_CLASS_SIMPLE_AV_CONTROL: SimpleAvControl,
            COMMAND_CLASS_SOUND_SWITCH: SoundSwitch,
            COMMAND_CLASS_SUPERVISION: Supervision,
            COMMAND_CLASS_SWITCH_ALL: SwitchAll,
            COMMAND_CLASS_SWITCH_BINARY: SwitchBinary,
            COMMAND_CLASS_SWITCH_COLOR: SwitchColor,
            COMMAND_CLASS_SWITCH_MULTILEVEL: SwitchMultilevel,
            COMMAND_CLASS_SWITCH_TOGGLE_BINARY: SwitchToggleBinary,
            COMMAND_CLASS_SWITCH_TOGGLE_MULTILEVEL: SwitchToggleMultilevel,
            COMMAND_CLASS_TARIFF_CONFIG: TariffConfig,
            COMMAND_CLASS_TARIFF_TBL_MONITOR: TariffTblMonitor,
            COMMAND_CLASS_THERMOSTAT_FAN_MODE: ThermostatFanMode,
            COMMAND_CLASS_THERMOSTAT_FAN_STATE: ThermostatFanState,
            COMMAND_CLASS_THERMOSTAT_MODE: ThermostatMode,
            COMMAND_CLASS_THERMOSTAT_OPERATING_STATE: ThermostatOperatingState,
            COMMAND_CLASS_THERMOSTAT_SETBACK: ThermostatSetback,
            COMMAND_CLASS_THERMOSTAT_SETPOINT: ThermostatSetpoint,
            COMMAND_CLASS_TIME: Time,
            COMMAND_CLASS_TIME_PARAMETERS: TimeParameters,
            COMMAND_CLASS_TRANSPORT_SERVICE: TransportService,
            COMMAND_CLASS_USER_CODE: UserCode,
            COMMAND_CLASS_VERSION: Version,
            COMMAND_CLASS_WAKE_UP: WakeUp,
            COMMAND_CLASS_WINDOW_COVERING: WindowCovering,
            COMMAND_CLASS_ZIP: ZIP,
            COMMAND_CLASS_ZIP_6LOWPAN: ZIP6Lowpan,
            COMMAND_CLASS_ZIP_GATEWAY: ZIPGateway,
            COMMAND_CLASS_ZIP_NAMING: ZIPNaming,
            COMMAND_CLASS_ZIP_ND: ZIPND,
            COMMAND_CLASS_ZIP_PORTAL: ZIPPortal,
            COMMAND_CLASS_ZWAVEPLUS_INFO: ZwaveplusInfo,
            NETWORK_MANAGEMENT_INSTALLATION_MAINTENANCE: (
                NetworkManagementInstallationMaintenance
            ),
            '__original_module__': mod
        }
        self.__dict__ = mod.__dict__
        dict.__init__(self, **kwargs)
        sys.modules[__name__] = self

    def __missing__(self, key):
        value = EmptyCommandClass
        self.__setitem__(key, value)
        return value


cc = CommandClasses()
