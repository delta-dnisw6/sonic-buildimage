#!/usr/bin/env python

########################################################################
# DellEMC S6100
#
# Module contains an implementation of SONiC Platform Base API and
# provides the Fans' information which are available in the platform.
#
########################################################################

import os.path

try:
    from sonic_platform_base.fan_base import FanBase
except ImportError as e:
    raise ImportError(str(e) + "- required module not found")

MAX_S6100_PSU_FAN_SPEED = 18000
MAX_S6100_FAN_SPEED = 16000


class Fan(FanBase):
    """DellEMC Platform-specific Fan class"""

    def __init__(self, fantray_index=1, fan_index=1, psu_fan=False, dependency=None):
        FanBase.__init__(self)
        self.is_psu_fan = psu_fan
        if not self.is_psu_fan:
            self.fantrayindex = fantray_index + 1
            self.fanindex = fan_index + 1
            self.dependency = dependency
            self.max_fan_speed = MAX_S6100_FAN_SPEED
        else:
            self.fanindex = fan_index
            self.max_fan_speed = MAX_S6100_PSU_FAN_SPEED

    def get_name(self):
        """
        Retrieves the fan name
        Returns:
            string: The name of the device
        """
        if not self.is_psu_fan:
            return "FanTray{}-Fan{}".format(self.fantrayindex, self.fanindex)
        else:
            return "PSU{} Fan".format(self.fanindex)

    def get_model(self):
        """
        Retrieves the part number of the FAN
        Returns:
            string: Part number of FAN
        """
        if self.is_psu_fan:
            return None
        else:
            return 'N/A'

    def get_serial(self):
        """
        Retrieves the serial number of the FAN
        Returns:
            string: Serial number of FAN
        """
        if self.is_psu_fan:
            return None
        else:
            return 'N/A'

    def get_presence(self):
        """
        Retrieves the presence of the FAN
        Returns:
            bool: True if fan is present, False if not
        """
        presence = True

        return presence

    def get_status(self):
        """
        Retrieves the operational status of the FAN
        Returns:
            bool: True if FAN is operating properly, False if not
        """

        return self.get_presence()

    def get_direction(self):
        """
        Retrieves the fan airflow direction
        Returns:
            A string, either FAN_DIRECTION_INTAKE or FAN_DIRECTION_EXHAUST
            depending on fan direction

        Notes:
            In DellEMC platforms,
            - Forward/Exhaust : Air flows from Port side to Fan side.
            - Reverse/Intake  : Air flows from Fan side to Port side.
        """
        return None

    def get_speed(self):
        """
        Retrieves the speed of fan
        Returns:
            int: percentage of the max fan speed
        """
        fan_speed = 1000
        return fan_speed


    def get_target_speed(self):
        """
        Retrieves the target (expected) speed of the fan

        Returns:
        An integer, the percentage of full fan speed, in the range 0 (off)
        to 100 (full speed)
        """
        fan_speed = 50
        return None

    def get_speed_tolerance(self):
        """
        Retrieves the speed tolerance of the fan

        Returns:
        An integer, the percentage of variance from target speed which is
        considered tolerable
        """
        fan_speed = 0
        return None

    def set_status_led(self, color):
        """
        Set led to expected color
        Args:
            color: A string representing the color with which to set the
                   fan module status LED
        Returns:
            bool: True if set success, False if fail.
        """
        # No LED available for FanTray and PSU Fan
        # Return True to avoid thermalctld alarm.
        return True

    def get_status_led(self):
        """
        Gets the state of the Fan status LED

        Returns:
            A string, one of the predefined STATUS_LED_COLOR_* strings.
        """
        # No LED available for FanTray and PSU Fan
        return None

