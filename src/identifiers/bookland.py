# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Name:        bookland
# Purpose:     International standard identifiers for books, book-like
#              publications, periodicals and notated music
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


r"""International standard identifiers for books, book-like publications,
periodicals and notated music
"""

import re
from typing import Optional, Tuple, Union

from .identifier import Identifier
from .gs1 import GTIN13
from .isbnutils import lookup_isbn_prefix
from .ismnutils import lookup_ismn_prefix


_pattern_1 = re.compile(r'^(\d+)-(\d+)-(\d+)-(\d+)(?:-(\d))?$')
_pattern_2 = re.compile(r'^(\d+) (\d+) (\d+) (\d+)(?: (\d))?$')


class _BooklandGTIN(GTIN13):
    """Base class for the "bookland" GTINs."""

    __slots__ = '_registrant_idx'

    @property
    def registration_group(self) -> str:
        """Return the Registration Group of the identifier."""
        return self._id[3:self._registrant_idx]

    @property
    def registrant(self) -> str:
        """Return the Registrant of the identifier."""
        return self._id[self._registrant_idx:self._ref_idx]

    publication = GTIN13.item_reference

    # noinspection PyMissingConstructor
    def __init__(self, *args) -> None:
        """An instance of {cls} can be created in two ways, by providing a
        Unicode string representation of an {cls} or by providing a GS1
        prefix, a registration group, a registrant, a publication number and,
        optionally, a check digit.

        **1. Form**

        Args:
            id (str): string representation of an {cls}

        Returns:
            instance of :class:`{cls}`

        Raises:
            TypeError: given `id` is not a str
            ValueError: given `id` contains wrong check digit
            ValueError: given `id` does not follow the format required for an
                {cls}

        **2. Form**

        Args:
            gs1_prefix (str): 3-digit GS1 prefix
            registration_group (str): number identifying the
                local registration authority
            registrant (str): number identifying
                the publishing company
            publication (str): number identifying
                the publication
            check_digit (str): 1-digit number (optional)

        Returns:
            instance of :class:`{cls}`

        Raises:
            TypeError: invalid number of arguments
            TypeError: a given argument is not a Unicode string
            ValueError: a given argument contains character(s) other than
                digits 0-9
            ValueError: given `gs1_prefix` not valid
            ValueError: given `registration_group` not valid
            ValueError: given `registrant` not valid
            ValueError: combined length of arguments not valid
            ValueError: wrong check digit
        """
        if not all(isinstance(arg, str) for arg in args):
            raise TypeError("All arguments must be instances of 'str'.")
        n_args = len(args)
        if n_args == 1:
            digits = args[0].strip()
            if not digits.isnumeric():
                # canonical form given?
                match = _pattern_1.match(digits) or _pattern_2.match(digits)
                if match:
                    parts = match.groups()
                    if parts[4] is None:  # check digit omitted
                        self.__init__(*parts[:4])
                        return
                    else:
                        self.__init__(*parts)
                        return
                else:
                    raise ValueError("Argument must only contain digits "
                                     "or be a string formatted as "
                                     f"{self.__class__.__name__}.")
            reg_idx, ref_idx = self.__class__.lookup_prefix(digits)
            n_digits = len(digits)
            if n_digits == self.LENGTH:
                check_digit = self.__class__.calc_check_digit(digits[:-1])
                if check_digit != digits[-1]:
                    raise ValueError("Wrong check digit; should be '"
                                     f"{check_digit}'.")
            elif n_digits == self.LENGTH - 1:
                check_digit = self.__class__.calc_check_digit(digits)
                digits += check_digit
            else:
                raise ValueError(f"Argument must have {self.LENGTH}"
                                 f" or {self.LENGTH - 1} digits.")
        elif 4 <= n_args <= 5:
            digits = ''.join(args)
            if not digits.isnumeric():
                raise ValueError("Arguments must only contain digits.")
            reg_idx, ref_idx = self.__class__.lookup_prefix(digits)
            if len(args[0]) != 3:
                raise ValueError(f"Undefined GS1 prefix: '{args[0]}'.")
            if len(''.join(args[:2])) != reg_idx:
                raise ValueError("Undefined registration group: '" 
                                 f"{args[1]}'.")
            if len(''.join(args[:3])) != ref_idx:
                raise ValueError(f"Undefined registrant: '{args[2]}'.")
            n_digits = len(digits)
            if n_args == 5 and n_digits == self.LENGTH:
                check_digit = self.__class__.calc_check_digit(digits[:-1])
                if check_digit != digits[-1]:
                    raise ValueError("Wrong check digit; should be '"
                                     f"{check_digit}'.")
            elif n_args == 4 and n_digits == self.LENGTH - 1:
                check_digit = self.__class__.calc_check_digit(digits)
                digits += check_digit
            else:
                raise ValueError(f"{n_args} arguments must contain " 
                                 f"{self.LENGTH + n_args - 5} digits.")
        else:
            raise TypeError("One, four or five arguments required, "
                            f"{n_args} given.")
        self._id = digits
        self._registrant_idx = reg_idx
        self._ref_idx = ref_idx

    def elements(self) -> Tuple[str, str, str, str, str]:
        """Return the identifier's elements (gs1_prefix, registration_group,
        registrant, publication, check_digit) as tuple."""
        return (self.gs1_prefix, self.registration_group, self.registrant,
                self.publication, self.check_digit)

    def __str__(self) -> str:
        """str(self)"""
        # prefixing the number with the acronym of the identifier is
        # recommended by the standard
        return self.__class__.__name__ + ' ' + self.separated()


class ISBN(_BooklandGTIN):
    """International Standard Book Number

    The ISBN is a unique international identifier for monographic
    publications.

    Each ISBN consists of 13 digits. It contains a 3-digits GS1 prefix ('978'
    or '979'), a Registration Group, denoting the local registration
    authority, a number denoting the Registrant, i. e. the company which
    registered the ISBN, a number denoting the Publication and a check digit.
    """

    __slots__ = ()

    @staticmethod
    def lookup_prefix(digits: str) -> Tuple[int, int]:
        """Check ISBN prefix in `digits`."""
        return lookup_isbn_prefix(digits)

    def __init__(self, *args) -> None:
        super(ISBN, self).__init__(*args)

    __init__.__doc__ = _BooklandGTIN.__init__.__doc__.format(cls='ISBN')


class ISMN(_BooklandGTIN):
    """International Standard Music Number

    The ISMN is a unique international identifier of all notated music
    publications, whether available for sale, hire or gratis, whether a part,
    a score, or an element in a multi-media kit.

    Each ISMN consists of 13 digits. It contains a 3-digits GS1 prefix
    ('979'), a Registration Group ('0'), a number denoting the Registrant, i.
    e. the company which registered the ISMN, a number denoting the
    Publication and a check digit.
    """

    __slots__ = ()

    @staticmethod
    def lookup_prefix(digits: str) -> Tuple[int, int]:
        """Check ISMN prefix in `digits`."""
        return lookup_ismn_prefix(digits)

    def __init__(self, *args) -> None:
        super(ISMN, self).__init__(*args)

    __init__.__doc__ = _BooklandGTIN.__init__.__doc__.format(cls='ISMN')


class ISSN(Identifier):
    """International Standard Serial Number

    The ISSN is used to identify newspapers, journals, magazines and
    periodicals of all kinds and on all media - print and electronic."""

    __slots__ = ()

    @staticmethod
    def calc_check_digit(digits: str) -> str:
        """Calculate ISSN check digit from `digits`."""
        checksum = sum((weight * int(digit)
                        for weight, digit
                        in zip(range(len(digits) + 1, 1, -1), digits)))
        rem = -checksum % 11
        return str(rem) if rem != 10 else 'X'

    @property
    def raw_number(self) -> str:
        """Return the ISSN without check digit."""
        return self._id[:-1]

    @property
    def check_digit(self) -> str:
        """Return the ISSN's check digit."""
        return self._id[-1]

    # noinspection PyMissingConstructor
    def __init__(self, digits: str) -> None:
        """Args:
            digits (str): string representation of the ISSN

        The argument must be a string with 8 digits, with 7 digits or with 7
        digits followed by an 'X', optionally separated by a blank or a hyphen
        after the fourth digit.

        Returns:
            instance of :class:`ISSN`

        Raises:
            ValueError: given arg has invalid format
            ValueError: given arg contains wrong check digit
        """
        if not isinstance(digits, str):
            raise TypeError("Argument must be instance of 'str'.")
        try:
            if digits[4] in ('-', ' '):
                digits = digits[:4] + digits[5:]
        except IndexError:
            pass
        else:
            n_digits = len(digits)
            if n_digits == 7 and digits.isnumeric():
                check_digit = self.__class__.calc_check_digit(digits)
                self._id = digits + check_digit
                return
            if n_digits == 8 and digits[:-1].isnumeric():
                check_digit = self.__class__.calc_check_digit(digits[:-1])
                if check_digit == digits[-1]:
                    self._id = digits
                    return
                else:
                    raise ValueError("Wrong check digit; should be '" 
                                     f"{check_digit}'.")
        raise ValueError("Argument must be a string with 8 digits, "
                         "with 7 digits or with 7 digits followed "
                         "by an 'X', optionally separated by a blank "
                         "or a hyphen after the fourth digit.")

    def as_gtin(self, addon = None) -> "ISSN13":
        """Return GTIN13 created from `self` + `addon`."""
        return ISSN13(self, addon)

    def separated(self, separator: Optional[str] = '-') -> str:
        """Return ISSN as string, optionally split by `separator`."""
        return separator.join((self._id[:4], self._id[4:]))

    def __str__(self) -> str:
        """str(self)"""
        # prefixing the number with the acronym of the identifier is
        # recommended by the standard
        return self.__class__.__name__ + ' ' + self.separated()


class ISSN13(GTIN13):
    """International Standard Serial Number (as GTIN)

    The ISSN is used to identify newspapers, journals, magazines and
    periodicals of all kinds and on all media - print and electronic.

    As GTIN it is used mainly to create an EAN-13 barcode."""

    __slots__ = ()

    @staticmethod
    def lookup_prefix(digits: str) -> int:
        """Check for ISSN prefix in `digits`."""
        if digits.startswith('977'):
            return 3
        raise ValueError("ISSN prefix must be '977'.")

    def __init__(self, serial_number: Union[ISSN, str],
                 addon: Optional[str] = None) -> None:
        if isinstance(serial_number, ISSN):
            if addon is None:
                digits = '977' + serial_number.raw_number + '00'
            elif isinstance(addon, str):
                if len(addon) != 2 or not addon.isnumeric():
                    raise ValueError("'addon', if given, must be a string "
                                     "containing 2 digits.")
                digits = '977' + serial_number.raw_number + addon
            else:
                raise TypeError("'addon' must be an instance of 'str'.")
            super(ISSN13, self).__init__(digits)
        elif isinstance(serial_number, str):
            try:
                issn = ISSN(serial_number)
            except ValueError:
                # given serial number is not an ISSN
                if addon is not None:
                    raise TypeError("'addon' must only be given together "
                                    "with an ISSN.")
                super(ISSN13, self).__init__(serial_number)
            else:
                self.__init__(issn, addon)
        else:
            raise TypeError("`serial_number` must be an ISSN or a string "
                            "representing an ISSN or a GTIN with prefix "
                            "'977'.")

    def extract_issn(self) -> ISSN:
        """Return the ISSN encoded in `self`."""
        return ISSN(self._id[3:10])
