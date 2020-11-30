# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Name:        ibanutils
# Purpose:     Utility functions for checking IBANs
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


"""Utility functions for checking IBANs"""


# standard library imports
from string import ascii_uppercase, digits
from typing import Tuple


_ALPHABET = digits + ascii_uppercase


def calc_iban_check_digits(country_code: str, bban: str) -> str:
    """Calculate IBAN check digits from `country_code` and `bban`."""
    string = bban.upper() + country_code + '00'
    check_num = int(''.join((str(_ALPHABET.index(char))
                             for char in string)))
    return '%02i' % (98 - check_num % 97)


def split_iban(iban: str) -> Tuple[str, str, str]:
    """Split `iban` into country_code, check_digits and bban."""
    country_code, check_digits, bban = iban[:2], iban[2:4], iban[4:]
    return country_code, check_digits, bban


def check_iban_check_digits(iban: str) -> bool:
    """Return True if `iban` has correct check digits, otherwise False."""
    country_code, check_digits, bban = split_iban(iban)
    corr_check_digits = calc_iban_check_digits(country_code, bban)
    return check_digits == corr_check_digits
