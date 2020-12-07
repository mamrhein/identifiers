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
from collections import namedtuple
from csv import DictReader
import os.path
from typing import Generator, List


# Downloaded file 'ISO10383_MIC.csv' from
# 'https://www.iso20022.org/sites/default/files/ISO10383_MIC/'
# and converted to utf-8 encoding and tab-separated.

file_name = os.path.join(os.path.dirname(__file__), "ISO10383_MIC.csv")


def _reader(file_name: str, encoding= 'utf-8') \
        -> Generator[List[str], None, None]:
    with open(file_name, mode='r', encoding=encoding) as csv_file:
        for row in DictReader(csv_file, delimiter='\t', quotechar='"'):
            yield {key.strip(): val for key, val in row.items()}


_MIC_registry = {}
MICRecord = namedtuple('MICRecord', ('mic', 'country_code',
                                     'operating_mic', 'name', 'city'))

for record in _reader(file_name):
    mic = record['MIC']
    country_code = record['ISO COUNTRY CODE (ISO 3166)']
    operating_mic = record['OPERATING MIC']
    name = record['NAME-INSTITUTION DESCRIPTION']
    city = record['CITY']
    # build MIC record
    mic_record = MICRecord(mic, country_code, operating_mic, name, city)
    _MIC_registry[mic] = mic_record


# for testing purposes
def _dump_registry() -> None:
    for key, val in sorted(_MIC_registry.items()):
        print(key, val)
    print(20 * '-')
    print(f"{len(_MIC_registry)} records")


def get_mic_record(mic: str) -> MICRecord:
    """Retrieve MIC record from registry."""
    return _MIC_registry[mic]
