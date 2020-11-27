# -*- coding: utf-8 -*-
##----------------------------------------------------------------------------
## Name:        gs1utils
## Purpose:     Utility functions for GS1 identifiers
##
## Author:      Michael Amrhein (mamrhein@users.sourceforge.net)
##
## Copyright:   (c) 2016 Michael Amrhein
## License:     This program is part of a larger application. For license
##              details please read the file LICENSE.TXT provided together
##              with the application.
##----------------------------------------------------------------------------
## $Source$
## $Revision$


"""Utility functions for GS1 identifiers"""


from __future__ import absolute_import
import os.path
from bisect import bisect
try:
    from xml.etree import cElementTree as ETree
except ImportError:
    from xml.etree import ElementTree as ETree


__metaclass__ = type


file_name = os.path.join(os.path.dirname(__file__), "GS1_CP_Ranges.xml")

etree = ETree.parse(file_name)
root = etree.getroot()
prefix_list = [(elem.get('prefix'), int(elem.get('gcpLength')))
               for elem in root.getchildren()]


def lookup_company_prefix(id):
    idx = bisect(prefix_list, (id,)) - 1
    prefix, cp_length = prefix_list[idx]
    if id.startswith(prefix):
        if cp_length > 0:
            return cp_length
        raise ValueError("Excluded prefix: '" + prefix + "'.")
    raise ValueError("Undefined prefix.")
