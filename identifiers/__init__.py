# -*- coding: utf-8 -*-
##----------------------------------------------------------------------------
## Name:        identifiers (package)
## Purpose:     Standardized identifiers for unique objects or unique classes
##              of objects
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


"""Standardized identifiers for unique objects or unique classes of objects.

Definition from Wikipedia:
"An identifier is a name that identifies (that is, labels the identity of)
either a unique object or a unique class of objects, where the "object" or
class may be an idea, physical [countable] object (or class thereof), or
physical [noncountable] substance (or class thereof). The abbreviation ID
often refers to identity, identification (the process of identifying), or an
identifier (that is, an instance of identification). An identifier may be a
word, number, letter, symbol, or any combination of those."
"""


# standard library imports
from __future__ import absolute_import

# local imports
from .banking import BIC, IBAN
from .bookland import ISBN, ISMN, ISSN
from .finance import MIC, ISIN
from .gs1 import GLN, GSIN, GTIN12, GTIN13, GTIN14, SSCC
from .identifier import Identifier


__version__ = 0, 2, 1


__all__ = [
    'Identifier',
    'GLN',
    'GSIN',
    'GTIN12',
    'GTIN13',
    'GTIN14',
    'SSCC',
    'ISBN',
    'ISMN',
    'ISSN',
    'BIC',
    'IBAN',
    'MIC',
    'ISIN'
]
