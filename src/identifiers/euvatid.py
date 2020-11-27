# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Name:        euvatid
# Purpose:     European Union VAT Registration Numbers
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


"""European Union VAT Registration Numbers"""


# standard library imports
from __future__ import absolute_import, unicode_literals
from datetime import date
from itertools import chain
import re
from string import ascii_uppercase

# third-party imports

# local imports
from .identifier import Identifier

str = type(u'')


__metaclass__ = type


_VAT_ID_RULES = {}


# - AT - Austria -

def check_at(base, add=None):
    s1 = sum((int(c) for c in base[::2]))
    s2 = sum(chain(*(divmod(2 * int(c), 10) for c in base[1::2])))
    return str((96 - s1 - s2) % 10)

_VAT_ID_RULES['AT'] = (
    (re.compile('^U(?P<base>\d{7})(?P<check>\d)$'), check_at),
)


# - BE - Belgium -

def check_be(base, add=None):
    return '%02i' % (97 - int(base) % 97)

_VAT_ID_RULES['BE'] = (
    (re.compile('^(?P<base>0[1-9]\d{6})(?P<check>\d{2})$'), check_be),
)


# - BG - Bulgaria -

def check_bg_9d(base, add=None):
    weights = (1, 2, 3, 4, 5, 6, 7, 8)
    s = sum(w * int(c) for w, c in zip(weights, base))
    r = s % 11
    if r < 10:
        return str(r)
    weights = (3, 4, 5, 6, 7, 8, 9, 10)
    s = sum(w * int(c) for w, c in zip(weights, base))
    r = s % 11
    return str(r % 10)


def check_bg_ucn(base, add=None):
    year, month, day = int(base[:2]), int(base[2:4]), int(base[4:6])
    if month < 20:
        century = 1900
    elif 20 <= month < 40:
        month -= 20
        century = 1800
    else:
        month -= 40
        century = 2000
    try:
        birthdate = date(century + year, month, day)
    except ValueError:
        return 'f'          # invalid ucn
    else:
        if birthdate >= date.today():
            return 'f'      # invalid ucn
    weights = (2, 4, 8, 5, 10, 9, 7, 3, 6)
    s = sum(w * int(c) for w, c in zip(weights, base))
    r = s % 11
    return str(r % 10)


def check_bg_10d(base, add=None):
    weights = (21, 19, 17, 13, 11, 9, 7, 3, 1)
    s = sum(w * int(c) for w, c in zip(weights, base))
    return str(s % 10)

_VAT_ID_RULES['BG'] = (
    # legal entities
    (re.compile('^(?P<base>\d{8})(?P<check>\d)$'),
     check_bg_9d),
    # individuals (uniform civil number)
    (re.compile('^(?P<base>\d{2}([024][1-9]|[135][012])(0[1-9]|[12]\d|3[01])'
                '\d{3})(?P<check>\d)$'), check_bg_ucn),
    # foreigners
    (re.compile('^(?P<base>\d{9})(?P<check>\d)$'),
     check_bg_10d),
)


# - CY - Cyprus -

def check_cy(base, add=None):
    map = [1, 0, 5, 7, 9, 13, 15, 17, 19, 21]
    s1 = sum((int(c) for c in base[1::2]))
    s2 = sum((map[int(c)] for c in base[::2]))
    r = (s1 + s2) % 26
    return chr(ord('A') + r)

_VAT_ID_RULES['CY'] = (
    (re.compile('^(?P<base>[013-59]\d{7})(?P<check>[A-Z])$'), check_cy),
)


# - CZ - Czech Republic -

def _check_cz_date(s, variant='new'):
    y, m, d = int(s[:2]), int(s[2:4]), int(s[4:6])
    if m >= 50:
        m -= 50
    if variant == 'new' and y < 54:
        y += 2000
    else:
        y += 1900
    try:
        date(y, m, d)
    except ValueError:
        return False
    else:
        return True


def check_cz_10d(base, add=None):
    if not _check_cz_date(base):
        return 'f'                  # check failed
    parts = base[:2], base[2:4], base[4:6], base[6:8], base[8:]
    s = sum(int(p) for p in parts)
    if s % 11 == 0 and int(base) % 11 == 0:
        return ''                   # check ok
    else:
        return 'f'                  # check failed


def check_cz_9d(base, add=None):
    if _check_cz_date(base, 'old'):
        return ''                   # check ok
    else:
        return 'f'                  # check failed


def check_cz_sp(base, add=None):
    s = sum((8 - i) * int(c) for i, c in enumerate(base[1:]))
    return str(9 - (11 - s % 11) % 10)


def check_cz_8d(base, add=None):
    s = sum((8 - i) * int(c) for i, c in enumerate(base))
    return str((11 - s % 11) % 10)

_VAT_ID_RULES['CZ'] = (
    # 10-digit individuals (born 1.1.1954 or later)
    (re.compile('^(?P<base>\d{2}([05]\d|[16][0-2])(0[1-9]|[12]\d|3[01])\d{4})'
                '(?P<check>)$'), check_cz_10d),
    # 9-digit individuals (born before 1.1.1954)
    (re.compile('^(?P<base>([0-4]\d|5[0-3])'
                '([05]\d|[16][0-2])(0[1-9]|[12]\d|3[01])\d{3})'
                '(?P<check>)$'), check_cz_9d),
    # special cases
    (re.compile('^(?P<base>6\d{7})(?P<check>\d)$'), check_cz_sp),
    # legal entities
    (re.compile('^(?P<base>[0-8]\d{6})(?P<check>\d)$'), check_cz_8d),
)


# - DE - Germany -

def check_de(base, add=None):
    p = 10
    for c in base:
        s = int(c) + p
        m = s % 10
        if m == 0:
            m = 10
        p = (2 * m) % 11
    return str((11 - p) % 10)

_VAT_ID_RULES['DE'] = (
    (re.compile('^(?P<base>\d{8})(?P<check>\d)$'), check_de),
)


# - DK - Denmark -

def check_dk(base, add=None):
    weights = (2, 7, 6, 5, 4, 3, 2, 1)
    s = sum(int(c) * w for (c, w) in zip(base, weights))
    r = s % 11
    if r == 0:
        return ''            # check ok
    else:
        return 'f'           # check failed

_VAT_ID_RULES['DK'] = (
    (re.compile('^(?P<base>[1-9]\d{7})(?P<check>)$'), check_dk),
)


# - EE - Estonia -

def check_ee(base, add=None):
    weights = (3, 7, 1, 3, 7, 1, 3, 7)
    s = sum(int(c) * w for (c, w) in zip(base, weights))
    r = s % 10
    if r == 0:
        return '0'
    else:
        return str(10 - r)

_VAT_ID_RULES['EE'] = (
    (re.compile('^(?P<base>\d{8})(?P<check>\d)$'), check_ee),
)


# - ES - Spain -

_ES_CC_MAP = 'TRWAGMYFPDXBNJZSQVHLCKE'


def check_es_prof(base, add=None):
    s1 = sum(chain(*(divmod(2 * int(c), 10) for c in base[1::2])))
    s2 = sum((int(c) for c in base[2::2]))
    r = (s1 + s2) % 10
    if r == 0:
        return '0'
    else:
        return str(10 - r)


def check_es_non_prof(base, add=None):
    s1 = sum(chain(*(divmod(2 * int(c), 10) for c in base[1::2])))
    s2 = sum((int(c) for c in base[2::2]))
    i = 9 - (s1 + s2) % 10
    return ascii_uppercase[i]


def check_es_dom(base, add=None):
    i = int(base) % 23
    return _ES_CC_MAP[i]


def check_es_other(base, add=None):
    i = int(base[1:]) % 23
    return _ES_CC_MAP[i]

_VAT_ID_RULES['ES'] = (
    # legal entities with profit aim
    (re.compile('^(?P<base>[A-H,JVU]\d{7})(?P<check>\d)$'), check_es_prof),
    # legal entities with non-profit aim
    (re.compile('^(?P<base>[NP-SW]\d{7})(?P<check>[A-J])$'),
     check_es_non_prof),
    # domestic natural persons with national identity card
    (re.compile('^(?P<base>\d{8})(?P<check>[A-Z])$'), check_es_dom),
    # other natural persons
    (re.compile('^(?P<base>[KLMXYZ]\d{7})(?P<check>[A-Z])$'), check_es_other),
)


# - FI - Finland -

def check_fi(base, add=None):
    weights = (7, 9, 10, 5, 8, 4, 2)
    s = sum(int(c) * w for (c, w) in zip(base, weights))
    r = s % 11
    if r == 0:
        return '0'
    elif r == 1:
        return ''       # invalid id
    else:
        return str(11 - r)

_VAT_ID_RULES['FI'] = (
    (re.compile('^(?P<base>\d{7})(?P<check>\d)$'), check_fi),
)


# - FR - France -

_FR_CC_MAP = '0123456789ABCDEFGHJKLMNPQRSTUVWXYZ'


def check_fr_old(base, add=None):
    d = (int(base) * 100 + 12) % 97
    return "%02i" % d


def check_fr_new(base, add=None):
    cc, num = base[:2], base[2:]
    d0 = _FR_CC_MAP.index(cc[0])
    d1 = _FR_CC_MAP.index(cc[1])
    if d0 <= 9:
        s = d0 * 24 + d1 - 10
    else:
        s = d0 * 34 + d1 - 100
    x = s % 11
    y = (int(num) + s // 11 + 1) % 11
    if x == y:
        return ''       # valid
    else:
        return 'f'      # check failed

_VAT_ID_RULES['FR'] = (
    # old system
    (re.compile('^(?P<check>\d{2})(?P<base>[1-9]{9})$'), check_fr_old),
    # new system
    (re.compile('^(?P<check>)(?P<base>([A-HJ-NP-Z]\d|\d[A-HJ-NP-Z])[1-9]{9})'),
     check_fr_new),
)


# - GB - United Kingdom -

def check_gb(base, add=None):
    s = sum(int(c) * w for c, w in zip(base[:-2], range(8, 1, -1)))
    cc = int(base[-2:])
    r1 = 97 - s % 97
    if r1 == cc:
        return ''       # valid
    if base[0] != '0':
        r2 = 97 - (s + 55) % 97
        if r2 == cc:
            return ''       # valid
    return 'f'          # check failed

_VAT_ID_RULES['GB'] = (
    # branch traders (12 digits) and standard (9 digits)
    (re.compile('^(?P<base>((00|[1-9]\d)\d{7}))(?P<check>)'
                '(\d\d[1-9]|\d[1-9]\d|[1-9]\d\d|$)$'), check_gb),
    # government departments
    (re.compile('^GD[0-4]\d{2}'), None),
    # health authorities
    (re.compile('^HA[5-9]\d{2}'), None),
)


# - GR - Greece -

def check_gr(base, add=None):
    s = sum(int(c) * 2 ** i for c, i in zip(base, range(len(base), 0, -1)))
    return str((s % 11) % 10)

_VAT_ID_RULES['GR'] = (
    (re.compile('^(?P<base>\d{7,8})(?P<check>\d)$'), check_gr),
)
# European Directive 2001/115 allowed 'EL' as synonym for 'GR'
_VAT_ID_RULES['EL'] = _VAT_ID_RULES['GR']


# - HR - Croatia -

def check_hr(base, add=None):
    p = 10
    r = 0
    for c in base:
        r = (int(c) + p) % 10
        if r == 0:
            p = 9
        else:
            p = (2 * r) % 11
    return str((11 - p) % 10)

_VAT_ID_RULES['HR'] = (
    (re.compile('^(?P<base>\d{10})(?P<check>\d)$'), check_hr),
)


# - HU - Hungary -

def check_hu(base, add=None):
    weights = (9, 7, 3, 1, 9, 7, 3)
    s = sum(int(c) * w for (c, w) in zip(base, weights))
    r = s % 10
    if r == 0:
        return '0'
    else:
        return str(10 - r)

_VAT_ID_RULES['HU'] = (
    (re.compile('^(?P<base>[1-9]\d{6})(?P<check>\d)$'), check_hu),
)


# - IE - Ireland -

_IE_CC_MAP = 'WABCDEFGHIJKLMNOPQRSTUV'


def check_ie_v1(base, add):
    v2_base = '0' + base + add
    return check_ie_v2(v2_base)


def check_ie_v2(base, add=None):
    s = sum(w * int(c) for w, c in zip(range(8, 1, -1), base))
    i = s % 23
    return _IE_CC_MAP[i]


def check_ie_v3(base, add):
    s = sum((w * int(c) for w, c in zip(range(8, 1, -1), base)),
            9 * (ord(add) - ord('@')))      # 'A' - 'I' -> 1 - 9
    i = s % 23
    return _IE_CC_MAP[i]

_VAT_ID_RULES['IE'] = (
    # version 1 (old style)
    (re.compile('^(?P<add>\d)[A-Z+*](?P<base>\d{5})(?P<check>[A-W])'),
     check_ie_v1),
    # version 2 (new style, 8 chars)
    (re.compile('^(?P<base>\d{7})(?P<check>[A-W])$'), check_ie_v2),
    # version 3 (new style, 9 chars)
    (re.compile('^(?P<base>\d{7})(?P<check>[A-W])(?P<add>[A-I])'),
     check_ie_v3),
)


# - IT - Italy -

def check_it(base, add=None):
    s1 = sum((int(c) for c in base[::2]))
    s2 = sum(chain(*(divmod(2 * int(c), 10) for c in base[1::2])))
    r = (s1 + s2) % 10
    if r == 0:
        return '0'
    else:
        return str(10 - r)

_VAT_ID_RULES['IT'] = (
    (re.compile('^(?P<base>\d{7}(0\d[1-9]|0[1-9]\d|100|12[01]|888|999))'
                '(?P<check>\d)$'), check_it),
)


# - LT - Lithuania -

def check_lt(base, add=None):
    weights = (1, 2, 3, 4, 5, 6, 7, 8, 9, 1, 2)
    s = sum(w * int(c) for w, c in zip(weights, base))
    r = s % 11
    if r == 10:
        weights = (3, 4, 5, 6, 7, 8, 9, 1, 2, 3, 4)
        s = sum(w * int(c) for w, c in zip(weights, base))
        r = (s % 11) % 10
    return str(r)

_VAT_ID_RULES['LT'] = (
    (re.compile('^(?P<base>\d{10}1)(?P<check>\d)$'), check_lt),
    (re.compile('^(?P<base>\d{7}1)(?P<check>\d)$'), check_lt),
)


# - LU - Luxembourg -

def check_lu(base, add=None):
    return '%02i' % (int(base) % 89)

_VAT_ID_RULES['LU'] = (
    (re.compile('^(?P<base>\d{6})(?P<check>\d{2})$'), check_lu),
)


# - LV - Latvia -

def check_lv_legal(base, add=None):
    weights = (9, 1, 4, 8, 3, 10, 2, 5, 7, 6)
    s = sum(w * int(c) for w, c in zip(weights, base))
    if base[0] == '9' and s % 11 == 4:
        s -= 45
    r = s % 11
    if r == 4:
        return '0'
    elif r > 4:
        return str(14 - r)
    else:
        return str(3 - r)


def check_lv_natural(base, add=None):
    d, m, y = int(base[:2]), int(base[2:4]), int(base[4:6])
    # 7th digit indicates century
    y += 1800 + int(base[6]) * 100
    try:
        date(y, m, d)
    except ValueError:
        return 'f'                  # check failed
    else:
        return ''                   # check ok

_VAT_ID_RULES['LV'] = (
    # legal persons
    (re.compile('^(?P<base>[4-9]\d{9})(?P<check>\d)$'), check_lv_legal),
    # natural persons
    (re.compile('^(?P<base>(0[1-9]|[12]\d|3[01])(0[1-9]|1[0-2])\d{2}[012]'
                '\d{4})(?P<check>)$'), check_lv_natural),
)


# - MT - Malta -

def check_mt(base, add=None):
    weights = (3, 4, 6, 7, 8, 9)
    s = sum(w * int(c) for w, c in zip(weights, base))
    return '%02i' % (37 - s % 37)

_VAT_ID_RULES['MT'] = (
    (re.compile('^(?P<base>[1-9]\d{5})(?P<check>\d{2})$'), check_mt),
)


# - NL - Netherlands -

def check_nl(base, add=None):
    weights = (9, 8, 7, 6, 5, 4, 3, 2)
    s = sum(w * int(c) for w, c in zip(weights, base))
    r = s % 11
    if r == 10:
        return 'f'          # invalid id
    else:
        return str(r)

_VAT_ID_RULES['NL'] = (
    (re.compile('^(?P<base>\d{8})(?P<check>\d)B(\d[1-9]|[1-9]\d)$'),
     check_nl),
)


# - PL - Poland -

def check_pl(base, add=None):
    weights = (6, 5, 7, 2, 3, 4, 5, 6, 7)
    s = sum(w * int(c) for w, c in zip(weights, base))
    r = s % 11
    if r == 10:
        return 'f'          # invalid id
    else:
        return str(r)

_VAT_ID_RULES['PL'] = (
    (re.compile('^(?P<base>\d{9})(?P<check>\d)$'), check_pl),
)


# - PT - Portugal -

def check_pt(base, add=None):
    weights = (9, 8, 7, 6, 5, 4, 3, 2)
    s = sum(w * int(c) for w, c in zip(weights, base))
    r = s % 11
    if r <= 1:
        return '0'
    else:
        return str(11 - r)

_VAT_ID_RULES['PT'] = (
    (re.compile('^(?P<base>[1-9]\d{7})(?P<check>\d)$'), check_pt),
)


# - RO - Romania -

def check_ro_legal(base, add=None):
    weights = (7, 5, 3, 2, 1, 7, 5, 3, 2)
    s = sum(w * int(c) for w, c in zip(weights, base))
    r = (10 * s) % 11
    return str(r % 10)


def check_ro_natural(base, add=None):
    y, m, d = int(base[1:3]), int(base[3:5]), int(base[5:7])
    # first digit indicates century:
    # 1-2 -> 1900, 3-4 -> 1800, 5-6 -> 2000, 7-9 unspecified
    c = base[0]
    if c in ['1', '2']:
        y += 1900
    elif c in ['3', '4']:
        y += 1800
    else:
        y += 2000
    try:
        date(y, m, d)
    except ValueError:
        return 'f'                  # check failed
    weights = (2, 7, 9, 1, 4, 6, 3, 5, 8, 2, 7, 9)
    s = sum(w * int(c) for w, c in zip(weights, base))
    r = s % 11
    return str(r % 10)

_VAT_ID_RULES['RO'] = (
    # legal persons
    (re.compile('^(?P<base>[1-9]\d{8})(?P<check>\d)$'), check_ro_legal),
    # natural persons
    (re.compile('^(?P<base>[1-9]\d{2}(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])'
                '(0[1-9]|[1-3]\d|4[0-7]|5[12])\d{3})(?P<check>\d)$'),
     check_ro_natural),
)


# - SE - Sweden -

def check_se(base, add=None):
    s1 = sum(chain(*(divmod(2 * int(c), 10) for c in base[::2])))
    s2 = sum((int(c) for c in base[1::2]))
    r = (s1 + s2) % 10
    if r == 0:
        return '0'
    else:
        return str(10 - r)

_VAT_ID_RULES['SE'] = (
    (re.compile('^(?P<base>\d{9})(?P<check>\d)(0[1-9]|[1-8]\d|9[1-4])'),
     check_se),
)


# - SI - Slovenia -

def check_si(base, add=None):
    weights = (8, 7, 6, 5, 4, 3, 2)
    s = sum(w * int(c) for w, c in zip(weights, base))
    r = s % 11
    if r == 0:
        return 'f'          # invalid id
    return str((11 - r) % 10)

_VAT_ID_RULES['SI'] = (
    (re.compile('^(?P<base>[1-9]\d{6})(?P<check>\d)$'), check_si),
)


# - SK - Slovakia -

def check_sk(base, add=None):
    n = int(base)
    if n % 11 == 0:
        return ''           # check ok
    else:
        return 'f'          # check failed

_VAT_ID_RULES['SK'] = (
    (re.compile('^(?P<base>[1-9]\d[2-47-9]\d{7})(?P<check>)$'), check_sk),
)


def get_first_match(rules, candidate):
    for pattern, check in rules:
        match = pattern.match(candidate)
        if match:
            return match, check
    return None, None


class EUVATId(Identifier):

    """European Union VAT Registration Number

    The VAT Registration Number is used to identify natural and legal persons
    located in the European Union for purposes of VAT handling.

    Each VAT Id begins with the two-letter ISO 3166-1 code(*) for the country
    where it is registered, followed by a registration code. The structure of
    the latter depends on the country.

    (*) As an exception, European Directive 2001/115 allowed 'EL' as synonym
    for 'GR'.
    """

    __slots__ = ()

    @property
    def country_code(self):
        """Return the VAT Id's country code."""
        return self._id[:2]

    @property
    def registration_code(self):
        """Return the VAT Id's registration code."""
        return self._id[2:]

    def elements(self):
        """Return the VAT Id's country code and registration code as a
        tuple."""
        return (self.country_code, self.registration_code)

    def __init__(self, vat_id):
        """Instances of EUVATId are created from a string containing the
        country code and the registration code.

        Depending on the country, different patterns and check algorithms are
        applied to validate an id.

        Args:
            vat_id (`Unicode string`): string representation of a VAT-Id

        Returns:
            instance of :class:`EUVATId`

        Raises:
            TypeError: given `vat_id` is not a `Unicode string`
            ValueError: given `vat_id` contains an unknown country code
            ValueError: given `vat_id` does not follow the format required for
                the given country code
            ValueError: given `vat_id` does not pass the checks for the given
                country code
        """
        if not isinstance(vat_id, str):
            raise TypeError("Argument must be instance of %s." % str)
        vat_id = vat_id.strip().upper()
        country_code = vat_id[:2]
        try:
            rules = _VAT_ID_RULES[country_code]
        except KeyError:
            msg = "Unknown country code: '%s'" % country_code
        else:
            reg_code = vat_id[2:]
            match, check = get_first_match(rules, reg_code)
            if match and match.end() == len(reg_code):
                if (check is None or
                        check(match.group('base'),
                              match.groupdict().get('add')) ==
                        match.group('check')):
                    self._id = vat_id
                    return
                else:
                    msg = "'%s' does not pass the checks for '%s'." \
                          % (reg_code, country_code)
            else:
                msg = "'%s' does not match the pattern%s for '%s': '%s'." \
                      % (reg_code, '' if len(rules) == 1 else 's',
                         country_code, ' | '.join((p.pattern
                                                   for p, _ in rules)))
        raise ValueError(msg)

    def __str__(self):
        """str(self)"""
        return self._id