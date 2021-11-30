#!/usr/bin/env python3

#############################################################################
#
# Module contains an implementation of SONiC Platform Base API and
# provides the platform information
#
#############################################################################

try:
    import sys
    from sonic_platform_base.chassis_base import ChassisBase
    from sonic_platform.fan_drawer import FanDrawer
    from sonic_platform.psu import Psu
    from sonic_platform.thermal import Thermal
    from sonic_platform.eeprom import Eeprom
    from sonic_platform.sfp import Sfp
    from sonic_platform.fan import Fan
except ImportError as e:
    raise ImportError(str(e) + "- required module not found")

MAX_AG9032V2_MODULE = 5
MAX_AG9032V2_PSU = 2
MAX_AG9032V2_FANTRAY = 5
MAX_AG9032V2_FAN = 1
MAX_AG9032V2_THERMAL = 5
MAX_AG9032V2_SFP = 34 
PMON_REBOOT_CAUSE_PATH = "/usr/share/sonic/platform/reboot-cause/"
REBOOT_CAUSE_FILE = "reboot-cause.txt"
PREV_REBOOT_CAUSE_FILE = "previous-reboot-cause.txt"

class Chassis(ChassisBase):

    REBOOT_CAUSE_PATH = "/host/reboot-cause/platform/reboot_reason"

    _port_to_i2c_mapping = {
            1:  20,
            2:  21,
            3:  22,
            4:  23,
            5:  24,
            6:  25,
            7:  26,
            8:  27,
            9:  28,
            10: 29,
            11: 30,
            12: 31,
            13: 32,
            14: 33,
            15: 34,
            16: 35,
            17: 36,
            18: 37,
            19: 38,
            20: 39,
            21: 40,
            22: 41,
            23: 42,
            24: 43,
            25: 44,
            26: 45,
            27: 46,
            28: 47,
            29: 48,
            30: 49,
            31: 50,
            32: 51,
            33: 52,
            34: 53,
            }

    def __init__(self):
        ChassisBase.__init__(self)

        # Initialize EEPROM
        self._eeprom = Eeprom()

        # Initialize FAN
        for i in range(MAX_AG9032V2_FANTRAY):
            fan_drawer = FanDrawer(i)
            fan = Fan(i, 0, False)
            fan_drawer._fan_list.append(fan)
            self._fan_drawer_list.append(fan_drawer)

        # Initialize PSU
        for i in range(MAX_AG9032V2_PSU):
            psu = Psu(i)
            self._psu_list.append(psu)

        # Initialize THERMAL
        for i in range(MAX_AG9032V2_THERMAL):
            thermal = Thermal(i)
            self._thermal_list.append(thermal)

        self.PORT_START = 1
        self.PORT_END = 34
        self.PORTS_IN_BLOCK = (self.PORT_END + 1)
        _sfp_port = range(33, self.PORTS_IN_BLOCK)
        eeprom_base = "/sys/bus/i2c/devices/{0}-0050/eeprom"

        for index in range(self.PORT_START, self.PORTS_IN_BLOCK):
            eeprom_path = eeprom_base.format(self._port_to_i2c_mapping[index])
            port_type = 'SFP' if index in _sfp_port else 'QSFP_DD'
            sfp_node = Sfp(index, port_type, eeprom_path)
            self._sfp_list.append(sfp_node)

    def __read_txt_file(self, file_path):
        try:
            with open(file_path, 'r') as fd:
                data = fd.read()
                return data.strip()
        except IOError:
            pass
        return None

    def get_presence(self):
        """
        Retrieves the presence of the chassis
        Returns:
            bool: True if chassis is present, False if not
        """
        return True

    def get_status(self):
        """
        Retrieves the operational status of the chassis
        Returns:
            bool: A boolean value, True if chassis is operating properly
            False if not
        """
        return True

    def get_num_fans(self):
        return self._num_fans

    def get_name(self):
        """
        Retrieves the name of the chassis
        Returns:
            string: The name of the chassis
        """
        return self._eeprom.modelstr()

    def get_reboot_cause(self):
        """
        Retrieves the cause of the previous reboot
        Returns:
            A tuple (string, string) where the first element is a string
            containing the cause of the previous reboot. This string must be
            one of the predefined strings in this class. If the first string
            is "REBOOT_CAUSE_HARDWARE_OTHER", the second string can be used
            to pass a description of the reboot cause.
        """
        description = 'None'
        reboot_cause = self.REBOOT_CAUSE_HARDWARE_OTHER

        reboot_cause_path = PMON_REBOOT_CAUSE_PATH + REBOOT_CAUSE_FILE
        prev_reboot_cause_path = PMON_REBOOT_CAUSE_PATH + PREV_REBOOT_CAUSE_FILE

        sw_reboot_cause = self.__read_txt_file(reboot_cause_path) or "Unknown"
        prev_sw_reboot_cause = self.__read_txt_file(prev_reboot_cause_path) or "Unknown"

        if sw_reboot_cause == "Unknown" and (prev_sw_reboot_cause == "Unknown" or prev_sw_reboot_cause == self.REBOOT_CAUSE_POWER_LOSS):
            reboot_cause = self.REBOOT_CAUSE_POWER_LOSS
            description = prev_sw_reboot_cause
        elif sw_reboot_cause != "Unknown":
            reboot_cause = self.REBOOT_CAUSE_NON_HARDWARE
            description = sw_reboot_cause
        elif prev_reboot_cause_path != "Unknown":
            reboot_cause = self.REBOOT_CAUSE_NON_HARDWARE
            description = prev_sw_reboot_cause

        return (reboot_cause, description)

    def get_sfp(self, index):
        """
        Retrieves sfp represented by (0-based) index <index>

        Args:
            index: An integer, the index (0-based) of the sfp to retrieve.
                   The index should be the sequence of a physical port in a chassis,
                   starting from 0.
                   For example, 0 for Ethernet0, 1 for Ethernet4 and so on.

        Returns:
            An object dervied from SfpBase representing the specified sfp
        """
        sfp = None

        try:
            # The index will start from 0
            sfp = self._sfp_list[index]
        except IndexError:
            sys.stderr.write("SFP index {} out of range (1-{})\n".format(
                             index, len(self._sfp_list)))
        return sfp

