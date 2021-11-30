#!/usr/bin/env python3

########################################################################
# Delta AG9032V2
#
# Module contains an implementation of SONiC Platform Base API and
# provides the Fans' information which are available in the platform.
#
########################################################################

try:
    import os.path
    import re
    from sonic_platform_base.fan_base import FanBase
except ImportError as e:
    raise ImportError(str(e) + "- required module not found")

class Fan(FanBase):
    def __init__(self, fantray_index, fan_index, psu_fan):
        FanBase.__init__(self)
        self.psu_fan = psu_fan
        if not self.psu_fan:
            self.fantray_index = fantray_index + 1
            self.fan_index = fan_index + 1
        else:
            self.fan_index = fan_index
    def get_name(self):
        """
        Retrieves the fan name
        Returns:
            string: The name of the device
        """
        if not self.psu_fan:
            return "FanTray{}-Fan{}".format(self.fantray_index, self.fan_index)
        else:
            return "PSU{} Fan".format(self.fan_index)

    def get_model(self):
        """
        Retrieves the part number of the FAN
        Returns:
            string: Part number of FAN
        """
        if self.psu_fan:
            return None
        else:
            return 'N/A'

    def get_serial(self):
        """
        Retrieves the serial number of the FAN
        Returns:
            string: Serial number of FAN
        """
        if self.psu_fan:
            return None
        else:
            return 'N/A'

    def get_presence(self):
        """
        Retrieves the presence of the FAN
        Returns:
            bool: True if fan is present, False if not
        """
        presence = False
        try:
            if self.psu_fan:
                p = os.popen("ipmitool raw 0x38 0x2 3 0x6a 0x3 1")
                content = p.readline().rstrip()
                reg_value = int(content,16)
                if self.fan_index == 1:
                    mask = (1 << 7)
                else:
                    mask = (1 << 3)
                if reg_value & mask == 0:
                    presence = True
            else:
                command = ("ipmitool raw 0x38 0x0e")
                p = os.popen(command)
                content = p.readline().rstrip()
                reg_value = int(content, 16)
                mask = (16 >> self.fantray_index - 1)
                if reg_value & mask == 0:
                    presence = True
            p.close()
        except IOError:
            return False
        return presence

    def get_status(self):
        """
        Retrieves the operational status of the FAN
        Returns:
            bool: True if FAN is operating properly, False if not
        """
        presence = True
        if self.psu_fan:
            try:
                p = os.popen("ipmitool raw 0x38 0x2 3 0x6a 0x3 1")
                content = p.readline().rstrip()
                reg_value = int(content,16)
                if self.fan_index == 1:
                    mask = (1 << 6)
                else:
                    mask = (1 << 2)
                if reg_value & mask == 0:
                    presence = False
                p.close()   
            except IOError:
                return False
        else:
            return self.get_presence()
        return presence

    def get_direction(self):
        """
        Retrieves the fan airflow direction
        Returns:
            A string, either FAN_DIRECTION_INTAKE or FAN_DIRECTION_EXHAUST
            depending on fan direction

        Notes:
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
        try:
            if self.psu_fan:
                command = "ipmitool sdr get PSU{}_Fan".format(self.fan_index)
            else:
                command = "ipmitool sdr get Fantray_{}_{}".format(self.fantray_index, self.fan_index)
            p = os.popen(command)
            content = p.read().rstrip()
            info_req = re.search(r"%s\s*:(.*)" %  "Sensor Reading", content)
            if not info_req:
                return "N/A"
            fan_speed = info_req.group(1).split(' ')[1]
            p.close()
        except IOError:
            raise SyntaxError
        return int(fan_speed)

    def get_target_speed(self):
        """
        Retrieves the target (expected) speed of the fan

        Returns:
        An integer, the percentage of full fan speed, in the range 0 (off)
        to 100 (full speed)
        """
        return None

    def get_speed_tolerance(self):
        """
        Retrieves the speed tolerance of the fan

        Returns:
        An integer, the percentage of variance from target speed which is
        considered tolerable
        """
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

