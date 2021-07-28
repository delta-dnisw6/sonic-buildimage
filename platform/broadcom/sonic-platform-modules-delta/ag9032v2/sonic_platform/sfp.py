#!/usr/bin/env python

#############################################################################
# Delta
#
# Module contains an implementation of SONiC Platform Base API and
# provides the platform information
#
#############################################################################

try:
    import os.path
    from sonic_platform_base.sfp_base import SfpBase
    from sonic_platform_base.sonic_sfp.sff8436 import sff8436Dom
    from sonic_platform_base.sonic_sfp.sff8436 import sff8436InterfaceId
    from sonic_platform_base.sonic_sfp.sff8472 import sff8472Dom
    from sonic_platform_base.sonic_sfp.sff8472 import sff8472InterfaceId
except ImportError as e:
    raise ImportError (str(e) + "- required module not found")


QSFP_INFO_OFFSET = 128
QSFP_DOM_OFFSET = 0

SFP_INFO_OFFSET = 0
SFP_DOM_OFFSET = 256

XCVR_INTFACE_BULK_OFFSET = 0
XCVR_INTFACE_BULK_WIDTH_QSFP = 20
XCVR_INTFACE_BULK_WIDTH_SFP = 21
XCVR_HW_REV_WIDTH_QSFP = 2
XCVR_HW_REV_WIDTH_SFP = 4
XCVR_CABLE_LENGTH_WIDTH_QSFP = 5
XCVR_VENDOR_NAME_OFFSET = 20
XCVR_VENDOR_NAME_WIDTH = 16
XCVR_VENDOR_OUI_OFFSET = 37
XCVR_VENDOR_OUI_WIDTH = 3
XCVR_VENDOR_PN_OFFSET = 40
XCVR_VENDOR_PN_WIDTH = 16
XCVR_HW_REV_OFFSET = 56
XCVR_HW_REV_WIDTH_OSFP = 2
XCVR_HW_REV_WIDTH_SFP = 4
XCVR_VENDOR_SN_OFFSET = 68
XCVR_VENDOR_SN_WIDTH = 16
XCVR_VENDOR_DATE_OFFSET = 84
XCVR_VENDOR_DATE_WIDTH = 8
XCVR_DOM_CAPABILITY_OFFSET = 92
XCVR_DOM_CAPABILITY_WIDTH = 1

# Offset for values in QSFP eeprom
QSFP_DOM_REV_OFFSET = 1
QSFP_DOM_REV_WIDTH = 1
QSFP_TEMPE_OFFSET = 22
QSFP_TEMPE_WIDTH = 2
QSFP_VOLT_OFFSET = 26
QSFP_VOLT_WIDTH = 2
QSFP_CHANNL_MON_OFFSET = 34
QSFP_CHANNL_MON_WIDTH = 16
QSFP_CHANNL_MON_WITH_TX_POWER_WIDTH = 24
QSFP_CONTROL_OFFSET = 86
QSFP_CONTROL_WIDTH = 8
QSFP_CHANNL_RX_LOS_STATUS_OFFSET = 3
QSFP_CHANNL_RX_LOS_STATUS_WIDTH = 1
QSFP_CHANNL_TX_FAULT_STATUS_OFFSET = 4
QSFP_CHANNL_TX_FAULT_STATUS_WIDTH = 1
QSFP_POWEROVERRIDE_OFFSET = 93
QSFP_POWEROVERRIDE_WIDTH = 1
QSFP_MODULE_THRESHOLD_OFFSET = 128
QSFP_MODULE_THRESHOLD_WIDTH = 24
QSFP_CHANNEL_THRESHOLD_OFFSET = 176
QSFP_CHANNEL_THRESHOLD_WIDTH = 16

qsfp_cable_length_tup = ('Length(km)', 'Length OM3(2m)',
                         'Length OM2(m)', 'Length OM1(m)',
                         'Length Cable Assembly(m)')

qsfp_compliance_code_tup = ('10/40G Ethernet Compliance Code', 'SONET Compliance codes',
                            'SAS/SATA compliance codes', 'Gigabit Ethernet Compliant codes',
                            'Fibre Channel link length/Transmitter Technology',
                            'Fibre Channel transmission media', 'Fibre Channel Speed')


# Offset for values in SFP eeprom
SFP_TEMPE_OFFSET = 96
SFP_TEMPE_WIDTH = 2
SFP_VOLT_OFFSET = 98
SFP_VOLT_WIDTH = 2
SFP_CHANNL_MON_OFFSET = 100
SFP_CHANNL_MON_WIDTH = 6
SFP_MODULE_THRESHOLD_OFFSET = 0
SFP_MODULE_THRESHOLD_WIDTH = 40
SFP_CHANNL_THRESHOLD_OFFSET = 112
SFP_CHANNL_THRESHOLD_WIDTH = 2
SFP_STATUS_CONTROL_OFFSET = 110
SFP_STATUS_CONTROL_WIDTH = 1
SFP_TX_DISABLE_HARD_BIT = 7
SFP_TX_DISABLE_SOFT_BIT = 6

sfp_cable_length_tup = ('LengthSMFkm-UnitsOfKm', 'LengthSMF(UnitsOf100m)',
                        'Length50um(UnitsOf10m)', 'Length62.5um(UnitsOfm)',
                        'LengthCable(UnitsOfm)', 'LengthOM3(UnitsOf10m)')

sfp_compliance_code_tup = ('10GEthernetComplianceCode', 'InfinibandComplianceCode',
                           'ESCONComplianceCodes', 'SONETComplianceCodes',
                           'EthernetComplianceCodes', 'FibreChannelLinkLength',
                           'FibreChannelTechnology', 'SFP+CableTechnology',
                           'FibreChannelTransmissionMedia', 'FibreChannelSpeed')


class Sfp(SfpBase):
    """Platform-specific Sfp class"""

    # Port number
    # QSFP: 0-31, SFP: 32-33
    PORT_START = 0
    PORT_END_QSFP  = 31
    PORT_START_SFP = 32
    PORT_END = 33

    EEPROM_OFFSET = 20

    _port_to_eeprom_mapping = {}

    @property
    def port_start(self):
        return self.PORT_START

    @property
    def port_end(self):
        return self.PORT_END

    @property
    def port_start_sfp(self):
        return self.PORT_START_SFP

    @property
    def qsfp_ports(self):
        return range(self.PORT_START, self.PORT_END_QSFP)

    @property
    def port_to_eeprom_mapping(self):
        return self._port_to_eeprom_mapping


    def __init__(self, sfp_index=0):
        # Init index
        self.index = sfp_index
        self.port_num = self.index

        # Init eeprom path
        eeprom_path = "/sys/bus/i2c/devices/{0}-0050/eeprom"

        for x in range(self.port_start, self.port_end + 1):
            self.port_to_eeprom_mapping[x] = eeprom_path.format(x + self.EEPROM_OFFSET)

        self.info_dict_keys = ['type', 'hardware_rev', 'serial', 'manufacturer', 'model', 'connector', 'encoding', 'ext_identifier',
                               'ext_rateselect_compliance', 'cable_type', 'cable_length', 'nominal_bit_rate', 'specification_compliance', 'vendor_date', 'vendor_oui',
                               'application_advertisement', 'type_abbrv_name']

        SfpBase.__init__(self)

    def __read_eeprom_specific_bytes(self, offset, num_bytes):
        sysfsfile_eeprom = None
        eeprom_raw = []

        for i in range(0, num_bytes):
            eeprom_raw.append("0x00")

        sysfs_sfp_i2c_client_eeprom_path = self.port_to_eeprom_mapping[self.port_num]
        try:
            sysfsfile_eeprom = open(
                sysfs_sfp_i2c_client_eeprom_path, mode="rb", buffering=0)
            sysfsfile_eeprom.seek(offset)
            raw = sysfsfile_eeprom.read(num_bytes)
            if sys.version_info[0] >= 3:
                for n in range(0, num_bytes):
                    eeprom_raw[n] = hex(raw[n])[2:].zfill(2)
            else:
                for n in range(0, num_bytes):
                    eeprom_raw[n] = hex(ord(raw[n]))[2:].zfill(2)
        except Exception:
            pass
        finally:
            if sysfsfile_eeprom:
                sysfsfile_eeprom.close()

        return eeprom_raw

    def get_transceiver_info(self):
        """
        Retrieves transceiver info of this SFP
        Returns:
            A dict which contains following keys/values :
        ========================================================================
        keys                       |Value Format   |Information
        ---------------------------|---------------|----------------------------
        type                       |1*255VCHAR     |type of SFP
        hardware_rev               |1*255VCHAR     |hardware version of SFP
        serial                     |1*255VCHAR     |serial number of the SFP
        manufacturer               |1*255VCHAR     |SFP vendor name
        model                      |1*255VCHAR     |SFP model name
        connector                  |1*255VCHAR     |connector information
        encoding                   |1*255VCHAR     |encoding information
        ext_identifier             |1*255VCHAR     |extend identifier
        ext_rateselect_compliance  |1*255VCHAR     |extended rateSelect compliance
        cable_length               |INT            |cable length in m
        nominal_bit_rate           |INT            |nominal bit rate by 100Mbs
        specification_compliance   |1*255VCHAR     |specification compliance
        vendor_date                |1*255VCHAR     |vendor date
        vendor_oui                 |1*255VCHAR     |vendor OUI
        application_advertisement  |1*255VCHAR     |supported applications advertisement
        ========================================================================
        """
        # check present status
        if self.port_num > self.PORT_END_QSFP: # SFP index 32~33
            sfpi_obj = sff8472InterfaceId()
        else: # QSFP index 0~31
            sfpi_obj = sff8436InterfaceId()
        if not self.get_presence() or not sfpi_obj:
            return {}

        if self.port_num > self.PORT_END_QSFP: # SFP index 32~33
            offset = SFP_INFO_OFFSET
            sfp_interface_bulk_raw = self.__read_eeprom_specific_bytes(
                (offset + XCVR_INTFACE_BULK_OFFSET), XCVR_INTFACE_BULK_WIDTH_SFP)
        else: # QSFP index 0~31
            offset = QSFP_INFO_OFFSET
            sfp_interface_bulk_raw = self.__read_eeprom_specific_bytes(
                (offset + XCVR_INTFACE_BULK_OFFSET), XCVR_INTFACE_BULK_WIDTH_QSFP)

        sfp_interface_bulk_data = sfpi_obj.parse_sfp_info_bulk(
            sfp_interface_bulk_raw, 0)

        sfp_vendor_name_raw = self.__read_eeprom_specific_bytes(
            (offset + XCVR_VENDOR_NAME_OFFSET), XCVR_VENDOR_NAME_WIDTH)
        sfp_vendor_name_data = sfpi_obj.parse_vendor_name(
            sfp_vendor_name_raw, 0)

        sfp_vendor_pn_raw = self.__read_eeprom_specific_bytes(
            (offset + XCVR_VENDOR_PN_OFFSET), XCVR_VENDOR_PN_WIDTH)
        sfp_vendor_pn_data = sfpi_obj.parse_vendor_pn(
            sfp_vendor_pn_raw, 0)

        if self.port_num > self.PORT_END_QSFP: # SFP index 32~33
            sfp_vendor_rev_raw = self.__read_eeprom_specific_bytes(
                (offset + XCVR_HW_REV_OFFSET), XCVR_HW_REV_WIDTH_SFP)
        else: # QSFP index 0~31
            sfp_vendor_rev_raw = self.__read_eeprom_specific_bytes(
                (offset + XCVR_HW_REV_OFFSET), XCVR_HW_REV_WIDTH_QSFP)

        sfp_vendor_rev_data = sfpi_obj.parse_vendor_rev(
            sfp_vendor_rev_raw, 0)

        sfp_vendor_sn_raw = self.__read_eeprom_specific_bytes(
            (offset + XCVR_VENDOR_SN_OFFSET), XCVR_VENDOR_SN_WIDTH)
        sfp_vendor_sn_data = sfpi_obj.parse_vendor_sn(
            sfp_vendor_sn_raw, 0)

        sfp_vendor_oui_raw = self.__read_eeprom_specific_bytes(
            (offset + XCVR_VENDOR_OUI_OFFSET), XCVR_VENDOR_OUI_WIDTH)
        if sfp_vendor_oui_raw is not None:
            sfp_vendor_oui_data = sfpi_obj.parse_vendor_oui(
                sfp_vendor_oui_raw, 0)

        sfp_vendor_date_raw = self.__read_eeprom_specific_bytes(
            (offset + XCVR_VENDOR_DATE_OFFSET), XCVR_VENDOR_DATE_WIDTH)
        sfp_vendor_date_data = sfpi_obj.parse_vendor_date(
            sfp_vendor_date_raw, 0)

        transceiver_info_dict = dict.fromkeys(self.info_dict_keys, 'N/A')
        compliance_code_dict = dict()

        if sfp_interface_bulk_data:
            transceiver_info_dict['type'] = sfp_interface_bulk_data['data']['type']['value']
            transceiver_info_dict['connector'] = sfp_interface_bulk_data['data']['Connector']['value']
            transceiver_info_dict['encoding'] = sfp_interface_bulk_data['data']['EncodingCodes']['value']
            transceiver_info_dict['ext_identifier'] = sfp_interface_bulk_data['data']['Extended Identifier']['value']
            transceiver_info_dict['ext_rateselect_compliance'] = sfp_interface_bulk_data['data']['RateIdentifier']['value']
            transceiver_info_dict['type_abbrv_name'] = sfp_interface_bulk_data['data']['type_abbrv_name']['value']

        transceiver_info_dict['manufacturer'] = sfp_vendor_name_data[
            'data']['Vendor Name']['value'] if sfp_vendor_name_data else 'N/A'
        transceiver_info_dict['model'] = sfp_vendor_pn_data['data']['Vendor PN']['value'] if sfp_vendor_pn_data else 'N/A'
        transceiver_info_dict['hardware_rev'] = sfp_vendor_rev_data['data']['Vendor Rev']['value'] if sfp_vendor_rev_data else 'N/A'
        transceiver_info_dict['serial'] = sfp_vendor_sn_data['data']['Vendor SN']['value'] if sfp_vendor_sn_data else 'N/A'
        transceiver_info_dict['vendor_oui'] = sfp_vendor_oui_data['data']['Vendor OUI']['value'] if sfp_vendor_oui_data else 'N/A'
        transceiver_info_dict['vendor_date'] = sfp_vendor_date_data[
            'data']['VendorDataCode(YYYY-MM-DD Lot)']['value'] if sfp_vendor_date_data else 'N/A'
        transceiver_info_dict['cable_type'] = "Unknown"
        transceiver_info_dict['cable_length'] = "Unknown"

        if self.port_num > self.PORT_END_QSFP: # SFP index 32~33
            for key in sfp_cable_length_tup:
                if key in sfp_interface_bulk_data['data']:
                    transceiver_info_dict['cable_type'] = key
                    transceiver_info_dict['cable_length'] = str(
                        sfp_interface_bulk_data['data'][key]['value'])

            for key in sfp_compliance_code_tup:
                if key in sfp_interface_bulk_data['data']['Specification compliance']['value']:
                    compliance_code_dict[key] = sfp_interface_bulk_data['data']['Specification compliance']['value'][key]['value']

            transceiver_info_dict['specification_compliance'] = str(
                compliance_code_dict)
            transceiver_info_dict['nominal_bit_rate'] = str(
                sfp_interface_bulk_data['data']['NominalSignallingRate(UnitsOf100Mbd)']['value'])
        else: # QSFP index 0~31
            for key in qsfp_cable_length_tup:
                if key in sfp_interface_bulk_data['data']:
                    transceiver_info_dict['cable_type'] = key
                    transceiver_info_dict['cable_length'] = str(
                        sfp_interface_bulk_data['data'][key]['value'])

            for key in qsfp_compliance_code_tup:
                if key in sfp_interface_bulk_data['data']['Specification compliance']['value']:
                    compliance_code_dict[key] = sfp_interface_bulk_data['data']['Specification compliance']['value'][key]['value']

            transceiver_info_dict['specification_compliance'] = str(
                compliance_code_dict)
            transceiver_info_dict['nominal_bit_rate'] = str(
                sfp_interface_bulk_data['data']['Nominal Bit Rate(100Mbs)']['value'])


        return transceiver_info_dict

    def get_presence(self):
        """
        Retrieves the presence of the device
        Returns:
            bool: True if device is present, False if not
        """
        # Check for invalid port_num
        if self.port_num < self.port_start or self.port_num > self.port_end:
            return False

        try:
            reg_file = open("/sys/devices/platform/delta-ag9032v2-swpld1.0/sfp_is_present")
        except IOError as e:
            print("Error: unable to open file: %s" % str(e))
            return False

        content = reg_file.readline().rstrip()

        # content is a string containing the hex representation of the register
        reg_value = int(content, 16)

        # Mask off the bit corresponding to our port
        mask = (1 << (self.port_end - self.port_num + 6))

        # ModPrsL is active low
        if reg_value & mask == 0:
            return True

        return False

    def get_reset_status(self):
        """
        Retrieves the reset status of SFP
        Returns:
            A Boolean, True if reset enabled, False if disabled
        """
        # Check for invalid port_num
        if self.port_num < self.port_start or self.port_num > self.PORT_END_QSFP:
            return False
        try:
            reg_file = open("/sys/devices/platform/delta-ag9032v2-swpld1.0/qsfp_reset", "r+")
        except IOError as e:
            print("Error: unable to open file: %s" % str(e))
            return False

        content = reg_file.readline().rstrip()

        # File content is a string containing the hex representation of the register
        reg_value = int(content, 16)

        # Mask off the bit corresponding to our port
        mask = (1 << (self.port_end - self.port_num) - 1)

        # ResetL is active low
        reg_value = reg_value & ~mask

        # Convert our register value back to a hex string and write back
        reg_file.seek(0)
        reg_file.write(hex(reg_value))
        reg_file.close()

        # Sleep 1 second to allow it to settle
        time.sleep(1)

        # Flip the bit back high and write back to the register to take port out of reset
        try:
            reg_file = open(QSFP_RESET_REGISTER_DEVICE_FILE, "w")
        except IOError as e:
            print("Error: unable to open file: %s" % str(e))
            return False

        reg_value = reg_value | mask
        reg_file.seek(0)
        reg_file.write(hex(reg_value))
        reg_file.close()

        return True

    def get_lpmode(self):
        """
        Retrieves the lpmode (low power mode) status of this SFP
        Returns:
            A Boolean, True if lpmode is enabled, False if disabled
        """
        # Check for invalid port_num
        if self.port_num < self.port_start or self.port_num > self.PORT_END_QSFP:
            return False

        try:
            reg_file = open("/sys/devices/platform/delta-ag9032v2-swpld1.0/qsfp_lpmode")
        except IOError as e:
            print("Error: unable to open file: %s" % str(e))

        content = reg_file.readline().rstrip()

        # content is a string containing the hex representation of the register
        reg_value = int(content, 16)

        # Mask off the bit corresponding to our port
        mask = (1 << (self.port_end - self.port_num) - 1)

        # LPMode is active high
        if reg_value & mask == 0:
            return False

        return True

    def get_tx_disable(self):
        """
        Retrieves the tx_disable status of this SFP
        Returns:
            A Boolean, True if tx_disable is enabled, False if disabled
        """
        return False

    def get_rx_los(self):
        """
        Retrieves the RX LOS (lost-of-signal) status of SFP
        Returns:
            A Boolean, True if SFP has RX LOS, False if not.
            Note : RX LOS status is latched until a call to get_rx_los or a reset.
        """
        return False

    def get_tx_fault(self):
        """
        Retrieves the TX fault status of SFP
        Returns:
            A Boolean, True if SFP has TX fault, False if not
            Note : TX fault status is lached until a call to get_tx_fault or a reset.
        """
        return False
