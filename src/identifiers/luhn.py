# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Name:        luhn
# Purpose:     Luhn algorithm, a simple checksum formula used to validate a
#              variety of identification numbers
#
# Author:      Michael Amrhein (michael@adrhinum.de)
#
# Copyright:   (c) 2017 Michael Amrhein
# License:     This program is part of a larger application. For license
#              details please read the file LICENSE.TXT provided together
#              with the application.
# ----------------------------------------------------------------------------
# $Source$
# $Revision$


"""Luhn algorithm, a simple checksum formula used to validate a variety of
identification numbers"""


# standard library imports
from string import ascii_uppercase, digits

# third-party imports

# local imports


# A straight forward implementation of the Luhn algorithm could look like
# this:
#
# def luhn(digits):
#     """Return the Luhn check digit for the given numerical string."""
#     parity = (len(digits) + 1) % 2
#     cum = 0
#     for idx, digit in enumerate([int(d) for d in digits]):
#         if idx % 2 == parity:
#             digit *= 2
#             if digit > 9:
#                 digit -= 9
#         cum += digit
#     return 10 - cum % 10
#
# The original Luhn algorithms does only operate on numerical identifiers. In
# order to make it applicable to alpha-numerical identifiers (containing
# digits and ascii letters), the extended version provided here allows to
# transform the input string into a sequence of digits by mapping the letters
# A - Z into 10 - 35 using the following list.
_ALPHABET = digits + ascii_uppercase

# For enhanced performance, the implementation provided here uses an array of
# two pre-calculated values for each character, one used for characters at odd
# positions and one for characters at even positions.
#
# The array was calculated by the following algorithm:
#
# def pre_calc_list():
#     values = []
#     for idx, char in enumerate(_ALPHABET):
#         # for odd positions (parity = 0)
#         if idx < 10:
#             val_if_pos_odd = idx
#             next_parity_if_pos_odd = 1
#         else:
#             q, r = divmod(idx, 10)
#             val_if_pos_odd = 2 * q + r
#             next_parity_if_pos_odd = 0
#         # for even positions (parity = 1)
#         if idx < 10:
#             val_if_pos_even = 2 * idx
#             if val_if_pos_even > 9:
#                 val_if_pos_even -= 9
#             next_parity_if_pos_even = 0
#         else:
#             q, r = divmod(idx, 10)
#             r *= 2
#             if r > 9:
#                 r -= 9
#             val_if_pos_even = q + r
#             next_parity_if_pos_even = 1
#         values.append(((val_if_pos_odd, next_parity_if_pos_odd),
#                        (val_if_pos_even, next_parity_if_pos_even)))
#     return values

_PRE_CALC = [
    ((0, 1), (0, 0)),
    ((1, 1), (2, 0)),
    ((2, 1), (4, 0)),
    ((3, 1), (6, 0)),
    ((4, 1), (8, 0)),
    ((5, 1), (1, 0)),
    ((6, 1), (3, 0)),
    ((7, 1), (5, 0)),
    ((8, 1), (7, 0)),
    ((9, 1), (9, 0)),
    ((2, 0), (1, 1)),
    ((3, 0), (3, 1)),
    ((4, 0), (5, 1)),
    ((5, 0), (7, 1)),
    ((6, 0), (9, 1)),
    ((7, 0), (2, 1)),
    ((8, 0), (4, 1)),
    ((9, 0), (6, 1)),
    ((10, 0), (8, 1)),
    ((11, 0), (10, 1)),
    ((4, 0), (2, 1)),
    ((5, 0), (4, 1)),
    ((6, 0), (6, 1)),
    ((7, 0), (8, 1)),
    ((8, 0), (10, 1)),
    ((9, 0), (3, 1)),
    ((10, 0), (5, 1)),
    ((11, 0), (7, 1)),
    ((12, 0), (9, 1)),
    ((13, 0), (11, 1)),
    ((6, 0), (3, 1)),
    ((7, 0), (5, 1)),
    ((8, 0), (7, 1)),
    ((9, 0), (9, 1)),
    ((10, 0), (11, 1)),
    ((11, 0), (4, 1))
]


def luhn(base, num_only=False, allow_lower_case=False):
    """Return the Luhn check digit for the given string.

    Args:
        base(str): string for which to calculate the check digit
        num_only(bool): allow only digits in `base` (default: False)
        allow_lower_case(bool): allow lower case letters in `base`
            (default: False)

    Returns:
        int: Luhn check digit

    Raises:
        ValueError: given `base` contains an unallowed character
    """
    if num_only:
        alphabet = _ALPHABET[:10]
    else:
        alphabet = _ALPHABET
    if allow_lower_case:
        base = base.upper()
    try:
        pre_calc = (_PRE_CALC[alphabet.index(c)] for c in reversed(base))
        cum = 0
        parity = 1
        for elem in pre_calc:
            val, parity = elem[parity]
            cum += val
    except ValueError:
        pass    # fall through
    else:
        return 10 - cum % 10
    # unallowed character detected
    if num_only:
        msg = 'The string given must only contain digits.'
    elif allow_lower_case:
        msg = 'The string given must only contain digits and ascii letters.'
    else:
        msg = 'The string given must only contain digits and upper case ' \
              'ascii letters.'
    raise ValueError(msg)
