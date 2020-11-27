# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Name:        micutils
# Purpose:     Utility functions for checking MICs
#
# Author:      Michael Amrhein (mamrhein@users.sourceforge.net)
#
# Copyright:   (c) 2017 Michael Amrhein
# License:     This program is part of a larger application. For license
#              details please read the file LICENSE.TXT provided together
#              with the application.
# ---------------------------------------------------------------------------
# $Source$
# $Revision$


"""Utility functions for checking MICs"""


# standard library imports
from __future__ import absolute_import, unicode_literals
from collections import namedtuple
from csv import DictReader
import os.path
import sys


__metaclass__ = type


# downloaded file 'ISO10383_MIC.xls' from
# 'https://www.iso20022.org/sites/default/files/ISO10383_MIC/'
# and converted to csv
file_name = os.path.join(os.path.dirname(__file__), "ISO10383_MIC.csv")

if sys.version_info.major < 3:

    def reader(file_name, encoding='utf-8'):
        with open(file_name, mode='rb') as csv_file:
            for row in DictReader(csv_file, delimiter=b'\t', quotechar=b'"'):
                yield {unicode(key.strip(), encoding): unicode(val, encoding)
                       for key, val in row.iteritems()}

else:

    def reader(file_name, encoding='utf-8'):
        with open(file_name, mode='r', encoding=encoding) as csv_file:
            for row in DictReader(csv_file, delimiter='\t', quotechar='"'):
                yield {key.strip(): val.strip() for key, val in row.items()}


_MIC_registry = {}
MICRecord = namedtuple('MICRecord', ('mic', 'country_code',
                                     'operating_mic', 'name', 'city'))

for record in reader(file_name):
    mic = record['MIC']
    country_code = record['ISO COUNTRY CODE (ISO 3166)']
    operating_mic = record['OPERATING MIC']
    name = record['NAME-INSTITUTION DESCRIPTION']
    city = record['CITY']
    # build MIC record
    mic_record = MICRecord(mic, country_code, operating_mic, name, city)
    _MIC_registry[mic] = mic_record


# for testing purposes
def _dump_registry():
    for key, val in sorted(_MIC_registry.items()):
        print(key, val)
    print(20 * '-')
    print("%i records" % len(_MIC_registry))


# query function
def get_mic_record(mic):
    """Retrieve MIC record from registry."""
    return _MIC_registry[mic]
