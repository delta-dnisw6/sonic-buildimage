#!/usr/bin/env python

#############################################################################
#
# Module contains an implementation of SONiC Platform Base API and
# provides the platform information
#
#############################################################################

try:
    import time
    import sys
    from sonic_platform_base.chassis_base import ChassisBase
    from sonic_platform.fan_drawer import FanDrawer
    from sonic_platform.psu import Psu
    from sonic_platform.fan import Fan
    from sonic_platform.thermal import Thermal
    from sonic_platform.eeprom import Eeprom
    from sonic_platform.sfp import Sfp
except ImportError as e:
    raise ImportError(str(e) + "- required module not found")

MAX_AG9032V2_PSU = 2
MAX_AG9032V2_FANTRAY = 5
MAX_AG9032V2_FAN = 1
MAX_AG9032V2_THERMAL = 5
MAX_AG9032V2_SFP = 34 

class Chassis(ChassisBase):

    def __init__(self):
        ChassisBase.__init__(self)

        # Initialize EEPROM
        self._eeprom = Eeprom()

        # Initialize FAN
        for i in range(0, MAX_AG9032V2_FANTRAY):
            fandrawer = FanDrawer(i)
            self._fan_drawer_list.append(fandrawer)
            self._fan_list.extend(fandrawer._fan_list)
        self._num_fans=MAX_AG9032V2_FANTRAY * MAX_AG9032V2_FAN

        # Initialize PSU
        for i in range(MAX_AG9032V2_PSU):
            psu = Psu(i)
            self._psu_list.append(psu)

        # Initialize THERMAL
        for i in range(MAX_AG9032V2_THERMAL):
            thermal = Thermal(i)
            self._thermal_list.append(thermal)

        # Initialize SFP
        for i in range(MAX_AG9032V2_SFP):
            sfp = Sfp(i)
            self._sfp_list.append(sfp)

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
