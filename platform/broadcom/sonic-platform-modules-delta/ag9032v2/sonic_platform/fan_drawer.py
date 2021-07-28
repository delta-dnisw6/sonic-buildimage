#!/usr/bin/env python

########################################################################
# Delta AG9032V2
#
# Module contains an implementation of SONiC Platform Base API and
# provides the Fan-Drawers' information available in the platform.
#
########################################################################

try:
    from sonic_platform_base.fan_drawer_base import FanDrawerBase
    from sonic_platform.fan import Fan
except ImportError as e:
    raise ImportError(str(e) + "- required module not found")

AG9032V2_FANS_PER_FANTRAY = 1

class FanDrawer(FanDrawerBase):
    def __init__(self, fantray_index):

        FanDrawerBase.__init__(self)
        self.fantrayindex = fantray_index + 1
        for i in range(AG9032V2_FANS_PER_FANTRAY):
            self._fan_list.append(Fan(fantray_index, i))

    def get_name(self):
        """
        Retrieves the fan drawer name
        Returns:
            string: The name of the device
        """
        return "FanTray{}".format(self.fantrayindex)
