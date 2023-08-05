"""
    TestNW
    ======

    Contains helpers to translate network data into TestNW objects used
    within the library and test framework.

    .. Copyright:
        Copyright 2018 Wirepas Ltd. All Rights Reserved.
        See file LICENSE.txt for full license details.
"""
import datetime
import logging
import struct
import binascii
import json

from .types import ApplicationTypes
from .generic import GenericMessage

from .. import tools

class TestNWMessage(GenericMessage):
    """
    NodeDiagnosticsMessage

    Represents traffic diagnostics report message sent by nodes.

    Message content:
        row[0..]
            id       byte
                         test_data_id               4 lowest bits
                         id_ctrl                    4 highest bits
            size     byte
                         number_of_fields           6 lowest bits
                         bytes_per_field_minus_one  2 highest bits
            datafields[number_of_fields][bytes_per_field]
    """
    def __init__(self, *args, **kwargs)-> 'TestNWMessage':
        super(TestNWMessage, self).__init__(*args, **kwargs)
        self.type = ApplicationTypes.TestNWMessage

        if isinstance(self.data_payload, str):
            self.data_payload = bytes(self.data_payload, "utf8")

        # Parse all rows from apdu.
        self.row_count = 0
        apdu_offset = 0
        self.testdata_id = []
        self.id_ctrl = []
        self.number_of_fields = []
        self.bytes_per_field = []
        self.datafields = []

        try:
            while apdu_offset < len(self.data_payload):
                if self.data_payload[apdu_offset] == 0:
                    break
                # Test data ID is the 4 lowest bits from the first byte
                self.testdata_id.append(self.data_payload[apdu_offset] & 0x0f)
                # ID_ctrl is the 4 highest bits of the first byte
                self.id_ctrl.append(self.data_payload[apdu_offset] & 0xf0)
                apdu_offset += 1
                # Number of fields is the lowest 6 bits of second byte
                self.number_of_fields.append(self.data_payload[apdu_offset] & 0x3f)
                # Bytes per field is the two highest bits of second byte + 1
                self.bytes_per_field.append((self.data_payload[apdu_offset] >> 6) + 1)
                apdu_offset +=1

                self.datafields.append([])
                for i in range(self.number_of_fields[self.row_count]):
                    value = 0
                    for j in range(self.bytes_per_field[self.row_count]):
                        value += self.data_payload[apdu_offset] << (j*8)
                        apdu_offset += 1
                    self.datafields[self.row_count].append(value)
                self.row_count += 1
        except IndexError:
            print('A broken testnw apdu')
