# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Name:        finance
# Purpose:     International identifiers for tradable financial assets
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


"""International identifiers for tradable financial assets"""


# standard library imports
from string import ascii_uppercase, digits
from typing import Tuple

# third-party imports
from iso3166 import countries

# local imports
from .identifier import Identifier
from .luhn import luhn
from .micutils import get_mic_record


_ALPHABET = digits + ascii_uppercase


class MIC(Identifier):

    """Market Identifier Code

    A unique identification code used to identify securities trading
    exchanges, regulated and non-regulated trading markets.

    Each MIC is a four alpha character code, defined in ISO 10383.
    """

    __slots__ = ()

    # noinspection PyMissingConstructor
    def __init__(self, mic: str) -> None:
        """
        Args:
            mic (str): string representation of the MIC

        Returns:
            :class:`MIC` instance

        Raises:
            TypeError: given `mic` is not an instance of str
            ValueError: given `mic` not found in the registry
        """
        if not isinstance(mic, str):
            raise TypeError("Argument must be instance of 'str'.")
        mic = mic.strip()
        try:
            get_mic_record(mic)
        except KeyError:
            raise ValueError(f"Unknown MIC: '{mic}'.")
        self._id = mic

    def __str__(self) -> str:
        """str(self)"""
        return self._id


class ISIN(Identifier):

    """International Securities Identification Number

    An International Securities Identification Number uniquely identifies a
    tradable financial asset, a.k.a security.

    As defined in ISO 6166, each ISIN consists of a two-letter ISO 3166-1
    Country Code for the issuing country, followed by nine alpha-numeric
    characters (the National Securities Identifying Number, or NSIN, which
    identifies the security), and one numerical check digit, calculated by the
    Luhn algorithm.
    """

    __slots__ = ()

    # TODO: rename to calc_check_digit
    @staticmethod
    def calc_check_digits(country_code: str, nsin: str) -> str:
        """Calculate ISIN check digit."""
        return str(luhn(country_code + nsin))

    @property
    def country_code(self) -> str:
        """Return the ISIN's Country Code."""
        return self._id[:2]

    @property
    def check_digit(self) -> str:
        """Return the ISIN's check digits."""
        return self._id[-1]

    @property
    def nsin(self) -> str:
        """Return the ISIN's National Securities Identifying Number."""
        return self._id[2:-1]

    def elements(self) -> Tuple[str, str, str]:
        """Return the ISIN's Country Code, National Securities Identifying
        Number and check digit as tuple."""
        return self.country_code, self.nsin, self.check_digit

    # noinspection PyMissingConstructor
    def __init__(self, *args: str) -> None:
        """Instances of :class:`ISIN` can be created in two ways, by providing
        a Unicode string representation of an ISIN or by providing a country
        code and a national securities identifying number.

        **1. Form**

        Args:
            isin (str): string representation of an ISIN

        Returns:
            instance of :class:`ISIN`

        Raises:
            TypeError: given `isin` is not a `Unicode string`
            ValueError: given `isin` contains an unknown country code
            ValueError: given `isin` contains a wrong check digit
            ValueError: given `isin` must be 12 characters long
            ValueError: given `isin` contains invalid character(s)

        **2. Form**

        Args:
            country_code (str): 2-character country code
                according to ISO 3166
            nsin (str): national securities identifying
                number

        Returns:
            instance of :class:`ISIN`

        Raises:
            TypeError: invalid number of arguments
            TypeError: given `country_code` is not a `Unicode string`
            ValueError: given `country_code` contains an invalid or unknown
                country code
            TypeError: given `nsin` is not a `Unicode string`
            ValueError: length of given `nsin` not valid
            ValueError: given `nsin` contains invalid character(s)
        """
        n_args = len(args)
        if n_args == 1:
            arg0 = args[0]
            if not isinstance(arg0, str):
                raise TypeError("Argument must be instance of 'str'.")
            arg0 = arg0.strip()
            if len(arg0) != 12:
                raise ValueError('Invalid ISIN format: '
                                 'given string must be 12 characters long.')
            country_code = arg0[:2]
            try:
                countries.get(country_code)
            except KeyError:
                raise ValueError(f"Unknown country code: '{country_code}'.")
            nsin = arg0[2:-1]
            check_digit = self.__class__.calc_check_digits(country_code, nsin)
            if check_digit != arg0[-1]:
                raise ValueError("Wrong check digit; should be "
                                 f"'{check_digit}'.")
            self._id = arg0
        elif n_args == 2:
            arg0 = args[0]
            if not isinstance(arg0, str):
                raise TypeError("Country code must be instance of 'str'.")
            if len(arg0) != 2:
                raise ValueError("Country code must be a 2-character string.")
            country_code = arg0
            try:
                countries.get(country_code)
            except KeyError:
                raise ValueError(f"Unknown country code: '{country_code}'.")
            arg1 = args[1]
            if isinstance(arg1, str):
                len_nsin = len(arg1)
                if len_nsin == 9:
                    nsin = arg1
                elif 6 <= len_nsin < 9:
                    nsin = arg1.rjust(9, '0')
                else:
                    raise ValueError("Given NSIN must contain between 6 and 9"
                                     " characters.")
            else:
                raise TypeError("Given nsin must be instance of 'str'.")
            check_digit = self.__class__.calc_check_digits(country_code, nsin)
            self._id = ''.join((country_code, nsin, check_digit))
        else:
            raise TypeError('Invalid number of arguments.')

    def __str__(self) -> str:
        """str(self)"""
        return self._id
