#!/usr/bin/env python
#
# Name: chassis.py, version: 1.0
#
# Description: Module contains the definitions of SONiC platform APIs
#

try:
    import os
    from sonic_platform_base.chassis_base import ChassisBase
    from sonic_platform.fan_drawer import FanDrawer
    from sonic_platform.psu import Psu
    from sonic_platform.fan import Fan
    from sonic_platform.thermal import Thermal
except ImportError as e:
    raise ImportError(str(e) + "- required module not found")

MAX_AG9032V2_MODULE = 5
MAX_AG9032V2_PSU = 2
MAX_AG9032V2_FANTRAY = 5
MAX_AG9032V2_FAN = 1
MAX_AG9032V2_THERMAL = 5 

class Chassis(ChassisBase):

    def __init__(self):
        ChassisBase.__init__(self)

#        for i in range(MAX_AG9032V2_FANTRAY):
#            fandrawer = FanDrawer(i)
#            self._fan_drawer_list.append(fandrawer)
#            self._fan_list.extend(fandrawer._fan_list)
        # Initialize FAN
        for index in range(0, MAX_AG9032V2_FANTRAY):
            fandrawer = FanDrawer(index)
            self._fan_drawer_list.append(fandrawer)
            self._fan_list.extend(fandrawer._fan_list)
        self._num_fans=MAX_AG9032V2_FANTRAY * MAX_AG9032V2_FAN

        # Initialize PSU
        for i in range(MAX_AG9032V2_PSU):
            psu = Psu(i)
            self._psu_list.append(psu)

        for i in range(MAX_AG9032V2_THERMAL):
            thermal = Thermal(i)
            self._thermal_list.append(thermal)

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

