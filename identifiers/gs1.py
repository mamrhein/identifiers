# -*- coding: utf-8 -*-
##----------------------------------------------------------------------------
## Name:        GS1 identifiers
## Purpose:     Identifiers standardized by gs1.org
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


"""Identifiers standardized by gs1.org"""


from __future__ import absolute_import
from abc import abstractproperty
from .identifier import Identifier
from .gs1utils import lookup_company_prefix


__metaclass__ = type


class GS1NumericalIdentifier(Identifier):

    """Abstract base class for numerical identifiers defined by the GS1
    organization.

    Note: This is the base only for the numerical GS1 identifiers
          having a fixed length and a check digit at the end.
    """

    __slots__ = ('_ref_idx')

    @staticmethod
    def lookup_prefix(digits):
        return lookup_company_prefix(digits)

    @staticmethod
    def calc_check_digit(digits):
        """Calculate and return the GS1 check digit."""
        ints = [int(d) for d in digits]
        l = len(ints)
        odds = slice((l - 1) % 2, l, 2)
        even = slice(l % 2, l, 2)
        checksum = 3 * sum(ints[odds]) + sum(ints[even])
        return str(-checksum % 10)

    @abstractproperty
    def LENGTH(self):
        pass

    @abstractproperty
    def EXTRA_DIGITS(self):
        pass

    @property
    def gs1_prefix(self):
        """Return the identifier's GS1 prefix part."""
        offset = self.EXTRA_DIGITS
        return self._id[offset:offset + 3]

    @property
    def company_prefix(self):
        """Return the identifier's company prefix part."""
        offset = self.EXTRA_DIGITS
        return self._id[offset:self._ref_idx]

    @property
    def _reference(self):
        """Return the identifier's reference part."""
        return self._id[self._ref_idx:-1]

    @property
    def check_digit(self):
        """Return the identifier's check digit."""
        return self._id[-1]

    def __init__(self, *args):
        n_args = len(args)
        if n_args == 1:
            digits = args[0]
            if not digits.isnumeric():
                raise ValueError("Argument must only contain digits.")
            offset = self.EXTRA_DIGITS
            ref_idx = self.__class__.lookup_prefix(digits[offset:]) + offset
            n_digits = len(digits)
            if n_digits == self.LENGTH:
                check_digit = self.__class__.calc_check_digit(digits[:-1])
                if check_digit != digits[-1]:
                    raise ValueError("Wrong check digit; should be '" +
                                     check_digit + "'.")
            elif n_digits == self.LENGTH - 1:
                check_digit = self.__class__.calc_check_digit(digits)
                digits += check_digit
            else:
                raise ValueError("Argument must have " + str(self.LENGTH) +
                                 " or " + str(self.LENGTH - 1) + " digits.")
        elif 3 <= n_args <= 4:
            digits = ''.join(args)
            if not digits.isnumeric():
                raise ValueError("Arguments must only contain digits.")
            offset = self.EXTRA_DIGITS
            ref_idx = self.__class__.lookup_prefix(digits[offset:]) + offset
            if len(args[0]) != 3:
                raise ValueError("Undefined GS1 prefix: " + args[0] + "'.")
            if len(''.join(args[:2])) != ref_idx:
                raise ValueError("Undefined company prefix: '" +
                                 args[1] + "'.")
            n_digits = len(digits)
            if n_args == 4 and n_digits == self.LENGTH:
                check_digit = self.__class__.calc_check_digit(digits[:-1])
                if check_digit != digits[-1]:
                    raise ValueError("Wrong check digit; should be '" +
                                     check_digit + "'.")
            elif n_args == 3 and n_digits == self.LENGTH - 1:
                check_digit = self.__class__.calc_check_digit(digits)
                digits += check_digit
            else:
                raise ValueError(str(n_args) + " arguments must contain " +
                                 str(self.LENGTH + n_args - 4) + " digits.")
        else:
            raise TypeError("One, three or four arguments required, " +
                            str(n_args) + " given.")
        self._id = digits
        self._ref_idx = ref_idx

    def __str__(self):
        """str(self)"""
        return str(self._id)

    def elements(self):
        """Return the identifier's elements as tuple."""
        offset = self.EXTRA_DIGITS
        if offset:
            return (self._id[:offset], self.company_prefix, self._reference,
                    self.check_digit)
        else:
            return (self.company_prefix, self._reference, self.check_digit)

    def separated(self, separator='-'):
        """Return a string representation of the identifier with its elements
        separated by the given separator."""
        return separator.join((part for part in self.elements() if part))


class GTIN(GS1NumericalIdentifier):

    """Global Trade Item Number

    Used to identify products and services.
    """

    __slots__ = ()

    item_reference = GS1NumericalIdentifier._reference


class GTIN_12(GTIN):

    """Global Trade Item Number (12 digits)

    Used to identify products and services.
    """

    __slots__ = ()

    LENGTH = 12
    EXTRA_DIGITS = 0

    @staticmethod
    def lookup_prefix(digits):
        return lookup_company_prefix('0' + digits)


class GTIN_13(GTIN):

    """Global Trade Item Number (13 digits)

    Used to identify products and services.
    """

    __slots__ = ()

    LENGTH = 13
    EXTRA_DIGITS = 0


class GTIN_14(GTIN):

    """Global Trade Item Number (14 digits)

    Used to identify products and services.
    """

    __slots__ = ()

    LENGTH = 14
    EXTRA_DIGITS = 1

    @property
    def level_indicator(self):
        return self._id[0]

    def __init__(self, *args):
        n_args = len(args)
        if n_args == 1:
            arg = args[0]
            if isinstance(arg, (GTIN_13, GTIN_12)):
                pad = self.LENGTH - arg.LENGTH
                self._id = '0' * pad + arg._id
                self._ref_idx = arg._ref_idx + pad
            else:
                super(GTIN_14, self).__init__(*args)


class GLN(GS1NumericalIdentifier):

    """Global Location Number

    Used to identify parties and locations, for example companies, warehouses,
    factories and stores.
    """

    __slots__ = ()

    LENGTH = 13
    EXTRA_DIGITS = 0

    location_reference = GS1NumericalIdentifier._reference


class SSCC(GS1NumericalIdentifier):

    """Serial Shipping Container Code

    Used to identify logistics units, for example loads on pallets,
    roll cages or parcels.
    """

    __slots__ = ()

    LENGTH = 18
    EXTRA_DIGITS = 1

    serial_reference = GS1NumericalIdentifier._reference


class GSIN(GS1NumericalIdentifier):

    """Global Shipment Identification Number

    Used to identify shipments, i. e. logistics units delivered to a customer
    together.
    """

    __slots__ = ()

    LENGTH = 17
    EXTRA_DIGITS = 0

    shipper_reference = GS1NumericalIdentifier._reference
