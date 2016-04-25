# -*- coding: utf-8 -*-
##----------------------------------------------------------------------------
## Name:        test_gs1
## Purpose:     Test driver for module gs1
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


"""Test driver for module gs1"""


from __future__ import absolute_import, unicode_literals
import unittest
from identifiers.gs1 import GLN, GSIN, GTIN12, GTIN13, GTIN14, SSCC


__metaclass__ = type


class GS1NumericalIdentifierTest(unittest.TestCase):

    # Use concrete class 'GLN' to test common features implemented in the
    # abstract base class

    def test_constructor_1(self):
        # wrong type of argument
        self.assertRaises(TypeError, GLN, 5700191234561)
        # wrong number of arguments
        self.assertRaises(TypeError, GLN, '570019', '123456')
        # invalid format
        self.assertRaises(ValueError, GLN, '570019-123456-1')
        self.assertRaises(ValueError, GLN, '570019123456X')
        self.assertRaises(ValueError, GLN, '570 019 123456')
        # wrong number of digits
        self.assertRaises(ValueError, GLN, '57001912345619')
        self.assertRaises(ValueError, GLN, '57001912345')
        # invalid GS1 prefix
        self.assertRaises(ValueError, GLN, '050123456789')
        self.assertRaises(ValueError, GLN, '9780191234561')
        self.assertRaises(ValueError, GLN, '977019123456')
        # invalid company prefix
        self.assertRaises(ValueError, GLN, '569789123456')
        # wrong check digit
        self.assertRaises(ValueError, GLN, '5700191234567')
        # correct GLN
        gln = GLN('5700191234561')
        self.assertEqual(gln._id, '5700191234561')
        gln = GLN('570019123456')
        self.assertEqual(gln._id, '5700191234561')

    def test_constructor_4_5(self):
        # wrong type of argument
        self.assertRaises(TypeError, GLN, 570, '019', '123456', '1')
        self.assertRaises(TypeError, GLN, '570', 19, '123456', '1')
        self.assertRaises(TypeError, GLN, '570', '019', 123456, '1')
        self.assertRaises(TypeError, GLN, '570', '019', '123456', 1)
        # wrong number of digits
        self.assertRaises(ValueError, GLN, '570', '019', '1234567', '1')
        self.assertRaises(ValueError, GLN, '570', '019', '123456', '01')
        # invalid GS1 prefix
        self.assertRaises(ValueError, GLN, '050', '123456', '789')
        self.assertRaises(ValueError, GLN, '977', '019', '123456')
        # invalid company prefix
        self.assertRaises(ValueError, GLN, '569', '789', '123456')
        # wrong check digit
        self.assertRaises(ValueError, GLN, '570', '019', '123456', '9')
        # correct GLN
        gln = GLN('570', '019', '123456', '1')
        self.assertEqual(gln._id, '5700191234561')
        gln = GLN('570', '019', '123456')
        self.assertEqual(gln._id, '5700191234561')

    def test_str(self):
        self.assertEqual(str(GLN('5700191234561')), '5700191234561')


class GLN_Test(unittest.TestCase):

    def test_elements(self):
        gln = GLN('5700271234566')
        self.assertEqual(gln.gs1_prefix, '570')
        self.assertEqual(gln.company_prefix, '570027')
        self.assertEqual(gln.location_reference, '123456')
        self.assertEqual(gln.check_digit, '6')
        self.assertEqual(gln.elements(), ('570027', '123456', '6'))
        gln = GLN('377912345678')
        self.assertEqual(gln.gs1_prefix, '377')
        self.assertEqual(gln.company_prefix, '377912345678')
        self.assertEqual(gln.location_reference, '')
        self.assertEqual(gln.check_digit, '6')
        self.assertEqual(gln.elements(), ('377912345678', '', '6'))

    def test_separated(self):
        gln = GLN('5700271234566')
        self.assertEqual(gln.separated(), '570027-123456-6')
        self.assertEqual(gln.separated('•'), '570027•123456•6')


class GTIN12_Test(unittest.TestCase):

    def test_constructor_1(self):
        # invalid company prefix
        self.assertRaises(ValueError, GTIN12, '56978912345')
        # wrong number of digits
        self.assertRaises(ValueError, GTIN12, '5700191234561')
        self.assertRaises(ValueError, GTIN12, '5700191234')
        # correct GTIN12
        gtin = GTIN12('077123456786')
        self.assertEqual(gtin._id, '077123456786')

    def test_elements(self):
        gtin = GTIN12('077123456786')
        self.assertEqual(gtin.gs1_prefix, '077')
        self.assertEqual(gtin.company_prefix, '0771234')
        self.assertEqual(gtin.item_reference, '5678')
        self.assertEqual(gtin.check_digit, '6')
        self.assertEqual(gtin.elements(), ('0771234', '5678', '6'))

    def test_separated(self):
        gtin = GTIN12('077123456786')
        self.assertEqual(gtin.separated(), '0771234-5678-6')
        self.assertEqual(gtin.separated('•'), '0771234•5678•6')


class GTIN13_Test(unittest.TestCase):

    def test_elements(self):
        gtin = GTIN13('5700271234566')
        self.assertEqual(gtin.gs1_prefix, '570')
        self.assertEqual(gtin.company_prefix, '570027')
        self.assertEqual(gtin.item_reference, '123456')
        self.assertEqual(gtin.check_digit, '6')
        self.assertEqual(gtin.elements(), ('570027', '123456', '6'))
        gtin = GTIN13('377912345678')
        self.assertEqual(gtin.gs1_prefix, '377')
        self.assertEqual(gtin.company_prefix, '377912345678')
        self.assertEqual(gtin.item_reference, '')
        self.assertEqual(gtin.check_digit, '6')
        self.assertEqual(gtin.elements(), ('377912345678', '', '6'))

    def test_separated(self):
        gtin = GTIN13('5700271234566')
        self.assertEqual(gtin.separated(), '570027-123456-6')
        self.assertEqual(gtin.separated('•'), '570027•123456•6')


class GTIN14_Test(unittest.TestCase):

    def test_constructor_1(self):
        # invalid company prefix
        self.assertRaises(ValueError, GTIN14, '1569789123456')
        # wrong number of digits
        self.assertRaises(ValueError, GTIN14, '157001912345678')
        self.assertRaises(ValueError, GTIN14, '157001912345')
        # correct GTIN14
        gtin = GTIN14('40771234567895')
        self.assertEqual(gtin._id, '40771234567895')

    def test_elements(self):
        gtin = GTIN14('40771234567895')
        self.assertEqual(gtin.level_indicator, '4')
        self.assertEqual(gtin.gs1_prefix, '077')
        self.assertEqual(gtin.company_prefix, '0771234')
        self.assertEqual(gtin.item_reference, '56789')
        self.assertEqual(gtin.check_digit, '5')
        self.assertEqual(gtin.elements(), ('4', '0771234', '56789', '5'))

    def test_separated(self):
        gtin = GTIN14('40771234567895')
        self.assertEqual(gtin.separated(), '4-0771234-56789-5')
        self.assertEqual(gtin.separated('•'), '4•0771234•56789•5')


class GSIN_Test(unittest.TestCase):

    def test_constructor_1(self):
        # invalid company prefix
        self.assertRaises(ValueError, GSIN, '56978912345789013')
        # wrong number of digits
        self.assertRaises(ValueError, GSIN, '570789123456789013')
        self.assertRaises(ValueError, GSIN, '570789123456783')
        # correct GSIN
        gsin = GSIN('07712345678901233')
        self.assertEqual(gsin._id, '07712345678901233')

    def test_elements(self):
        gsin = GSIN('07712345678901233')
        self.assertEqual(gsin.gs1_prefix, '077')
        self.assertEqual(gsin.company_prefix, '0771234')
        self.assertEqual(gsin.shipper_reference, '567890123')
        self.assertEqual(gsin.check_digit, '3')
        self.assertEqual(gsin.elements(), ('0771234', '567890123', '3'))

    def test_separated(self):
        gsin = GSIN('07712345678901233')
        self.assertEqual(gsin.separated(), '0771234-567890123-3')
        self.assertEqual(gsin.separated('•'), '0771234•567890123•3')


class SSCC_Test(unittest.TestCase):

    def test_constructor_1(self):
        # invalid company prefix
        self.assertRaises(ValueError, SSCC, '85697891234567890')
        # wrong number of digits
        self.assertRaises(ValueError, SSCC, '8570789123456789019')
        self.assertRaises(ValueError, SSCC, '8570789123456789')
        # correct SSCC
        sscc = SSCC('707712345678901232')
        self.assertEqual(sscc._id, '707712345678901232')

    def test_elements(self):
        sscc = SSCC('707712345678901232')
        self.assertEqual(sscc.extension_digit, '7')
        self.assertEqual(sscc.gs1_prefix, '077')
        self.assertEqual(sscc.company_prefix, '0771234')
        self.assertEqual(sscc.serial_reference, '567890123')
        self.assertEqual(sscc.check_digit, '2')
        self.assertEqual(sscc.elements(), ('7', '0771234', '567890123', '2'))

    def test_separated(self):
        sscc = SSCC('707712345678901232')
        self.assertEqual(sscc.separated(), '7-0771234-567890123-2')
        self.assertEqual(sscc.separated('•'), '7•0771234•567890123•2')
