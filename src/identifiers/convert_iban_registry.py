#!/usr/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Name:        ibanutils
# Purpose:     Convert SWIFT iban registry file into a Python module
#
# Author:      Michael Amrhein (mamrhein@users.sourceforge.net)
#
# Copyright:   (c) 2017 Michael Amrhein
# License:     This program is part of a larger application. For license
#              details please read the file LICENSE.TXT provided together
#              with the application.
# ---------------------------------------------------------------------------
# $Source$
# $Revision$


"""Utility to convert SWIFT iban registry file into a Python module"""


# standard library imports
from csv import reader as CSVReader
from collections import namedtuple
from itertools import groupby
import os.path
from pprint import pprint
import re
import sys
from typing import Generator, IO, List, Optional, Pattern, Tuple

# local imports
pkg_dir = os.path.dirname(__file__)
sys.path = [os.path.dirname(pkg_dir)] + sys.path
# noinspection PyUnresolvedReferences,PyPackageRequirements
from identifiers.ibanutils import calc_iban_check_digits, split_iban


# TODO: renew IBAN registry
# Version 77 (May 2017),
# downloaded from 'https://www.swift.com/file/32751/download?token=JVZ22AEg',
# transposed and converted to csv
file_name: str = os.path.join(os.path.dirname(__file__),
                              "swift_standards_ibanregistry.txt")


def reader(file_name: str, encoding: Optional[str] = 'cp1252') \
        -> Generator[List[str], None, None]:
    """Return iterator over rows in file `path_to_input_file` in CSV format."""
    with open(file_name, mode='r', encoding=encoding) as csv_file:
        for row in CSVReader(csv_file, delimiter='\t', quotechar='"'):
            yield row


class IBANRecord:
    """Data holder for IBAN registry records"""
    pass


def read_registry(file_name: str) -> List[IBANRecord]:
    """Extract IBAN rules from file `path_to_input_file`."""
    rdr = reader(file_name)
    head_line = next(rdr)
    n_specs = len(head_line) - 1
    print("%i IBAN specs found." % n_specs)
    records = [IBANRecord() for _ in range(n_specs)]
    for line in rdr:
        data_elem_name, values = line[0], line[1:]
        # exclude lines used as sub-section headers
        if data_elem_name not in ('BBAN', 'IBAN'):
            attr_name = data_elem_name \
                .split('(')[0] \
                .split('/')[0] \
                .strip() \
                .replace(' ', '_') \
                .lower()
            for idx, value in enumerate(values):
                value = value.strip()
                if value == 'N/A':
                    value = None
                setattr(records[idx], attr_name, value)
        if data_elem_name == 'IBAN print format example':
            break  # skip the rest
    return records


# regexp to find format specs
FORMAT_REGEXP = r'(\d+)([!]*)([nace])'
_format = re.compile(FORMAT_REGEXP)


def group_format_spec(spec: str) -> Generator[Tuple[str, int, int],
                                              None, None]:
    """Group elements from format spec."""
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


def format_spec_to_regexp(spec: str) -> Pattern:
    """Build regexp from format spec"""
    expr = ''.join((CHAR_TYPE_MAP[_type] + '{' + str(min_length) +
                    '}' if min_length == max_length else ',%s}' % max_length
                    for _type, min_length, max_length
                    in group_format_spec(spec)))
    return re.compile(expr)


def extract_length(spec: str) -> int:
    """Get length value form format spec"""
    # spec = spec.split(';')[0]
    # try:
    #     return int(spec)
    # except ValueError:
    #     pass
    length = sum(int(n_chars) for n_chars, _, _ in _format.findall(spec))
    if length > 0:
        return length
    raise ValueError


# regexp to find position specs
POS_REGEXP = r'(\d{1,2})([-]*)(\d{0,2})'
_pos = re.compile(POS_REGEXP)


def extract_pos(spec: str) -> Tuple[int, int]:
    """Get start and end pos values from format spec"""
    pos_specs = _pos.findall(spec)
    if pos_specs:
        start, _, end = pos_specs[0]
        start = int(start)
        end = int(end) if end else start
        if start <= end:
            return start, end
    raise ValueError


def guess_pattern(example: str) -> Tuple[int, str]:
    """Guess pattern from example."""
    try:
        length = len(example)
    except TypeError:
        return 0, ''
    try:
        int(example)
    except ValueError:
        pattern = '%i!c' % length
    else:
        pattern = '%i!n' % length
    return length, pattern


IBANSpec = namedtuple('IBANSpec', ('bban_length', 'bban_structure',
                                   'bban_split_pos', 'examples'))


# noinspection PyUnresolvedReferences
def record_2_spec(record: IBANRecord) -> Tuple[str, IBANSpec]:
    """Convert IBANRecord `record` to country code and IBANSpec."""
    errors = []
    # extract relevant attrs from record
    country_code = record.iban_prefix_country_code
    bban_length = int(record.bban_length)
    bban_structure = record.bban_structure
    bank_id_pos = record.bank_identifier_position_within_the_bban
    if bank_id_pos:
        bank_id_start, bank_id_end = extract_pos(bank_id_pos)
        bank_id_length_from_pos = bank_id_end - bank_id_start + 1
    else:
        bank_id_length_from_pos = 0
    bank_id_pattern = record.bank_identifier_pattern
    bank_id_example = record.bank_identifier_example
    if bank_id_pattern:
        try:
            bank_id_length_from_pattern = extract_length(bank_id_pattern)
        except ValueError:
            # guess from example
            bank_id_length_from_pattern, bank_id_pattern = \
                guess_pattern(bank_id_example)
            errors.append("Bank id pattern misformed, guessed as: '%s'"
                          % bank_id_pattern)
    elif bank_id_example:
        # guess from example
        bank_id_length_from_pattern, bank_id_pattern = \
            guess_pattern(bank_id_example)
        errors.append("Bank id pattern missing, guessed as: '%s'"
                      % bank_id_pattern)
    else:
        bank_id_length_from_pattern, bank_id_pattern = 0, ''
    branch_id_pos = record.branch_identifier_position_within_the_bban
    if branch_id_pos:
        branch_id_start, branch_id_end = extract_pos(branch_id_pos)
        branch_id_length_from_pos = branch_id_end - branch_id_start + 1
    else:
        branch_id_length_from_pos = 0
    branch_id_pattern = record.branch_identifier_pattern
    branch_id_example = record.branch_identifier_example
    if branch_id_pattern:
        try:
            branch_id_length_from_pattern = extract_length(branch_id_pattern)
        except ValueError:
            # guess from example
            branch_id_length_from_pattern, branch_id_pattern = \
                guess_pattern(branch_id_example)
            errors.append("Branch id pattern misformed, guessed as: '%s'"
                          % branch_id_pattern)
    elif branch_id_example:
        # guess from example
        branch_id_length_from_pattern, branch_id_pattern = \
            guess_pattern(branch_id_example)
        errors.append("Branch id pattern missing, guessed as: '%s'"
                      % branch_id_pattern)
    else:
        branch_id_length_from_pattern, branch_id_pattern = 0, ''
    bban_split_pos = bank_id_length_from_pos + branch_id_length_from_pos
    # Differently from all others, Italian and San Marinos BBANs start with a
    # letter before the bank identifier. As simplification, we treat that
    # letter as part of the bank identifier:
    if country_code in ('IT', 'SM'):
        shift = 1  # provide for extra char
        bban_split_pos += 1
    else:
        shift = 0
    iban_length = int(record.iban_length)
    iban_structure = record.iban_structure
    iban_example = record.iban_electronic_format_example
    # check consistency
    # check length and positions within BBAN
    if bank_id_length_from_pos != bank_id_length_from_pattern:
        errors.append('Bank id position and pattern inconsistent')
    if branch_id_length_from_pos != branch_id_length_from_pattern:
        errors.append('Branch id position and pattern inconsistent')
    # check patterns
    if iban_structure != '%s2!n%s' % (country_code, bban_structure):
        # print("'%s'" % iban_structure,
        #       "'%s'" % country_code,
        #       "'%s'" % bban_structure)
        errors.append('Patterns for IBAN and BBAN inconsistent')
    if not bban_structure[shift * 3:].startswith('%s%s'
                                                 % (bank_id_pattern,
                                                    branch_id_pattern)):
        # print("'%s'" % bban_structure[shift * 3:],
        #       "'%s%s'" % (bank_id_pattern, branch_id_pattern))
        errors.append('Patterns for BBAN, bank id and branch id inconsistent')
    # check total length
    if iban_length != bban_length + 4:
        errors.append('Length specs for IBAN and BBAN inconsistent')
    # build regexp to check BBAN
    bban_regexp = format_spec_to_regexp(bban_structure)
    # check example
    exmpl_cc, exmpl_check_digits, exmpl_bban = split_iban(iban_example)
    if exmpl_cc != country_code:
        errors.append('IBAN example does not start with country code')
    if not bban_regexp.match(exmpl_bban):
        errors.append('BBAN part of example does not match BBAN structure')
    corr_check_digits = calc_iban_check_digits(country_code, exmpl_bban)
    if exmpl_check_digits != corr_check_digits:
        errors.append("Wrong check digits in IBAN example; should be '%s'"
                      % corr_check_digits)
        iban_example = country_code + corr_check_digits + exmpl_bban
    # build IBAN spec
    iban_spec = IBANSpec(bban_length, bban_regexp, bban_split_pos,
                         (iban_example,))
    # print errors
    if errors:
        print("Spec for '%s':" % country_code)
        for msg in errors:
            print('  ', msg)
        print('   Guessed BBAN split: %i' % bban_split_pos)
        print('   Guessed BBAN regexp: %s' % bban_regexp)
    # build IBAN specs to return
    return country_code, iban_spec


def write_module_header(py_file: IO, file_name: str) -> None:
    """Write header to Python module."""
    py_file.writelines((
        "# -*- coding: utf-8 -*-\n",
        "# $Source$\n",
        "# $Revision$\n",
        "\n",
        "\"\"\"IBAN registry generated from file '%s'\"\"\"\n" % file_name,
        "\n",
        "from collections import namedtuple\n",
        "import re\n",
        "\n",
        "IBANSpec = namedtuple(\n    '%s',\n" % IBANSpec.__name__,
        "    %s)\n" % str(IBANSpec._fields),
        "\n"))


def write_code(py_file: IO, iban_registry: dict) -> None:
    """Write IBAN registry and retrieval code to Python module."""
    py_file.write("IBAN_REGISTRY = \\\n")
    pprint(iban_registry, stream=py_file)
    py_file.writelines((
        "\n\n",
        "# query function\n",
        "def get_iban_spec(country_code: str) -> IBANSpec:\n",
        '    """Retrieve IBAN structure spec from registry."""\n',
        "    return IBAN_REGISTRY[country_code]\n"))


def main(path_to_input_file: str, module_name: str) -> None:
    """Convert IBAN registry to Python module."""
    records = read_registry(path_to_input_file)
    iban_registry = {}
    for record in records:
        country_code, spec = record_2_spec(record)
        iban_registry[country_code] = spec
    if module_name:
        py_file_name = os.path.join(pkg_dir,
                                    os.path.extsep.join((module_name, 'py')))
        with open(py_file_name, mode='w', encoding="utf-8") as py_file:
            write_module_header(py_file, os.path.basename(path_to_input_file))
            write_code(py_file, iban_registry)
    else:
        pprint(iban_registry)


def print_usage() -> None:
    """Print usage hint."""
    print("Usage: %s <input file> [<module name>]" % __file__)


if __name__ == '__main__':
    args = sys.argv[1:]
    n_args = len(args)
    if n_args not in (1, 2):
        print_usage()
    else:
        file_name = args[0]
        try:
            module_name = args[1]
        except IndexError:
            module_name = None
        main(file_name, module_name)
