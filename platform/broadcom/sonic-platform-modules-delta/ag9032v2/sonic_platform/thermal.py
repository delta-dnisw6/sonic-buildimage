#!/usr/bin/env python

########################################################################
# Delta AG9032V2
#
# Module contains an implementation of SONiC Platform Base API and
# provides the Thermals' information which are available in the platform
#
########################################################################


try:
    import os.path
    import re
    from sonic_platform_base.thermal_base import ThermalBase
except ImportError as e:
    raise ImportError(str(e) + "- required module not found")


class Thermal(ThermalBase):
    THERMAL_NAME = (
        'Sensor_Temp_1', 'Sensor_Temp_2', 'Sensor_Temp_3',
        'Sensor_Temp_4', 'Sensor_Temp_5')
    THERMAL_THRESHOLD_MAPPING = { 
        1: {"low_threshold": 45, "critical_threshold": 55, "high_threshold": 60},
        2: {"low_threshold": 50, "critical_threshold": 60, "high_threshold": 65},
        3: {"low_threshold": 65, "critical_threshold": 75, "high_threshold": 80},
        4: {"low_threshold": 60, "critical_threshold": 70, "high_threshold": 75},
        5: {"low_threshold": 50, "critical_threshold": 60, "high_threshold": 65}}

    def __init__(self, thermal_index):
        ThermalBase.__init__(self)
        self.index = thermal_index + 1

    def get_name(self):
        """
        Retrieves the name of the thermal

        Returns:
            string: The name of the thermal
        """
        return self.THERMAL_NAME[self.index - 1]

    def get_presence(self):
        """
        Retrieves the presence of the thermal

        Returns:
            bool: True if thermal is present, False if not
        """
        return True

    def get_model(self):
        """
        Retrieves the model number (or part number) of the Thermal

        Returns:
            string: Model/part number of Thermal
        """
        return 'NA'

    def get_serial(self):
        """
        Retrieves the serial number of the Thermal

        Returns:
            string: Serial number of Thermal
        """
        return 'NA'

    def get_status(self):
        """
        Retrieves the operational status of the thermal

        Returns:
            A boolean value, True if thermal is operating properly,
            False if not
        """
        status = True
        return status

    def get_position_in_parent(self):
        """
        Retrieves 1-based relative physical position in parent device.
        Returns:
            integer: The 1-based relative physical position in parent
            device or -1 if cannot determine the position
        """
        return self.index

    def is_replaceable(self):
        """
        Indicate whether this Thermal is replaceable.
        Returns:
            bool: True if it is replaceable.
        """
        return False

    def get_temperature(self):
        """
        Retrieves current temperature reading from thermal

        Returns:
            A float number of current temperature in Celsius up to
            nearest thousandth of one degree Celsius, e.g. 30.125
        """
        try:
            command = ("ipmitool sdr get Sensor_Temp_{}").format(self.index)
            p = os.popen(command)
            content = p.read().rstrip()
            info_req = re.search(r"%s\s*:(.*)" %  "Sensor Reading", content)
            if not info_req:
                return "NA"
            temp = info_req.group(1).split(' ')[1]
            p.close()
        except IOError:
            raise SyntaxError
        return float(temp)

    def get_high_threshold(self):
        """
        Retrieves the high threshold temperature of thermal

        Returns:
            A float number, the high threshold temperature of thermal in
            Celsius up to nearest thousandth of one degree Celsius,
            e.g. 30.125
        """
        thermal_high_threshold = self.THERMAL_THRESHOLD_MAPPING[self.index]["high_threshold"]
        return thermal_high_threshold / 1.0

    def get_low_threshold(self):
        """
        Retrieves the low threshold temperature of thermal

        Returns:
            A float number, the low threshold temperature of thermal in
            Celsius up to nearest thousandth of one degree Celsius,
            e.g. 30.125
        """
        thermal_low_threshold = self.THERMAL_THRESHOLD_MAPPING[self.index]["low_threshold"]
        return thermal_low_threshold / 1.0

    def get_high_critical_threshold(self):
        """
        Retrieves the high critical threshold temperature of thermal

        Returns:
            A float number, the high critical threshold temperature of
            thermal in Celsius up to nearest thousandth of one degree
            Celsius, e.g. 30.125
        """
        thermal_high_crit_threshold = self.THERMAL_THRESHOLD_MAPPING[self.index]["critical_threshold"]
        return thermal_high_crit_threshold / 1.0

    def set_high_threshold(self, temperature):
        """
        Sets the high threshold temperature of thermal

        Args :
            temperature: A float number up to nearest thousandth of one
            degree Celsius, e.g. 30.125
        Returns:
            A boolean, True if threshold is set successfully, False if
            not
        """
        return False

    def set_low_threshold(self, temperature):
        """
        Sets the low threshold temperature of thermal

        Args :
            temperature: A float number up to nearest thousandth of one
            degree Celsius, e.g. 30.125
        Returns:
            A boolean, True if threshold is set successfully, False if
            not
        """
        return False
