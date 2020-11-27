# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Name:        GS1 identifiers
# Purpose:     Identifiers standardized by gs1.org
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


"""Identifiers standardized by gs1.org"""


from abc import abstractmethod
from .identifier import Identifier
from .gs1utils import lookup_company_prefix


class GS1NumericalIdentifier(Identifier):

    """Abstract base class for numerical identifiers defined by the GS1
    organization.

    Note: This is the base only for the numerical GS1 identifiers
          having a fixed length and a check digit at the end.
    """

    __slots__ = '_ref_idx'

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

    # noinspection PyPep8Naming
    @property
    @abstractmethod
    def LENGTH(self):
        pass

    # noinspection PyPep8Naming
    @property
    @abstractmethod
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
        """An instance of {cls} can be created in two ways, by providing a
        Unicode string representation of a {cls} or by providing the {cls}'s
        elements as separate arguments.

        **1. Form**

        Args:
            id (`Unicode string`): string representation of a {cls} (with or
                without a check digit)

        If `id` does not include a check digit, it is calculated and appended
        automatically.

        Returns:
            instance of :class:`{cls}`

        Raises:
            TypeError: given `id` is not a `Unicode string`
            ValueError: given `id` contains character(s) other than digits 0-9
            ValueError: given `id` contains wrong check digit
            ValueError: length of given `id` not valid

        **2. Form**

        Args:
            {extra_arg}
            company_prefix (`Unicode string`): number identifying the company
                issuing the identifier, starting with a 3-digit GS1 prefix
            {item_ref} (`Unicode string`): number identifying the {item}
            check_digit (`Unicode string`): 1-digit number (optional)

        If `check_digit` is omitted, it is calculated and appended
        automatically.

        Returns:
            instance of :class:`{cls}`

        Raises:
            TypeError: invalid number of arguments
            TypeError: a given argument is not a Unicode string
            ValueError: a given argument contains character(s) other than
                digits 0-9
            ValueError: length of given `company_prefix` not valid
            ValueError: given `company_prefix` not valid
            ValueError: length of given `{item_ref}` not valid
            ValueError: invalid check digit
        """
        if not all(isinstance(arg, str) for arg in args):
            raise TypeError("All arguments must be instances of %s." % str)
        n_args = len(args)
        # 1. form: one argument given
        if n_args == 1:
            digits = args[0]
            if not digits.isnumeric():
                raise ValueError("Argument must only contain digits.")
            n_digits = len(digits)
            offset = self.EXTRA_DIGITS
            ref_idx = self.__class__.lookup_prefix(digits[offset:]) + offset
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
        # 2. form: single elements given
        else:
            error_msg = None
            extra_arg = min(self.EXTRA_DIGITS, 1)
            if extra_arg:
                try:
                    extra_digits, company_prefix, ref_elem, check_digit = args
                except ValueError:
                    try:
                        extra_digits, company_prefix, ref_elem = args
                    except ValueError:  # wrong number of arguments
                        error_msg = \
                            "One, three or four arguments required, {} given."
                    else:
                        check_digit = None
            else:
                extra_digits = ''
                try:
                    company_prefix, ref_elem, check_digit = args
                except ValueError:
                    try:
                        company_prefix, ref_elem = args
                    except ValueError:  # wrong number of arguments
                        error_msg = \
                            "One, two or three arguments required, {} given."
                    else:
                        check_digit = None
            if error_msg:   # wrong number of arguments
                raise TypeError(error_msg.format(n_args))
            digits = ''.join(args)
            if not digits.isnumeric():
                raise ValueError("Arguments must only contain digits.")
            offset = self.EXTRA_DIGITS
            if offset and len(extra_digits) != offset:
                raise ValueError("First element must contain " + str(offset) +
                                 " digit" + "s" * min(offset - 1, 1) +
                                 ", " + str(len(extra_digits)) + " given.")
            ref_idx = self.__class__.lookup_prefix(digits[offset:]) + offset
            if len(company_prefix) + offset != ref_idx:
                raise ValueError("Undefined company prefix: '" +
                                 company_prefix + "'.")
            len_ref_elem = self.LENGTH - ref_idx - 1
            if len(ref_elem) != len_ref_elem:
                raise ValueError(("Second", "Third")[extra_arg] +
                                 " argument must contain " +
                                 str(len_ref_elem) + " digits.")
            if check_digit:
                if len(check_digit) != 1:
                    raise ValueError("Check digit must only be one digit.")
                valid_check_digit = \
                    self.__class__.calc_check_digit(digits[:-1])
                if check_digit != valid_check_digit:
                    raise ValueError("Wrong check digit; should be '" +
                                     valid_check_digit + "'.")
            else:
                check_digit = self.__class__.calc_check_digit(digits)
                digits += check_digit
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


def _make_init_doc(cls, extra_arg='', item_ref='', item=''):
    doc = GS1NumericalIdentifier.__init__.__doc__

    def deco(meth):
        meth.__doc__ = doc.format(cls=cls, extra_arg=extra_arg,
                                  item_ref=item_ref, item=item)
        return meth

    return deco


class GTIN(GS1NumericalIdentifier):

    """Global Trade Item Number

    Used to identify products and services.
    """

    __slots__ = ()

    item_reference = GS1NumericalIdentifier._reference


class GTIN12(GTIN):

    """Global Trade Item Number (12 digits)

    Used to identify products and services.
    """

    __slots__ = ()

    LENGTH = 12
    EXTRA_DIGITS = 0

    @_make_init_doc('GTIN12', item_ref='item_reference', item='trade item')
    def __init__(self, *args):
        super(GTIN12, self).__init__(*args)


class GTIN13(GTIN):

    """Global Trade Item Number (13 digits)

    Used to identify products and services.
    """

    __slots__ = ()

    LENGTH = 13
    EXTRA_DIGITS = 0

    @_make_init_doc('GTIN13', item_ref='item_reference', item='trade item')
    def __init__(self, *args):
        super(GTIN13, self).__init__(*args)


class GTIN14(GTIN):

    """Global Trade Item Number (14 digits)

    Used to identify products and services.
    """

    __slots__ = ()

    LENGTH = 14
    EXTRA_DIGITS = 1

    @property
    def level_indicator(self):
        """Return the identifier's level indicator (i.e. the first digit)."""
        return self._id[0]

    def __init__(self, *args):
        """An instance of GTIN14 can be created in three ways, by providing a
        GTIN12 or GTIN13, by providing a Unicode string representation of a
        GTIN14 or by providing the GTIN14's elements as separate arguments.

        **1. Form**

        Args:
            gtin (`GTIN12` or `GTIN13`): GTIN to be expanded to a GTIN14

        Returns:
            instance of :class:`GTIN14`

        **2. Form**

        Args:
            id (`Unicode string`): string representation of a GTIN14 (with or
                without a check digit)

        If `id` does not include a check digit, it is calculated and appended
        automatically.

        Returns:
            instance of :class:`GTIN14`

        Raises:
            TypeError: given `id` is not a `Unicode string`
            ValueError: given `id` contains character(s) other than digits 0-9
            ValueError: given `id` contains wrong check digit
            ValueError: length of given `id` not valid

        **3. Form**

        Args:
            level_indicator (`Unicode string`): 1-digit number providing
                additional name space
            company_prefix (`Unicode string`): number identifying the company
                issuing the identifier, starting with a 3-digit GS1 prefix
            item_reference (`Unicode string`): number identifying the trade
                item
            check_digit (`Unicode string`): 1-digit number (optional)

        If `check_digit` is omitted, it is calculated and appended
        automatically.

        Returns:
            instance of :class:`GTIN14`

        Raises:
            TypeError: invalid number of arguments
            TypeError: a given argument is not a Unicode string
            ValueError: a given argument contains character(s) other than
                digits 0-9
            ValueError: length of given `company_prefix` not valid
            ValueError: given `company_prefix` not valid
            ValueError: length of given `item_reference` not valid
            ValueError: invalid check digit
        """
        if len(args) == 1:
            arg = args[0]
            if isinstance(arg, (GTIN13, GTIN12)):
                pad = self.LENGTH - arg.LENGTH
                self._id = '0' * pad + arg._id
                self._ref_idx = arg._ref_idx + pad
                return
        super(GTIN14, self).__init__(*args)


class GLN(GS1NumericalIdentifier):

    """Global Location Number

    Used to identify parties and locations, for example companies, warehouses,
    factories and stores.
    """

    __slots__ = ()

    LENGTH = 13
    EXTRA_DIGITS = 0

    location_reference = GS1NumericalIdentifier._reference

    @_make_init_doc('GLN', item_ref='location_reference', item='location')
    def __init__(self, *args):
        super(GLN, self).__init__(*args)


class SSCC(GS1NumericalIdentifier):

    """Serial Shipping Container Code

    Used to identify logistics units, for example loads on pallets,
    roll cages or parcels.
    """

    __slots__ = ()

    LENGTH = 18
    EXTRA_DIGITS = 1

    serial_reference = GS1NumericalIdentifier._reference

    @property
    def extension_digit(self):
        """Return the identifier's extension digit (i.e. the first digit)."""
        return self._id[0]

    @_make_init_doc('SSCC', extra_arg='extension_digit (`Unicode string`) '
                    '1-digit number providing additional name space',
                    item_ref='serial_reference',
                    item='shipping container')
    def __init__(self, *args):
        super(SSCC, self).__init__(*args)


class GSIN(GS1NumericalIdentifier):

    """Global Shipment Identification Number

    Used to identify shipments, i. e. logistics units delivered to a customer
    together.
    """

    __slots__ = ()

    LENGTH = 17
    EXTRA_DIGITS = 0

    shipper_reference = GS1NumericalIdentifier._reference

    @_make_init_doc('GSIN', item_ref='shipper_reference', item='shipment')
    def __init__(self, *args):
        super(GSIN, self).__init__(*args)
