#!/usr/bin/env pythonsr/local/lib/python3.7/dist-packages/sonic_platform/fan.py
#
# Name: fan.py, version: 1.0
#
# Description: Module contains the definitions of SONiC platform APIs
#

try:
    import math
    import os
    from sonic_platform_base.fan_base import FanBase
except ImportError as e:
    raise ImportError(str(e) + "- required module not found")

class Fan(FanBase):

    def __init__(self, fantray_index=1, fan_index=1, psu_fan=False, 
        dependency=None):
        FanBase.__init__(self)
        self.is_psu_fan = psu_fan
        if not self.is_psu_fan:
            self.fantrayindex = fantray_index + 1
            self.fanindex = fan_index + 1
        else:
            self.dependency = dependency
            self.fanindex = fan_index

##############################################
# Device methods
##############################################
    def get_name(self):
        """
        Retrieves the name of the device
        Returns:
            string: The name of the device
        """

        if self.is_psu_fan:
            return "PSU{} Fan".format(self.fanindex)
        else:
            return "FanTray{}-Fan{}".format(self.fantrayindex, self.fanindex)

    def get_model(self):
        """
        Retrieves the part number of the FAN
        Returns:
            String: Part number of FAN
        """
        return 'NA'

    def get_serial(self):
        """
        Retrieves the serial number of the FAN
        Returns:
            String: Serial number of FAN
        """
        return 'NA'

    def get_presence(self):
        """
        Retrieves the presence of the device
        Returns:
            bool: True if device is present, False if not
        """
        presence = False
        if self.is_psu_fan:
            return self.dependency.get_presence()
        else:
            presence = True
            return presence

    def get_status(self):
        """
        Retrieves the operational status of the device
        Returns:
            A boolean value, True if device is operating properly, False if not
        """
        presence = True
        return presence

##############################################
# FAN methods
##############################################
    def get_direction(self):
        """
        Retrieves the direction of fan
        Returns:
            A string, either FAN_DIRECTION_INTAKE or FAN_DIRECTION_EXHAUST
            depending on fan direction
        """
        return 'NA'

    def get_speed(self):
        """
        Retrieves the speed of fan as a percentage of full speed
        Returns:
            An integer, the percentage of full fan speed
        """
        #if self.__is_psu_fan:
        #else:
        speed = 0
        return speed

