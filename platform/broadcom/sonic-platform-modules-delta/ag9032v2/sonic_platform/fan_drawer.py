#!/usr/bin/env python3

########################################################################
# Delta Ag9032V2 
#
# Module contains an implementation of SONiC Platform Base API and
# provides the Fan-Drawers' information available in the platform.
#
########################################################################

try:
    from sonic_platform_base.fan_drawer_base import FanDrawerBase
except ImportError as e:
    raise ImportError(str(e) + "- required module not found")

AG9032V2_FANS_PER_FANTRAY = 5

class FanDrawer(FanDrawerBase):
    def __init__(self, fantray_index):

        FanDrawerBase.__init__(self)
        # FanTray is 1-based in Delta platforms
        self.fantray_index = fantray_index + 1

    def get_name(self):
        """
        Retrieves the fan drawer name
        Returns:
            string: The name of the device
        """
        return "FanTray{}".format(self.fantray_index)
