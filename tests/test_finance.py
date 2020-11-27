# -*- coding: utf-8 -*-
##----------------------------------------------------------------------------
## Name:        test_finance
## Purpose:     Test driver for module finance
##
## Author:      Michael Amrhein (mamrhein@users.sourceforge.net)
##
## Copyright:   (c) 2017 Michael Amrhein
## License:     This program is part of a larger application. For license
##              details please read the file LICENSE.TXT provided together
##              with the application.
##----------------------------------------------------------------------------
## $Source$
## $Revision$


"""Test driver for module finance"""


from __future__ import absolute_import, unicode_literals
import unittest
from identifiers.finance import MIC, ISIN


__metaclass__ = type


class MICTest(unittest.TestCase):

    def test_constructor(self):
        # wrong type of argument
        self.assertRaises(TypeError, MIC, 14)
        # wrong number of chars
        self.assertRaises(ValueError, MIC, 'ABCDE')
        self.assertRaises(ValueError, MIC, ' ABC  ')
        # wrong chars
        self.assertRaises(ValueError, MIC, 'ABcd')
        self.assertRaises(ValueError, MIC, 'ABCÜ')
        # unknown MIC
        self.assertRaises(ValueError, MIC, 'ZZ00')
        # correct MIC
        arg = 'ASEX'
        mic = MIC(arg)
        self.assertEqual(str(mic), arg)
        arg = '   ROCO  \n'
        mic = MIC(arg)
        self.assertEqual(str(mic), arg.strip())
        # ensure slot-only instance
        self.assertRaises(AttributeError, getattr, mic, '__dict__')


class ISINTest(unittest.TestCase):

    def test_constructor_1(self):
        # wrong number of arguments
        self.assertRaises(TypeError, ISIN, 'JU', 147, 'a')
        # wrong type of argument
        self.assertRaises(TypeError, ISIN, 147)
        # unknown country
        self.assertRaises(ValueError, ISIN, 'JU11CBJO0010')
        # wrong number of chars
        self.assertRaises(ValueError, ISIN, 'JOCBAVHDUE643')
        self.assertRaises(ValueError, ISIN, 'JOCBAVHDUE6')
        # wrong chars
        self.assertRaises(ValueError, ISIN, 'JOCBAVHdue64')
        self.assertRaises(ValueError, ISIN, 'JOCBÄVHDUE64')
        # wrong check digit
        self.assertRaises(ValueError, ISIN, 'JOCB9VHDUE64')
        # syntactic correct ISIN
        arg = 'JOCB9VHDUE67'
        isin = ISIN(arg)
        self.assertEqual(isin._id, arg)
        arg = ' JOCB9VHDUE67  \n'
        isin = ISIN(arg)
        self.assertEqual(isin._id, arg.strip())
        # ensure slot-only instance
        self.assertRaises(AttributeError, getattr, isin, '__dict__')

    def test_constructor_2(self):
        # wrong type of argument
        self.assertRaises(TypeError, ISIN, 38, 'ABC')
        self.assertRaises(TypeError, ISIN, 'JO', 10000000000131)
        self.assertRaises(TypeError, ISIN, 'JO', 3.9)
        # invalid / unknown country code
        self.assertRaises(ValueError, ISIN, 'JO47', 'CBJO')
        self.assertRaises(ValueError, ISIN, 'xx', 'CBJO')
        # wrong number of chars
        self.assertRaises(ValueError, ISIN, 'JO', '00000')
        self.assertRaises(ValueError, ISIN, 'JO', '0010080131')
        # wrong chars
        self.assertRaises(ValueError, ISIN, 'JO', 'CBJoVH302')
        self.assertRaises(ValueError, ISIN, 'JO', 'CBJAV#302')
        # syntactic correct ISIN
        args = ('JO', 'CBJAVH302')
        isin = ISIN(*args)
        self.assertEqual(isin._id, 'JOCBJAVH3025')
        args = ('JO', 'AVH302')
        isin = ISIN(*args)
        self.assertEqual(isin._id, 'JO000AVH3022')

    def test_elements(self):
        isin = ISIN('JO000AVH3022')
        self.assertEqual(isin.country_code, 'JO')
        self.assertEqual(isin.nsin, '000AVH302')
        self.assertEqual(isin.check_digit, '2')
        self.assertEqual(isin.elements(), ('JO', '000AVH302', '2'))

    def test_str(self):
        isin = ISIN('JOCB9VHDUE67')
        self.assertEqual(str(isin), 'JOCB9VHDUE67')
