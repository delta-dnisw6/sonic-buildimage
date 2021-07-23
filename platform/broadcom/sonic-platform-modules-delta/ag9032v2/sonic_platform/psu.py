#!/usr/bin/env python
#

import os.path
import re

try:
    from sonic_platform_base.psu_base import PsuBase
    from sonic_platform.fan import Fan
except ImportError as e:
    raise ImportError (str(e) + "- required module not found")

class Psu(PsuBase):

    def __init__(self, index):
        PsuBase.__init__(self)
        self.index = index + 1

        # Passing True to specify it is a PSU fan
        self._fan_list.append(Fan(fan_index=self.index, psu_fan=True,
                              dependency=self))

##############################################
# Device methods
##############################################
    def get_name(self):
        """
        Retrieves the name of the device

        Returns:
            string: The name of the device
        """
        return "PSU{}".format(self.index)

    def get_presence(self):
        """
        Retrieves the presence of the device

        Returns:
            bool: True if device is present, False if not
        """
        if self.index is None:
            return False
        try:
            p = os.popen("ipmitool raw 0x38 0x2 3 0x6a 0x3 1")
            content = p.readline().rstrip()
            reg_value = int(content)
            if self.index == 1:
                mask = (1 << 7)
                if reg_value & mask == 0x80:
                   return False
            else:
                mask = (1 << 3)
                if reg_value & mask == 0x08:
                   return False
            p.close()
        except IOError:
            return False
        return True

    def get_model(self):
        """
        Retrieves the model number (or part number) of the device

        Returns:
            string: Model/part number of device
        """
        try:
           command = ("ipmitool fru print {}").format(self.index)
           p = os.popen(command)
           content = p.read().rstrip()
           info_req = re.search(r"%s\s*:(.*)" % "Product Part Number", content)
           if not info_req:
              return "NA"
           p.close()
        except IOError:
           raise SyntaxError
        return info_req.group(1).strip()

    def get_serial(self):
        """
        Retrieves the serial number of the device

        Returns:
            string: Serial number of device
        """
        try:
           command = ("ipmitool fru print {}").format(self.index)
           p = os.popen(command)
           content = p.read().rstrip()
           info_req = re.search(r"%s\s*:(.*)" % "Product Serial", content)
           if not info_req:
             return "NA"
           p.close()
        except IOError:
           raise SyntaxError
        return info_req.group(1).strip()

    def get_status(self):
        """
        Retrieves the operational status of the device

        Returns:
            A boolean value, True if device is operating properly, False if not
        """
        try:
            p = os.popen("ipmitool raw 0x38 0x2 3 0x6a 0x3 1")
            content = p.readline().rstrip()
            reg_value = int(content, 16)
            if self.index == 1:
                mask = (1 << 6)
            else:
                mask = (1 << 2)
            if reg_value & mask == 0:
                return False
            p.close()
        except IOError:
            raise SyntaxError
        return True

##############################################
# PSU methods
##############################################

    def get_voltage(self):
        """
        Retrieves current PSU voltage output

        Returns:
            A float number, the output voltage in volts,
            e.g. 12.1
        """
        try:
            command = ("ipmitool sdr get PSU{}_Vout").format(self.index)
            p = os.popen(command)
            content = p.read().rstrip()
            info_req = re.search(r"%s\s*:(.*)" %  "Sensor Reading", content)
            if not info_req:
                return "NA"
            vout = info_req.group(1).split(' ')[1]
            p.close()
        except IOError:
            raise SyntaxError
        return float(vout)

    def get_current(self):
        """
        Retrieves present electric current supplied by PSU

        Returns:
            A float number, the electric current in amperes, e.g 15.4
        """
        try:
            command = ("ipmitool sdr get PSU{}_Iout").format(self.index)
            p = os.popen(command)
            content = p.read().rstrip()
            info_req = re.search(r"%s\s*:(.*)" %  "Sensor Reading", content)
            if not info_req:
                return "NA"
            iout = info_req.group(1).split(' ')[1]
            p.close()
        except IOError:
            raise SyntaxError
        return float(iout)

    def get_power(self):
        """
        Retrieves current energy supplied by PSU

        Returns:
            A float number, the power in watts, e.g. 302.6
        """
        try:
            command = ("ipmitool sdr get PSU{}_Pout").format(self.index)
            p = os.popen(command)
            content = p.read().rstrip()
            info_req = re.search(r"%s\s*:(.*)" %  "Sensor Reading", content)
            if not info_req:
                return "NA"
            pout = info_req.group(1).split(' ')[1]
            p.close()
        except IOError:
            raise SyntaxError
        return float(pout)

    def get_powergood_status(self):
        """
        Retrieves the powergood status of PSU

        Returns:
            A boolean, True if PSU has stablized its output voltages and passed all
            its internal self-tests, False if not.
        """
        return self.get_status()

    def set_status_led(self, color):
        """
        Sets the state of the PSU status LED

        Args:
            color: A string representing the color with which to set the
                   PSU status LED

        Returns:
            bool: True if status LED state is set successfully, False if not
        """
        raise NotImplementedError

    def get_status_led(self):
        """
        Gets the state of the PSU status LED

        Returns:
            A string, one of the predefined STATUS_LED_COLOR_* strings above
        """
        if self.get_powergood_status():
            return self.STATUS_LED_COLOR_GREEN
        else:
            return self.STATUS_LED_COLOR_OFF
