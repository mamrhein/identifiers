# -*- coding: utf-8 -*-
# $Source$
# $Revision$

"""IBAN registry generated from file 'swift_standards_ibanregistry.txt'"""

from __future__ import unicode_literals
from collections import namedtuple
import re

IBANSpec = namedtuple(
    'IBANSpec',
    ('bban_length', 'bban_structure', 'bban_split_pos', 'examples'))

IBAN_REGISTRY = \
{'AD': IBANSpec(bban_length=20, bban_structure=re.compile('[0-9]{8}[A-Za-z0-9]{12}'), bban_split_pos=8, examples=('AD1200012030200359100100',)),
 'AE': IBANSpec(bban_length=19, bban_structure=re.compile('[0-9]{19}'), bban_split_pos=3, examples=('AE070331234567890123456',)),
 'AL': IBANSpec(bban_length=24, bban_structure=re.compile('[0-9]{8}[A-Za-z0-9]{16}'), bban_split_pos=8, examples=('AL47212110090000000235698741',)),
 'AT': IBANSpec(bban_length=16, bban_structure=re.compile('[0-9]{16}'), bban_split_pos=5, examples=('AT611904300234573201',)),
 'AZ': IBANSpec(bban_length=24, bban_structure=re.compile('[A-Z]{4}[A-Za-z0-9]{20}'), bban_split_pos=4, examples=('AZ21NABZ00000000137010001944',)),
 'BA': IBANSpec(bban_length=16, bban_structure=re.compile('[0-9]{16}'), bban_split_pos=6, examples=('BA391290079401028494',)),
 'BE': IBANSpec(bban_length=12, bban_structure=re.compile('[0-9]{12}'), bban_split_pos=3, examples=('BE68539007547034',)),
 'BG': IBANSpec(bban_length=18, bban_structure=re.compile('[A-Z]{4}[0-9]{6}[A-Za-z0-9]{8}'), bban_split_pos=8, examples=('BG80BNBG96611020345678',)),
 'BH': IBANSpec(bban_length=18, bban_structure=re.compile('[A-Z]{4}[A-Za-z0-9]{14}'), bban_split_pos=4, examples=('BH67BMAG00001299123456',)),
 'BR': IBANSpec(bban_length=25, bban_structure=re.compile('[0-9]{23}[A-Z]{1}[A-Za-z0-9]{1}'), bban_split_pos=13, examples=('BR1800360305000010009795493C1',)),
 'BY': IBANSpec(bban_length=24, bban_structure=re.compile('[A-Za-z0-9]{4}[0-9]{4}[A-Za-z0-9]{16}'), bban_split_pos=4, examples=('BY13NBRB3600900000002Z00AB00',)),
 'CH': IBANSpec(bban_length=17, bban_structure=re.compile('[0-9]{5}[A-Za-z0-9]{12}'), bban_split_pos=5, examples=('CH9300762011623852957',)),
 'CR': IBANSpec(bban_length=18, bban_structure=re.compile('[0-9]{18}'), bban_split_pos=4, examples=('CR05015202001026284066',)),
 'CY': IBANSpec(bban_length=24, bban_structure=re.compile('[0-9]{8}[A-Za-z0-9]{16}'), bban_split_pos=8, examples=('CY17002001280000001200527600',)),
 'CZ': IBANSpec(bban_length=20, bban_structure=re.compile('[0-9]{20}'), bban_split_pos=4, examples=('CZ6508000000192000145399',)),
 'DE': IBANSpec(bban_length=18, bban_structure=re.compile('[0-9]{18}'), bban_split_pos=8, examples=('DE89370400440532013000',)),
 'DK': IBANSpec(bban_length=14, bban_structure=re.compile('[0-9]{14}'), bban_split_pos=4, examples=('DK5000400440116243',)),
 'DO': IBANSpec(bban_length=24, bban_structure=re.compile('[A-Za-z0-9]{4}[0-9]{20}'), bban_split_pos=4, examples=('DO28BAGR00000001212453611324',)),
 'EE': IBANSpec(bban_length=16, bban_structure=re.compile('[0-9]{16}'), bban_split_pos=2, examples=('EE382200221020145685',)),
 'ES': IBANSpec(bban_length=20, bban_structure=re.compile('[0-9]{20}'), bban_split_pos=8, examples=('ES9121000418450200051332',)),
 'FI': IBANSpec(bban_length=14, bban_structure=re.compile('[0-9]{14}'), bban_split_pos=3, examples=('FI2112345600000785',)),
 'FO': IBANSpec(bban_length=14, bban_structure=re.compile('[0-9]{14}'), bban_split_pos=4, examples=('FO6264600001631634',)),
 'FR': IBANSpec(bban_length=23, bban_structure=re.compile('[0-9]{10}[A-Za-z0-9]{11}[0-9]{2}'), bban_split_pos=5, examples=('FR1420041010050500013M02606',)),
 'GB': IBANSpec(bban_length=18, bban_structure=re.compile('[A-Z]{4}[0-9]{14}'), bban_split_pos=10, examples=('GB29NWBK60161331926819',)),
 'GE': IBANSpec(bban_length=18, bban_structure=re.compile('[A-Z]{2}[0-9]{16}'), bban_split_pos=2, examples=('GE29NB0000000101904917',)),
 'GI': IBANSpec(bban_length=19, bban_structure=re.compile('[A-Z]{4}[A-Za-z0-9]{15}'), bban_split_pos=4, examples=('GI75NWBK000000007099453',)),
 'GL': IBANSpec(bban_length=14, bban_structure=re.compile('[0-9]{14}'), bban_split_pos=4, examples=('GL8964710001000206',)),
 'GR': IBANSpec(bban_length=23, bban_structure=re.compile('[0-9]{7}[A-Za-z0-9]{16}'), bban_split_pos=7, examples=('GR1601101250000000012300695',)),
 'GT': IBANSpec(bban_length=24, bban_structure=re.compile('[A-Za-z0-9]{24}'), bban_split_pos=4, examples=('GT82TRAJ01020000001210029690',)),
 'HR': IBANSpec(bban_length=17, bban_structure=re.compile('[0-9]{17}'), bban_split_pos=7, examples=('HR1210010051863000160',)),
 'HU': IBANSpec(bban_length=24, bban_structure=re.compile('[0-9]{24}'), bban_split_pos=7, examples=('HU42117730161111101800000000',)),
 'IE': IBANSpec(bban_length=18, bban_structure=re.compile('[A-Z]{4}[0-9]{14}'), bban_split_pos=10, examples=('IE29AIBK93115212345678',)),
 'IL': IBANSpec(bban_length=19, bban_structure=re.compile('[0-9]{19}'), bban_split_pos=6, examples=('IL620108000000099999999',)),
 'IQ': IBANSpec(bban_length=19, bban_structure=re.compile('[A-Z]{4}[0-9]{15}'), bban_split_pos=7, examples=('IQ98NBIQ850123456789012',)),
 'IS': IBANSpec(bban_length=22, bban_structure=re.compile('[0-9]{22}'), bban_split_pos=4, examples=('IS140159260076545510730339',)),
 'IT': IBANSpec(bban_length=23, bban_structure=re.compile('[A-Z]{1}[0-9]{10}[A-Za-z0-9]{12}'), bban_split_pos=11, examples=('IT60X0542811101000000123456',)),
 'JO': IBANSpec(bban_length=26, bban_structure=re.compile('[A-Z]{4}[0-9]{4}[A-Za-z0-9]{18}'), bban_split_pos=8, examples=('JO94CBJO0010000000000131000302',)),
 'KW': IBANSpec(bban_length=26, bban_structure=re.compile('[A-Z]{4}[A-Za-z0-9]{22}'), bban_split_pos=4, examples=('KW81CBKU0000000000001234560101',)),
 'KZ': IBANSpec(bban_length=16, bban_structure=re.compile('[0-9]{3}[A-Za-z0-9]{13}'), bban_split_pos=3, examples=('KZ86125KZT5004100100',)),
 'LB': IBANSpec(bban_length=24, bban_structure=re.compile('[0-9]{4}[A-Za-z0-9]{20}'), bban_split_pos=4, examples=('LB62099900000001001901229114',)),
 'LC': IBANSpec(bban_length=28, bban_structure=re.compile('[A-Z]{4}[A-Za-z0-9]{24}'), bban_split_pos=4, examples=('LC55HEMM000100010012001200023015',)),
 'LI': IBANSpec(bban_length=17, bban_structure=re.compile('[0-9]{5}[A-Za-z0-9]{12}'), bban_split_pos=5, examples=('LI21088100002324013AA',)),
 'LT': IBANSpec(bban_length=16, bban_structure=re.compile('[0-9]{16}'), bban_split_pos=5, examples=('LT121000011101001000',)),
 'LU': IBANSpec(bban_length=16, bban_structure=re.compile('[0-9]{3}[A-Za-z0-9]{13}'), bban_split_pos=3, examples=('LU280019400644750000',)),
 'LV': IBANSpec(bban_length=17, bban_structure=re.compile('[A-Z]{4}[A-Za-z0-9]{13}'), bban_split_pos=4, examples=('LV80BANK0000435195001',)),
 'MC': IBANSpec(bban_length=23, bban_structure=re.compile('[0-9]{10}[A-Za-z0-9]{11}[0-9]{2}'), bban_split_pos=10, examples=('MC5811222000010123456789030',)),
 'MD': IBANSpec(bban_length=20, bban_structure=re.compile('[A-Za-z0-9]{20}'), bban_split_pos=2, examples=('MD24AG000225100013104168',)),
 'ME': IBANSpec(bban_length=18, bban_structure=re.compile('[0-9]{18}'), bban_split_pos=3, examples=('ME25505000012345678951',)),
 'MK': IBANSpec(bban_length=15, bban_structure=re.compile('[0-9]{3}[A-Za-z0-9]{10}[0-9]{2}'), bban_split_pos=3, examples=('MK07250120000058984',)),
 'MR': IBANSpec(bban_length=23, bban_structure=re.compile('[0-9]{23}'), bban_split_pos=10, examples=('MR1300020001010000123456753',)),
 'MT': IBANSpec(bban_length=27, bban_structure=re.compile('[A-Z]{4}[0-9]{5}[A-Za-z0-9]{18}'), bban_split_pos=9, examples=('MT84MALT011000012345MTLCAST001S',)),
 'MU': IBANSpec(bban_length=26, bban_structure=re.compile('[A-Z]{4}[0-9]{19}[A-Z]{3}'), bban_split_pos=8, examples=('MU17BOMM0101101030300200000MUR',)),
 'NL': IBANSpec(bban_length=14, bban_structure=re.compile('[A-Z]{4}[0-9]{10}'), bban_split_pos=4, examples=('NL91ABNA0417164300',)),
 'NO': IBANSpec(bban_length=11, bban_structure=re.compile('[0-9]{11}'), bban_split_pos=4, examples=('NO9386011117947',)),
 'PK': IBANSpec(bban_length=20, bban_structure=re.compile('[A-Z]{4}[A-Za-z0-9]{16}'), bban_split_pos=4, examples=('PK36SCBL0000001123456702',)),
 'PL': IBANSpec(bban_length=24, bban_structure=re.compile('[0-9]{24}'), bban_split_pos=8, examples=('PL61109010140000071219812874',)),
 'PS': IBANSpec(bban_length=25, bban_structure=re.compile('[A-Z]{4}[A-Za-z0-9]{21}'), bban_split_pos=4, examples=('PS92PALS000000000400123456702',)),
 'PT': IBANSpec(bban_length=21, bban_structure=re.compile('[0-9]{21}'), bban_split_pos=4, examples=('PT50000201231234567890154',)),
 'QA': IBANSpec(bban_length=25, bban_structure=re.compile('[A-Z]{4}[A-Za-z0-9]{21}'), bban_split_pos=4, examples=('QA58DOHB00001234567890ABCDEFG',)),
 'RO': IBANSpec(bban_length=20, bban_structure=re.compile('[A-Z]{4}[A-Za-z0-9]{16}'), bban_split_pos=4, examples=('RO49AAAA1B31007593840000',)),
 'RS': IBANSpec(bban_length=18, bban_structure=re.compile('[0-9]{18}'), bban_split_pos=3, examples=('RS35260005601001611379',)),
 'SA': IBANSpec(bban_length=20, bban_structure=re.compile('[0-9]{2}[A-Za-z0-9]{18}'), bban_split_pos=2, examples=('SA0380000000608010167519',)),
 'SC': IBANSpec(bban_length=27, bban_structure=re.compile('[A-Z]{4}[0-9]{20}[A-Z]{3}'), bban_split_pos=8, examples=('SC18SSCB11010000000000001497USD',)),
 'SE': IBANSpec(bban_length=20, bban_structure=re.compile('[0-9]{20}'), bban_split_pos=3, examples=('SE4550000000058398257466',)),
 'SI': IBANSpec(bban_length=15, bban_structure=re.compile('[0-9]{15}'), bban_split_pos=5, examples=('SI56263300012039086',)),
 'SK': IBANSpec(bban_length=20, bban_structure=re.compile('[0-9]{20}'), bban_split_pos=4, examples=('SK3112000000198742637541',)),
 'SM': IBANSpec(bban_length=23, bban_structure=re.compile('[A-Z]{1}[0-9]{10}[A-Za-z0-9]{12}'), bban_split_pos=11, examples=('SM86U0322509800000000270100',)),
 'ST': IBANSpec(bban_length=21, bban_structure=re.compile('[0-9]{21}'), bban_split_pos=8, examples=('ST32000200010192194210112',)),
 'SV': IBANSpec(bban_length=24, bban_structure=re.compile('[A-Z]{4}[0-9]{20}'), bban_split_pos=4, examples=('SV62CENR00000000000000700025',)),
 'TL': IBANSpec(bban_length=19, bban_structure=re.compile('[0-9]{19}'), bban_split_pos=3, examples=('TL380080012345678910157',)),
 'TN': IBANSpec(bban_length=20, bban_structure=re.compile('[0-9]{20}'), bban_split_pos=5, examples=('TN5910006035183598478831',)),
 'TR': IBANSpec(bban_length=22, bban_structure=re.compile('[0-9]{6}[A-Za-z0-9]{16}'), bban_split_pos=5, examples=('TR330006100519786457841326',)),
 'UA': IBANSpec(bban_length=25, bban_structure=re.compile('[0-9]{6}[A-Za-z0-9]{19}'), bban_split_pos=6, examples=('UA213223130000026007233566001',)),
 'VG': IBANSpec(bban_length=20, bban_structure=re.compile('[A-Z]{4}[0-9]{16}'), bban_split_pos=4, examples=('VG96VPVG0000012345678901',)),
 'XK': IBANSpec(bban_length=16, bban_structure=re.compile('[0-9]{16}'), bban_split_pos=4, examples=('XK051212012345678906',))}


# query function
def get_iban_spec(country_code):
    """Retrieve IBAN structure spec from registry."""
    return IBAN_REGISTRY[country_code]
