# -*- coding: utf-8 -*-
##----------------------------------------------------------------------------
## Name:        test_bookland
## Purpose:     Test driver for module bookland
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


"""Test driver for module bookland"""


from __future__ import absolute_import, unicode_literals
import unittest
from identifiers.bookland import ISBN, ISMN, ISSN, ISSN_13


__metaclass__ = type


class ISBNTest(unittest.TestCase):

    def test_constructor_1(self):
        # wrong number of arguments
        self.assertRaises(TypeError, ISBN, '978', '147')
        # wrong type of argument
        self.assertRaises(TypeError, ISBN, 14)
        # invalid format
        self.assertRaises(ValueError, ISBN, '978_982-114-123')
        self.assertRaises(ValueError, ISBN, '978982114123X')
        self.assertRaises(ValueError, ISBN, '978 982 114  123')
        self.assertRaises(ValueError, ISBN, '978 982 114 123  9')
        # wrong number of digits
        self.assertRaises(ValueError, ISBN, '97898211412349')
        self.assertRaises(ValueError, ISBN, '978 982 114 1234 9')
        self.assertRaises(ValueError, ISBN, '97898211412')
        self.assertRaises(ValueError, ISBN, '978 982 114 12')
        # wrong prefix
        self.assertRaises(ValueError, ISBN, '9769821141239')
        self.assertRaises(ValueError, ISBN, '976 982 114 123 9')
        # wrong registration group
        self.assertRaises(ValueError, ISBN, '9789901141239')
        self.assertRaises(ValueError, ISBN, '978 990 114 123 9')
        # wrong registrant
        self.assertRaises(ValueError, ISBN, '978-982-1141-23-9')
        # wrong check digit
        self.assertRaises(ValueError, ISBN, '9789821141234')
        self.assertRaises(ValueError, ISBN, '978 982 114 123 4')
        # correct ISBN
        isbn = ISBN('978351412345')
        self.assertEqual(isbn._id, '9783514123458')
        isbn = ISBN('9783514123458')
        self.assertEqual(isbn._id, '9783514123458')
        isbn = ISBN('978-982-114-123')
        self.assertEqual(isbn._id, '9789821141239')
        isbn = ISBN('978-982-114-123-9')
        self.assertEqual(isbn._id, '9789821141239')
        isbn = ISBN('978 982 114 123')
        self.assertEqual(isbn._id, '9789821141239')
        isbn = ISBN('978 982 114 123 9')
        self.assertEqual(isbn._id, '9789821141239')

    def test_constructor_4_5(self):
        # wrong type of argument
        self.assertRaises(TypeError, ISBN, 978, '3', '514', '12345', '8')
        self.assertRaises(TypeError, ISBN, '978', 3, '514', '12345', '8')
        self.assertRaises(TypeError, ISBN, '978', '3', 514, '12345', '8')
        self.assertRaises(TypeError, ISBN, '978', '3', '514', 12345, '8')
        self.assertRaises(TypeError, ISBN, '978', '3', '514', '12345', 8)
        # wrong number of digits
        self.assertRaises(ValueError, ISBN, '978', '982', '114', '1234', '9')
        self.assertRaises(ValueError, ISBN, '978', '982', '114', '12')
        # wrong prefix
        self.assertRaises(ValueError, ISBN, '976', '982', '114', '123', '9')
        # wrong registration group
        self.assertRaises(ValueError, ISBN, '978', '990', '114', '123', '9')
        # wrong registrant
        self.assertRaises(ValueError, ISBN, '978', '982', '1141', '23', '9')
        # wrong check digit
        self.assertRaises(ValueError, ISBN, '978', '982', '114', '123', '4')
        # correct ISBN
        isbn = ISBN('978', '3', '514', '12345', '8')
        self.assertEqual(isbn._id, '9783514123458')
        isbn = ISBN('978', '982', '114', '123')
        self.assertEqual(isbn._id, '9789821141239')

    def test_elements(self):
        isbn = ISBN('978-982-114-123-9')
        self.assertEqual(isbn.gs1_prefix, '978')
        self.assertEqual(isbn.registration_group, '982')
        self.assertEqual(isbn.registrant, '114')
        self.assertEqual(isbn.publication, '123')
        self.assertEqual(isbn.check_digit, '9')
        self.assertEqual(isbn.elements(), ('978', '982', '114', '123', '9'))

    def test_separated(self):
        isbn = ISBN('978-982-114-123-9')
        self.assertEqual(isbn.separated(), '978-982-114-123-9')
        self.assertEqual(isbn.separated('•'), '978•982•114•123•9')

    def test_str(self):
        isbn = ISBN('978-982-114-123-9')
        self.assertEqual(str(isbn), 'ISBN 978-982-114-123-9')


class ISMNTest(unittest.TestCase):

    def test_constructor_1(self):
        # wrong number of arguments
        self.assertRaises(TypeError, ISMN, '979', '147')
        # wrong type of argument
        self.assertRaises(TypeError, ISMN, 14)
        # invalid format
        self.assertRaises(ValueError, ISMN, '979-0_1100-1234-5')
        self.assertRaises(ValueError, ISMN, '979011001234X')
        self.assertRaises(ValueError, ISMN, '979-0-1100-1234- 5')
        self.assertRaises(ValueError, ISMN, '979-0-1100-1234-5-0')
        # wrong number of digits
        self.assertRaises(ValueError, ISMN, '97901100123')
        self.assertRaises(ValueError, ISMN, '979 0 1100 123')
        self.assertRaises(ValueError, ISMN, '97901100123456')
        self.assertRaises(ValueError, ISMN, '979-0-1100-12345-6')
        # wrong prefix
        self.assertRaises(ValueError, ISMN, '9780110012345')
        self.assertRaises(ValueError, ISMN, '978-0-1100-1234-5')
        # wrong registration group
        self.assertRaises(ValueError, ISMN, '979211001234')
        self.assertRaises(ValueError, ISMN, '979 2 1100 1234')
        # wrong registrant
        self.assertRaises(ValueError, ISMN, '979 0 11001 234 5')
        # wrong check digit
        self.assertRaises(ValueError, ISMN, '9790110012340')
        self.assertRaises(ValueError, ISMN, '979 0 1100 1234 4')
        # correct ISMN
        ismn = ISMN('979011001234')
        self.assertEqual(ismn._id, '9790110012345')
        ismn = ISMN('9790110012345')
        self.assertEqual(ismn._id, '9790110012345')
        ismn = ISMN('979-0-1100-1234')
        self.assertEqual(ismn._id, '9790110012345')
        ismn = ISMN('979-0-1100-1234-5')
        self.assertEqual(ismn._id, '9790110012345')
        ismn = ISMN('979 0 1100 1234')
        self.assertEqual(ismn._id, '9790110012345')
        ismn = ISMN('979 0 1100 1234 5')
        self.assertEqual(ismn._id, '9790110012345')

    def test_constructor_4_5(self):
        # wrong type of argument
        self.assertRaises(TypeError, ISMN, 979, '0', '1100', '1234', '5')
        self.assertRaises(TypeError, ISMN, '979', 0, '1100', '1234', '5')
        self.assertRaises(TypeError, ISMN, '979', '0', 1100, '1234', '5')
        self.assertRaises(TypeError, ISMN, '979', '0', '1100', 1234, '5')
        self.assertRaises(TypeError, ISMN, '979', '0', '1100', '1234', 5)
        # wrong number of digits
        self.assertRaises(ValueError, ISBN, '979', '0', '1100', '12345', '5')
        self.assertRaises(ValueError, ISBN, '979', '0', '1100', '123')
        # wrong prefix
        self.assertRaises(ValueError, ISBN, '976', '0', '1100', '1234', '5')
        # wrong registration group
        self.assertRaises(ValueError, ISBN, '979', '9', '1100', '1234', '5')
        # wrong registrant
        self.assertRaises(ValueError, ISBN, '979', '0', '11001', '234', '5')
        # wrong check digit
        self.assertRaises(ValueError, ISBN, '979', '0', '1100', '1234', '4')
        # correct ISMN
        ismn = ISMN('979', '0', '1100', '1234', '5')
        self.assertEqual(ismn._id, '9790110012345')
        ismn = ISMN('979', '0', '1100', '1234')
        self.assertEqual(ismn._id, '9790110012345')

    def test_elements(self):
        ismn = ISMN('979-0-1100-1234-5')
        self.assertEqual(ismn.gs1_prefix, '979')
        self.assertEqual(ismn.registration_group, '0')
        self.assertEqual(ismn.registrant, '1100')
        self.assertEqual(ismn.publication, '1234')
        self.assertEqual(ismn.check_digit, '5')
        self.assertEqual(ismn.elements(), ('979', '0', '1100', '1234', '5'))

    def test_str(self):
        ismn = ISMN('979-0-1100-1234-5')
        self.assertEqual(str(ismn), 'ISMN 979-0-1100-1234-5')


class ISSNTest(unittest.TestCase):

    def test_constructor(self):
        # wrong type of argument
        self.assertRaises(TypeError, ISSN, 1100123)
        # invalid format
        self.assertRaises(ValueError, ISSN, '03178471X')
        self.assertRaises(ValueError, ISSN, '031784')
        self.assertRaises(ValueError, ISSN, '0317_8471')
        self.assertRaises(ValueError, ISSN, '0317  8471')
        self.assertRaises(ValueError, ISSN, '0317-847-1')
        # wrong check digit
        self.assertRaises(ValueError, ISSN, '0317847X')
        self.assertRaises(ValueError, ISSN, '0317 847X')
        # correct ISSN
        issn = ISSN('03178471')
        self.assertEqual(issn._id, '03178471')
        issn = ISSN('0317-8471')
        self.assertEqual(issn._id, '03178471')
        issn = ISSN('0317 8471')
        self.assertEqual(issn._id, '03178471')
        issn = ISSN('0317847')
        self.assertEqual(issn._id, '03178471')
        issn = ISSN('0317-847')
        self.assertEqual(issn._id, '03178471')
        issn = ISSN('0317 847')
        self.assertEqual(issn._id, '03178471')
        issn = ISSN('1050124X')
        self.assertEqual(issn._id, '1050124X')
        issn = ISSN('1050-124X')
        self.assertEqual(issn._id, '1050124X')
        issn = ISSN('1050 124X')
        self.assertEqual(issn._id, '1050124X')
        issn = ISSN('1050124')
        self.assertEqual(issn._id, '1050124X')
        issn = ISSN('1050-124')
        self.assertEqual(issn._id, '1050124X')
        issn = ISSN('1050 124')
        self.assertEqual(issn._id, '1050124X')

    def test_as_gtin(self):
        issn = ISSN('1050124X')
        self.assertRaises(TypeError, issn.as_gtin, 5)
        self.assertRaises(ValueError, issn.as_gtin, '5')
        gtin = issn.as_gtin()
        self.assertTrue(isinstance(gtin, ISSN_13))
        self.assertEqual(gtin._id, '9771050124008')
        gtin = issn.as_gtin('57')
        self.assertTrue(isinstance(gtin, ISSN_13))
        self.assertEqual(gtin._id, '9771050124572')

    def test_raw_number(self):
        issn = ISSN('1050-124X')
        self.assertEqual(issn.raw_number, '1050124')

    def test_separated(self):
        issn = ISSN('1050-124X')
        self.assertEqual(issn.separated(), '1050-124X')
        self.assertEqual(issn.separated('•'), '1050•124X')

    def test_str(self):
        issn = ISSN('1050-124X')
        self.assertEqual(str(issn), 'ISSN 1050-124X')


class ISSN_13_Test(unittest.TestCase):

    def test_constructor(self):
        # wrong type of argument
        self.assertRaises(TypeError, ISSN_13, 1050124)
        self.assertRaises(TypeError, ISSN_13, '1050124', 25)
        self.assertRaises(TypeError, ISSN_13, ISSN('1050124'), 25)
        self.assertRaises(TypeError, ISSN_13, '9771050124', '25')
        # invalid format
        self.assertRaises(ValueError, ISSN_13, '03178471X')
        self.assertRaises(ValueError, ISSN_13, '031784')
        self.assertRaises(ValueError, ISSN_13, '0317_8471')
        self.assertRaises(ValueError, ISSN_13, '0317  8471')
        self.assertRaises(ValueError, ISSN_13, '0317-847-1')
        self.assertRaises(ValueError, ISSN_13, '9771050124')
        self.assertRaises(ValueError, ISSN_13, '9771050124X25')
        #invalid prefix
        self.assertRaises(ValueError, ISSN_13, '978105012425')
        # invalid addon
        self.assertRaises(ValueError, ISSN_13, '1050124', '5')
        self.assertRaises(ValueError, ISSN_13, '1050124', '125')
        # wrong check digit
        self.assertRaises(ValueError, ISSN_13, '0317847X')
        self.assertRaises(ValueError, ISSN_13, '0317 847X')
        self.assertRaises(ValueError, ISSN_13, '9771050124257')
        # correct ISSN_13
        issn = ISSN('1050-124X')
        for arg in [issn, '1050-124', '1050-124X', '977105012400',
                    '9771050124008']:
            gtin = ISSN_13(arg)
            self.assertEqual(gtin._id, '9771050124008')
        for arg in [issn, '1050-124', '1050-124X']:
            gtin = ISSN_13(arg, '25')
            self.assertEqual(gtin._id, '9771050124251')
        for arg in ['977105012425', '9771050124251']:
            gtin = ISSN_13(arg)
            self.assertEqual(gtin._id, '9771050124251')

    def test_elements(self):
        gtin = ISSN_13('9771050124008')
        self.assertEqual(gtin.gs1_prefix, '977')
        self.assertEqual(gtin.company_prefix, '977')
        self.assertEqual(gtin.item_reference, '105012400')
        self.assertEqual(gtin.check_digit, '8')
        self.assertEqual(gtin.elements(), ('977', '105012400', '8'))

    def test_separated(self):
        gtin = ISSN_13('9771050124008')
        self.assertEqual(gtin.separated(), '977-105012400-8')
        self.assertEqual(gtin.separated('•'), '977•105012400•8')

    def test_extract_issn(self):
        issn = ISSN('1050-124X')
        gtin = ISSN_13(issn)
        self.assertEqual(gtin.extract_issn(), issn)
        gtin = ISSN_13(issn, '25')
        self.assertEqual(gtin.extract_issn(), issn)
