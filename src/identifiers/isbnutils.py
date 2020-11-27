# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Name:        isbnutils
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


"""Utility functions for checking ISBNs"""


from __future__ import absolute_import
import os.path
from bisect import bisect
try:
    from xml.etree import cElementTree as ETree
except ImportError:
    from xml.etree import ElementTree as ETree


__metaclass__ = type


def _iter_rules(root):
    for elem in root.findall('RegistrationGroups/Group'):
        prefix = elem.findtext('Prefix').replace('-', '')
        prefix_length = len(prefix)
        for subelem in elem.findall('Rules/Rule'):
            number_range = subelem.findtext('Range')
            lower, upper = number_range.split('-')
            lower_prefix = prefix + lower
            upper_prefix = prefix + upper
            length = int(subelem.findtext('Length'))
            if length > 0:
                item_idx = prefix_length + length
            else:
                item_idx = 0
            yield (lower_prefix, upper_prefix, prefix_length, item_idx)


file_name = os.path.join(os.path.dirname(__file__), "ISBN_Ranges.xml")

etree = ETree.parse(file_name)
root = etree.getroot()
rule_list = list(_iter_rules(root))


def lookup_isbn_prefix(digits):
    idx = max(bisect(rule_list, (digits,)) - 1, 0)
    lower_prefix, upper_prefix, registrant_idx, item_idx = rule_list[idx]
    if lower_prefix <= digits <= upper_prefix:
        if item_idx > 0:
            return (registrant_idx, item_idx)
        raise ValueError("Excluded prefix range: '" + lower_prefix + "' - '" +
                         upper_prefix + "'.")
    if lower_prefix[:3] != digits[:3]:
        raise ValueError("Undefined prefix.")
    raise ValueError("Undefined registration group or registrant.")
