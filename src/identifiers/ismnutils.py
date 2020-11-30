# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Name:        ismnutils
# Purpose:     Utility functions for checking ISBNs
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


"""Utility functions for checking ISMNs"""


from bisect import bisect
from typing import Tuple

rule_list = [
    ('979000000000', '979009999999', 4, 7),
    ('979010000000', '979039999999', 4, 8),
    ('979040000000', '979069999999', 4, 9),
    ('979070000000', '979089999999', 4, 10),
    ('979090000000', '979099999999', 4, 11)
]


def lookup_ismn_prefix(digits: str) -> Tuple[int, int]:
    """Check ISMN prefix in `digits`."""
    idx = bisect(rule_list, (digits,)) - 1
    lower_prefix, upper_prefix, registrant_idx, item_idx = rule_list[idx]
    if lower_prefix <= digits <= upper_prefix:
        return registrant_idx, item_idx
    raise ValueError("ISMN prefix must be '9790'.")
