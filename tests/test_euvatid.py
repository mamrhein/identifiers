# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Name:        test_euvatid
# Purpose:     Test driver for module euvatid
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

from __future__ import absolute_import, unicode_literals
import unittest
from identifiers.euvatid import EUVATId


__metaclass__ = type


_VALID_IDS = [
    # 'AT': '^U(?P<base>\d{7})(?P<check>\d)$'
    'ATU13585627',
    'ATU10223006',
    # 'BE': '^(?P<base>0[1-9]\d{6})(?P<check>\d{2})$'
    'BE0776091951',
    'BE0136695962',
    'BE0111113203',
    # 'BG': '^(?P<base>\d{8})(?P<check>\d)$'
    #       '^(?P<base>\d{2}([024][1-9]|[135][012])(0[1-9]|[12]\d|3[01])\d{3})
    #           (?P<check>\d)$'
    #       '^(?P<base>\d{9})(?P<check>\d)$'
    'BG7523169263',
    'BG7501020018',
    'BG0542011038',
    'BG123456786',
    # 'CY': '^(?P<base>[013-59]\d{7})(?P<check>[A-Z])$'
    'CY12345678F',
    'CY33333333O',
    'CY93333333C',
    # 'CZ': '^(?P<base>\d{2}([05]\d|[16][0-2])(0[1-9]|[12]\d|3[01])\d{4})
    #           (?P<check>)$'
    #       '^(?P<base>([0-4]\d|5[0-3])([05]\d|[16][0-2])(0[1-9]|[12]\d|3[01])
    #           \d{3})(?P<check>)$'
    #       '^(?P<base>6\d{7})(?P<check>\d)$'
    #       '^(?P<base>[0-8]\d{6})(?P<check>\d)$'
    'CZ5502080001',
    'CZ0052291536',
    'CZ6852294449',
    'CZ8160080610',
    'CZ110101111',
    'CZ531124000',
    'CZ006031038',
    'CZ633333334',
    'CZ12345679',
    # 'DE': '^(?P<base>\d{8})(?P<check>\d)$'
    'DE111111125',
    'DE136695976',
    # 'DK': '^(?P<base>[1-9]\d{7})(?P<check>)$'
    'DK13585628',
    'DK88146328',
    # 'EE': '^(?P<base>\d{8})(?P<check>\d)$'
    'EE123456780',
    'EE444444442',
    # 'ES': '^(?P<base>[A-H,JVU]\d{7})(?P<check>\d)$'
    #       '^(?P<base>[NP-SW]\d{7})(?P<check>[A-J])$'
    #       '^(?P<base>\d{8})(?P<check>[A-Z])$'
    #       '^(?P<base>[KLMXYZ]\d{7})(?P<check>[A-Z])$'
    'ESA12345674',
    'ESP1234567D',
    'ES12345678Z',
    'ESK1234567L',
    # 'FI': '^(?P<base>\d{7})(?P<check>\d)$'
    'FI12345671',
    'FI09853608',
    # 'FR': '^(?P<check>\d{2})(?P<base>[1-9]{9})$'
    #       '^(?P<check>)(?P<base>([A-HJ-NP-Z]\d|\d[A-HJ-NP-Z])[1-9]{9})'
    'FR32123456789',
    'FR2H123456789',
    # 'GB': '^(?P<base>((00|[1-9]\d)\d{7}))(?P<check>)
    #           (\d\d[1-9]|\d[1-9]\d|[1-9]\d\d|$)$'
    #       '^GD[0-4]\d{2}'
    #       '^HA[5-9]\d{2}'
    'GB434031494',
    'GB434031439',
    'GB123456782',
    'GB123456727',
    'GB123456727872',
    'GB001234547',
    'GB001234547238',
    'GBGD123',
    'GBHA629',
    # 'GR': '^(?P<base>\d{7,8})(?P<check>\d)$'
    'GR12345670',
    'GR123456783',
    # 'HR': '^(?P<base>\d{10})(?P<check>\d)$'
    'HR12345678903',
    'HR11111111119',
    'HR00000777773',
    # 'HU': '^(?P<base>[1-9]\d{6})(?P<check>\d)$'
    'HU21376414',
    'HU10597190',
    'HU12345676',
    # 'IE': '^(?P<add>\d)[A-Z+*](?P<base>\d{5})(?P<check>[A-W])'
    #       '^(?P<base>\d{7})(?P<check>[A-W])$'
    #       '^(?P<base>\d{7})(?P<check>[A-W])(?P<add>[A-I])'
    'IE8Z49289F',
    'IE3628739L',
    'IE3628739UA',
    'IE7A12345J',
    'IE1234567T',
    # 'IT': '^(?P<base>\d{7}(0\d[1-9]|0[1-9]\d|100|12[01]|888|999))
    #           (?P<check>\d)$'
    'IT00000010215',
    'IT12345670017',
    'IT12345678887',
    # 'LT': '^(?P<base>\d{10}1)(?P<check>\d)$'
    #       '^(?P<base>\d{7}1)(?P<check>\d)$'
    'LT213179412',
    'LT123456715',
    'LT290061371314',
    'LT123456789011',
    # 'LU': '^(?P<base>\d{6})(?P<check>\d{2})$'
    'LU77777706',
    'LU10000356',
    'LU12345613',
    # 'LV': '^(?P<base>[4-9]\d{9})(?P<check>\d)$'
    #       '^(?P<base>(0[1-9]|[12]\d|3[01])(0[1-9]|1[0-2])\d{2}[012]\d{4})
    #           (?P<check>)$'
    'LV41234567891',
    'LV15066312345',
    'LV29020412345',
    # 'MT': '^(?P<base>[1-9]\d{5})(?P<check>\d{2})$'
    'MT12345634',
    'MT10000125',
    # 'NL': '^(?P<base>\d{8})(?P<check>\d)B(\d[1-9]|[1-9]\d)$'
    'NL123456782B70',
    'NL010000446B01',
    'NL000000012B34',
    # 'PL': '^(?P<base>\d{9})(?P<check>\d)$'
    'PL0123456789',
    'PL5260001246',
    # 'PT': '^(?P<base>[1-9]\d{7})(?P<check>\d)$'
    'PT123456789',
    'PT502757191',
    # 'RO': '^(?P<base>[1-9]\d{8})(?P<check>\d)$'
    #       '^(?P<base>[1-9]\d{2}(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])
    #           (0[1-9]|[1-3]\d|4[0-7]|5[12])\d{3})(?P<check>\d)$'
    'RO1234567897',
    'RO1630615123457',
    # 'SE': '^(?P<base>\d{9})(?P<check>\d)(0[1-9]|[1-8]\d|9[1-4])'
    'SE123456789701',
    'SE556188840494',
    # 'SI': '^(?P<base>[1-9]\d{6})(?P<check>\d)$'
    'SI12345679',
    'SI15012557',
    # 'SK': '^(?P<base>[1-9]\d[2-47-9]\d{7})(?P<check>)$'
    'SK1234567895',
    'SK4030000007',
]

_INVALID_IDS = [
    # 'AT': '^U(?P<base>\d{7})(?P<check>\d)$'
    # invalid format
    'ATU1234ABC',
    'AT012345678',
    # invalid check digit
    'ATU13585626',
    'ATU10223007',
    'ATU12345678',
    # 'BE': '^(?P<base>0[1-9]\d{6})(?P<check>\d{2})$'
    # invalid format
    'BE3123456789',
    'BE012345678X',
    'BE0012345678',
    # invalid check digit
    'BE0776091950',
    'BE0136695972',
    # 'BG': '^(?P<base>\d{8})(?P<check>\d)$'
    #       '^(?P<base>\d{2}([024][1-9]|[135][012])(0[1-9]|[12]\d|3[01])\d{3})
    #           (?P<check>\d)$'
    #       '^(?P<base>\d{9})(?P<check>\d)$'
    # invalid format
    'BGK123456789',
    'BG12345678',
    'BG7542011030',
    'BG7502290002',
    'BG12345678901',
    # invalid check digit
    'BG7523169266',
    'BG7501020017',
    'BG0542011030',
    'BG123456789',
    # 'CY': '^(?P<base>[013-59]\d{7})(?P<check>[A-Z])$'
    # invalid format
    'CY0X123456B',
    'CY23456789N',
    'CY67890123K',
    'CY123456789',
    # invalid check digit
    'CY12345678A',
    'CY33333333J',
    'CY93333333B',
    # 'CZ': '^(?P<base>\d{2}([05]\d|[16][0-2])(0[1-9]|[12]\d|3[01])\d{4})
    #           (?P<check>)$'
    #       '^(?P<base>([0-4]\d|5[0-3])([05]\d|[16][0-2])(0[1-9]|[12]\d|3[01])
    #           \d{3})(?P<check>)$'
    #       '^(?P<base>6\d{7})(?P<check>\d)$'
    #       '^(?P<base>[0-8]\d{6})(?P<check>\d)$'
    # invalid format
    'CZ1234567890',
    'CZ701120001',
    'CZ12345678X',
    'CZ6123456',
    'CZ9999999',
    # invalid check
    'CZ5502080000',
    'CZ7952290291',
    'CZ005229153',
    'CZ633333333',
    'CZ12345678',
    # 'DE': '^(?P<base>\d{8})(?P<check>\d)$'
    # invalid format
    'DE1234567890',
    'DE12345G678',
    # invalid check digit
    'DE111111120',
    'DE136695973',
    # 'DK': '^(?P<base>[1-9]\d{7})(?P<check>)$'
    # invalid format
    'DK1234567',
    'DKX1234567',
    'DK01234567',
    # invalid check
    'DK13585627',
    'DK88146324',
    # 'EE': '^(?P<base>\d{8})(?P<check>\d)$'
    # invalid format
    'EE0123456789',
    'EEO12345678'
    # invalid check digit
    'EE123456789',
    'EE444444444',
    # 'ES': '^(?P<base>[A-H,JVU]\d{7})(?P<check>\d)$'
    #       '^(?P<base>[NP-SW]\d{7})(?P<check>[A-J])$'
    #       '^(?P<base>\d{8})(?P<check>[A-Z])$'
    #       '^(?P<base>[KLMXYZ]\d{7})(?P<check>[A-Z])$'
    # invalid format
    'ESXA1234567',
    'ES01234567B8',
    'ES012345678',
    # invalid check digit
    'ESA12345678',
    'ESP1234567B',
    'ES12345678Y',
    'ESK1234567E',
    # 'FI': '^(?P<base>\d{7})(?P<check>\d)$'
    # invalid format
    'FI1234567',
    'FI123456789',
    'FI1234R678',
    # invalid check digit
    'FI12345678',
    'FI09853600',
    # 'FR': '^(?P<check>\d{2})(?P<base>[1-9]{9})$'
    #       '^(?P<check>)(?P<base>([A-HJ-NP-Z]\d|\d[A-HJ-NP-Z])[1-9]{9})'
    # invalid format
    'FR123456789AB',
    'FR12345678901',
    'FR0I123456789',
    'FRO4123456789',
    'FRXX123456789',
    # invalid check digit
    'FR22123456789',
    'FR0H123456789',
    'FR2J123456789',
    # 'GB': '^(?P<base>((00|[1-9]\d)\d{7}))(?P<check>)
    #           (\d\d[1-9]|\d[1-9]\d|[1-9]\d\d|$)$'
    #       '^GD[0-4]\d{2}'
    #       '^HA[5-9]\d{2}'
    # invalid format
    'GB1234567890',
    'GB012345678',
    'GB123456727000',
    'GBGD1234',
    'GBGD777',
    'GBHA12',
    'GBHA123',
    'GBAB123',
    # invalid check digits
    'GB434031499',
    'GB434031430',
    'GB123456781',
    'GB123456728',
    'GB123456728872',
    'GB001234589',
    'GB001234546',
    'GB001234548238',
    # 'GR': '^(?P<base>\d{7,8})(?P<check>\d)$'
    # invalid format
    'GR12345678G',
    'GR1234567',
    # invalid check digits
    'GR12345678',
    'GR123456789',
    # 'HR': '^(?P<base>\d{10})(?P<check>\d)$'
    # invalid format
    'HR1234567890',
    'HR123456789012',
    'HR1234567890X',
    # invalid check digits
    'HR12345678901',
    'HR11111111111',
    'HR00000777777',
    # 'HU': '^(?P<base>[1-9]\d{6})(?P<check>\d)$'
    # invalid format
    'HU1234567',
    'HU123456789',
    'HU1234567Z',
    'HU01234567'
    # invalid check digits
    'HU21376411',
    'HU10597199',
    'HU12345678',
    # 'IE': '^(?P<add>\d)[A-Z+*](?P<base>\d{5})(?P<check>[A-W])'
    #       '^(?P<base>\d{7})(?P<check>[A-W])$'
    #       '^(?P<base>\d{7})(?P<check>[A-W])(?P<add>[A-I])'
    # invalid format
    'IE12345678',
    'IE1234567XA',
    'IE1234567WM',
    'IE123456',
    'IEA123456C',
    # invalid check character
    'IE8Z49289V',
    'IE3628739M',
    'IE3628739VA',
    'IE7A12345I',
    'IE1234567U',
    # 'IT': '^(?P<base>\d{7}(0\d[1-9]|0[1-9]\d|100|12[01]|888|999))
    #           (?P<check>\d)$'
    # invalid format
    'IT12345678I07',
    'IT12345678804',
    'IT12345670009',
    'IT12345671239',
    # invalid check digit
    'IT00000010210',
    'IT12345670016',
    'IT12345678888',
    # 'LT': '^(?P<base>\d{10}1)(?P<check>\d)$'
    #       '^(?P<base>\d{7}1)(?P<check>\d)$'
    # invalid format
    'LT12345678',
    'LT1234567890',
    'LT123456729',
    'LT123456775',
    'LT290061371394',
    # invalid check digit
    'LT213179411',
    'LT123456712',
    'LT290061371318',
    'LT123456789012',
    # 'LU': '^(?P<base>\d{6})(?P<check>\d{2})$'
    # invalid format
    'LU777777065',
    'LU1111111111111111111111111',
    # invalid check digit
    'LU77777707',
    'LU10000366',
    'LU12345678',
    # 'LV': '^(?P<base>[4-9]\d{9})(?P<check>\d)$'
    #       '^(?P<base>(0[1-9]|[12]\d|3[01])(0[1-9]|1[0-2])\d{2}[012]\d{4})
    #           (?P<check>)$'
    # invalid format
    'LV15166312345',
    'LV20020072345',
    'LVA1234567890',
    # invalid check
    'LV41234567890',
    'LV29020012345',
    'LV31040023456',
    # 'MT': '^(?P<base>[1-9]\d{5})(?P<check>\d{2})$'
    # invalid format
    'MT123456-8',
    'MT01234567',
    # invalid check digits
    'MT12345633',
    'MT10000123',
    # 'NL': '^(?P<base>\d{8})(?P<check>\d)B(\d[1-9]|[1-9]\d)$'
    # invalid format
    'NL123456782B00',
    'NL123456782B-0',
    'NL123456782123',
    # invalid check digit
    'NL123456789B70',
    'NL010000444B01',
    'NL000000010B34',
    'NL200000100B10',
    # 'PL': '^(?P<base>\d{9})(?P<check>\d)$'
    # invalid format
    'PL123456789',
    'PLA123456789',
    # invalid check digit
    'PL1234567890',
    'PL0123456780',
    'PL5260001244',
    'PL0200000000',
    # 'PT': '^(?P<base>[1-9]\d{7})(?P<check>\d)$'
    # invalid format
    'PT12345678',
    'PT012345679',
    'PT1234567890',
    # invalid check digit
    'PT123456788',
    'PT502757190',
    # 'RO': '^(?P<base>[1-9]\d{8})(?P<check>\d)$'
    #       '^(?P<base>[1-9]\d{2}(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])
    #           (0[1-9]|[1-3]\d|4[0-7]|5[12])\d{3})(?P<check>\d)$'
    # invalid format
    'RO0123456789',
    'RO0123456789012',
    'RO5121018001230',
    'RO8121018641231',
    'RO1630229123459',
    # invalid check digit
    'RO1234567890',
    'RO1630615123456',
    # 'SE': '^(?P<base>\d{9})(?P<check>\d)(0[1-9]|[1-8]\d|9[1-4])'
    # invalid format
    'SE1234567897',
    'SE123456789700',
    'SE123456789797',
    # invalid check digit
    'SE123456789001',
    'SE556188840194',
    # 'SI': '^(?P<base>[1-9]\d{6})(?P<check>\d)$'
    # invalid format
    'SI1234567',
    'SI01234567',
    'SI123456789',
    # invalid check digit
    'SI12345678',
    'SI15012555',
    'SI76543110',
    # 'SK': '^(?P<base>[1-9]\d[2-47-9]\d{7})(?P<check>)$'
    'SK123456789',
    'SK1000000001',
    'SK0123456784',
    'SK12345678901',
    # invalid check digit
    'SK1234567890',
    'SK4030000000',
    # unknown country code
    'XX1234567',
]


class EUVATIdTest(unittest.TestCase):

    def test_constructor(self):
        # wrong type of argument
        self.assertRaises(TypeError, EUVATId, 14)
        # white space stripped and letters converted to upper case
        s = '  pt123456789   \n'
        vat_id = EUVATId(s)
        self.assertEqual(vat_id._id, s.strip().upper())
        # ensure slot-only instance
        vat_id = EUVATId(_VALID_IDS[0])
        self.assertRaises(AttributeError, getattr, vat_id, '__dict__')

    def test_valid_ids(self):
        for s in _VALID_IDS:
            vat_id = EUVATId(s)
            self.assertEqual(vat_id._id, s)

    def test_invalid_ids(self):
        for s in _INVALID_IDS:
            # print(s)
            self.assertRaises(ValueError, EUVATId, s)

    def test_str(self):
        s = _VALID_IDS[0]
        self.assertEqual(str(EUVATId(s)), s)


if __name__ == '__main__':
    unittest.main()
