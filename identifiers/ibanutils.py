# -*- coding: utf-8 -*-
##----------------------------------------------------------------------------
## Name:        ibanutils
## Purpose:     Utility functions for checking IBANs
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


"""Utility functions for checking IBANs"""


from __future__ import absolute_import, unicode_literals
from csv import DictReader
from collections import namedtuple
from itertools import groupby
import os.path
import re
import sys


__metaclass__ = type


# downloaded from 'https://www.swift.com/node/11971'
file_name = os.path.join(os.path.dirname(__file__), "Swift IBAN registry.txt")

if sys.version_info.major < 3:

    def reader(file_name, encoding='cp1252'):
        with open(file_name, mode='rb') as csv_file:
            for row in DictReader(csv_file, delimiter=b'\t', quotechar=b'"'):
                yield {unicode(key.strip(), encoding): unicode(val, encoding)
                       for key, val in row.iteritems()}

else:

    def reader(file_name, encoding='cp1252'):
        with open(file_name, mode='r', encoding=encoding) as csv_file:
            for row in DictReader(csv_file, delimiter='\t', quotechar='"'):
                yield {key.strip(): val.strip() for key, val in row.items()}


# regexp to find format specs
FORMAT_REGEXP = '(\d+)([!]*)([nace])'
_format = re.compile(FORMAT_REGEXP)


def group_format_spec(spec):
    for _type, elems in groupby(_format.findall(spec),
                                key=lambda expr: expr[2]):
        min_length = max_length = 0
        for n_chars, fixed, _ in elems:
            length = int(n_chars)
            if fixed:
                min_length += length
            max_length += length
        yield _type, min_length, max_length


# mapping (format code -> regexp part)
CHAR_TYPE_MAP = dict(zip('nace', ('[0-9]', '[A-Z]', '[A-Za-z0-9]', '[ ]')))


def format_spec_to_regexp(spec):
    expr = ''.join((CHAR_TYPE_MAP[_type] + '{' + str(min_length) +
                    '}' if min_length == max_length else ',%s}' % max_length
                   for _type, min_length, max_length
                   in group_format_spec(spec)))
    return re.compile(expr)


def extract_length(spec):
    spec = spec.split(';')[0]
    try:
        return int(spec)
    except ValueError:
        pass
    length = sum(int(n_chars) for n_chars, _, _ in _format.findall(spec))
    if length > 0:
        return length
    raise ValueError


# regexp to find position specs
POS_REGEXP = '(\d{1,2})([-]*)(\d{0,2})'
_pos = re.compile(POS_REGEXP)


def extract_pos(spec):
    pos_list = _pos.findall(spec)
    if pos_list:
        min_pos = min(int(start) for (start, _, _) in pos_list)
        max_pos = max(int(end if end else start)
                      for (start, _, end) in pos_list)
        if min_pos <= max_pos:
            return min_pos, max_pos
    raise ValueError


# regexp to extract examples
EXMPL_REGEXP = '([A-Z]{2}\w*)'
_exmpl = re.compile(EXMPL_REGEXP)


def extract_examples(spec):
    return _exmpl.findall(spec)


_IBAN_registry = {}
IBANSpec = namedtuple('IBANSpec', ('bban_length', 'bban_structure',
                                   'bank_identifier_length', 'examples'))

for record in reader(file_name):
    country_code = record['Country code as defined in ISO 3166']
    iban_structure = record['IBAN structure']
    iban_examples = extract_examples(record['IBAN electronic format example'])
    try:
        bban_length = int(record['BBAN length'])
    except ValueError:
        bban_length = int(record['IBAN length']) - 4
        bban_structure = iban_structure[5:]
    else:
        bban_structure = record['BBAN structure']
    try:
        min_pos, max_pos = extract_pos(record['Bank identifier position '
                                              'within the BBAN'])
    except ValueError:
        min_pos, max_pos = 1, 0
    try:
        bank_identifier_length = extract_length(record['Bank identifier '
                                                       'length'])
    except ValueError:
        bank_identifier_length = max_pos
    # Differently from all others, Italian BBANs start with a letter before
    # the bank identifier. As simolification, we treat that letter as part of
    # the bank identifier:
    bank_identifier_length += min_pos - 1
    # build IBAN spec
    iban_spec = IBANSpec(bban_length, format_spec_to_regexp(bban_structure),
                         bank_identifier_length, iban_examples)
    # If country code is not a 2-character code, extract country codes from
    # IBAN structure specs:
    if len(country_code) != 2:
        for code in iban_structure.split(','):
            _IBAN_registry[code.strip()[:2]] = iban_spec
    else:
        _IBAN_registry[country_code] = iban_spec

# correct known errors

# missing check digits in example for CR:
record = _IBAN_registry['CR']
example = record.examples[0]
example = example[:2] + '05' + example[2:]
record = record._replace(examples=(example,))
_IBAN_registry['CR'] = record

# blanks in example for MC:
record = _IBAN_registry['MC']
record = record._replace(examples=('MC5811222000010123456789030',))
_IBAN_registry['MC'] = record

# wrong structure spec and wrong check digits for SC:
record = _IBAN_registry['SC']
regexp = format_spec_to_regexp('4!a2!n2!n16!n3!a')
record = record._replace(bban_structure=re.compile(regexp))
example = record.examples[0]
example = example[:2] + '18' + example[4:]
record = record._replace(examples=(example,))
_IBAN_registry['SC'] = record


# for testing purposes
def _dump_registry():
    for key, val in sorted(_IBAN_registry.items()):
        print(key, val)


# query function
def get_iban_spec(country_code):
    """Retrieve IBAN structure spec from registry."""
    return _IBAN_registry[country_code]
