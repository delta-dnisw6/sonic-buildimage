#!/usr/bin/env python

#############################################################################
# Mellanox
#
# Platform and model specific eeprom subclass, inherits from the base class,
# and provides the followings:
# - the eeprom format definition
# - specific encoder/decoder if there is special need
#############################################################################

try:
    from sonic_eeprom import eeprom_tlvinfo
except ImportError, e:
    raise ImportError (str(e) + "- required module not found")

class board(eeprom_tlvinfo.TlvInfoDecoder):

    _TLV_INFO_MAX_LEN = 256

    def __init__(self, name, path, cpld_root, ro):
	self.eeprom_path = "/sys/devices/pci0000:00/0000:00:12.0/i2c-1/1-0053/eeprom"
	super(board, self).__init__(self.eeprom_path, 0, '', True)
