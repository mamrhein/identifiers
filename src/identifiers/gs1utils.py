# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Name:        gs1utils
# Purpose:     Utility functions for GS1 identifiers
#
# Author:      Michael Amrhein (mamrhein@users.sourceforge.net)
#
# Copyright:   (c) 2016 Michael Amrhein
# License:     This program is part of a larger application. For license
#              details please read the file LICENSE.TXT provided together
#              with the application.
# ---------------------------------------------------------------------------
# $Source$
# $Revision$


"""Utility functions for GS1 identifiers"""


import os.path
from bisect import bisect
from xml.etree import ElementTree as ETree


file_name = os.path.join(os.path.dirname(__file__), "GS1_CP_Ranges.xml")

etree = ETree.parse(file_name)
root = etree.getroot()
prefix_list = [(elem.get('prefix'), int(elem.get('gcpLength')))
               for elem in root]


def lookup_company_prefix(gs1_num_id: str) -> int:
    """Validate company prefix of given `gs1_num_id`."""
    idx = bisect(prefix_list, (gs1_num_id,)) - 1
    prefix, cp_length = prefix_list[idx]
    if gs1_num_id.startswith(prefix):
        if cp_length > 0:
            return cp_length
        raise ValueError(f"Excluded prefix: '{prefix}'.")
    raise ValueError("Undefined prefix.")
