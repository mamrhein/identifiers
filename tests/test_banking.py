# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Name:        test_banking
# Purpose:     Test driver for module banking
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


"""Test driver for module banking"""


from __future__ import absolute_import, unicode_literals
import unittest
from identifiers.banking import BIC, IBAN
from identifiers.ibanregistry import IBAN_REGISTRY, get_iban_spec


__metaclass__ = type


class BICTest(unittest.TestCase):

    def test_constructor(self):
        # wrong type of argument
        self.assertRaises(TypeError, BIC, 14)
        # wrong number of chars
        self.assertRaises(ValueError, BIC, 'ABCDBEBBXX')
        self.assertRaises(ValueError, BIC, 'ABCDEFG')
        # wrong chars
        self.assertRaises(ValueError, BIC, 'abcdbebbxxx')
        self.assertRaises(ValueError, BIC, 'ABCDBEBBXXÜ')
        # unknown country
        self.assertRaises(ValueError, BIC, 'ABCDBXBBXXX')
        # correct BIC
        arg = 'ABCDBEBBXXX'
        bic = BIC(arg)
        self.assertEqual(str(bic), arg)
        arg = ' ABCDBEB5  \n'
        bic = BIC(arg)
        self.assertEqual(str(bic), arg.strip())
        # ensure slot-only instance
        self.assertRaises(AttributeError, getattr, bic, '__dict__')

    def test_elements(self):
        bic = BIC('ABCDBEB3XXX')
        self.assertEqual(bic.party_prefix, 'ABCD')
        self.assertEqual(bic.country_code, 'BE')
        self.assertEqual(bic.party_suffix, 'B3')
        self.assertEqual(bic.branch_code, 'XXX')
        self.assertEqual(bic.elements(), ('ABCD', 'BE', 'B3', 'XXX'))
        bic = BIC('ABCDBEB3')
        self.assertEqual(bic.party_prefix, 'ABCD')
        self.assertEqual(bic.country_code, 'BE')
        self.assertEqual(bic.party_suffix, 'B3')
        self.assertEqual(bic.branch_code, '')
        self.assertEqual(bic.elements(), ('ABCD', 'BE', 'B3', ''))


class IBANTest(unittest.TestCase):

    def test_constructor_1(self):
        # wrong number of arguments
        self.assertRaises(TypeError, IBAN, 'JU', 147)
        # wrong type of argument
        self.assertRaises(TypeError, IBAN, 147)
        # unknown country
        self.assertRaises(ValueError, IBAN, 'JU11CBJO0010000000000131AVH302')
        # wrong number of chars
        self.assertRaises(ValueError, IBAN, 'JO11CBJO0010000000000131AVH')
        self.assertRaises(ValueError, IBAN, 'JO11CBJO0010000000000131AVH3029')
        # wrong chars
        self.assertRaises(ValueError, IBAN, 'JO11CBJ00010000000000131AVH302')
        self.assertRaises(ValueError, IBAN, 'JO11CBJO001C000000000131AVH302')
        # wrong check digits
        self.assertRaises(ValueError, IBAN, 'JO71CBJO0010000000000131AVH302')
        # correct IBAN
        arg = 'JO11CBJO0010000000000131AVH302'
        iban = IBAN(arg)
        self.assertEqual(iban._id, arg)
        arg = ' JO11CBJO0010000000000131AVH302  \n'
        iban = IBAN(arg)
        self.assertEqual(iban._id, arg.strip())
        # ensure slot-only instance
        self.assertRaises(AttributeError, getattr, iban, '__dict__')

    def test_constructor_3(self):
        # wrong type of argument
        self.assertRaises(TypeError, IBAN, 38, 147, 'ABC')
        self.assertRaises(TypeError, IBAN, 'JO', 147.0, 10000000000131)
        self.assertRaises(TypeError, IBAN, 'JO', 'CBJO3845', 3.9)
        # invalid / unknown country code
        self.assertRaises(ValueError, IBAN, 'JO47', 'CBJO',
                          '0010000000000131AVH302')
        self.assertRaises(ValueError, IBAN, 'xx', 'CBJO',
                          '0010000000000131AVH302')
        # wrong number of chars
        self.assertRaises(ValueError, IBAN, 'JO', 'CBJO0000', '000000131AVH')
        self.assertRaises(ValueError, IBAN, 'JO', 'CBJO', '0010080131AVH3029')
        # wrong chars
        self.assertRaises(ValueError, IBAN, 'JO', 'CBJ00010',
                          '000000000131AVH302')
        self.assertRaises(ValueError, IBAN, 'JO', 'CBJO001C',
                          '000000000131AVH302')
        # correct IBAN
        args = ('JO', 'CBJO0010', '000000000131AVH302')
        iban = IBAN(*args)
        self.assertEqual(iban._id, 'JO11CBJO0010000000000131AVH302')
        args = ('DE', 10000000, 1020304050)
        iban = IBAN(*args)
        self.assertEqual(iban._id, 'DE53100000001020304050')

    def test_elements(self):
        iban = IBAN('JO11CBJO0010000000000131AVH302')
        self.assertEqual(iban.country_code, 'JO')
        self.assertEqual(iban.check_digits, '11')
        self.assertEqual(iban.bank_identifier, 'CBJO0010')
        self.assertEqual(iban.bank_account_number, '000000000131AVH302')
        self.assertEqual(iban.elements(), ('JO', '11', 'CBJO0010',
                                           '000000000131AVH302'))
        iban = IBAN('MT84MALT011000012345MTLCAST001S')
        self.assertEqual(iban.country_code, 'MT')
        self.assertEqual(iban.check_digits, '84')
        self.assertEqual(iban.bank_identifier, 'MALT01100')
        self.assertEqual(iban.bank_account_number, '0012345MTLCAST001S')
        self.assertEqual(iban.elements(), ('MT', '84', 'MALT01100',
                                           '0012345MTLCAST001S'))

    def test_examples(self):
        for country_code in IBAN_REGISTRY:
            iban_spec = get_iban_spec(country_code)
            for exmpl in iban_spec.examples:
                self.assertTrue(IBAN(exmpl))

    def test_str(self):
        iban = IBAN('JO11CBJO0010000000000131AVH302')
        self.assertEqual(str(iban), 'JO11 CBJO 0010 0000 0000 0131 AVH3 02')
        iban = IBAN('MT84MALT011000012345MTLCAST001S')
        self.assertEqual(str(iban), 'MT84 MALT 0110 0001 2345 MTLC AST0 01S')
