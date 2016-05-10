# -*- coding: utf-8 -*-
##----------------------------------------------------------------------------
## Name:        test_identifier
## Purpose:     Test driver for module identifier
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


"""Test driver for module identifier"""


from __future__ import absolute_import, unicode_literals
from abc import ABCMeta
from copy import copy, deepcopy
import unittest
from uuid import uuid1
from identifiers.identifier import Identifier


__metaclass__ = type


class Id(Identifier):

    def __init__(self, id):
        self._id = id

    def __str__(self):
        return str(self._id)


class Id2(Id):

    pass


class IdentifierTest(unittest.TestCase):

    # Use concrete classes 'Id' and 'Id2' to test common features implemented
    # in the abstract base class

    def setUp(self):
        self.test_args = args = (3859015, 'abcde', uuid1(), object())
        self.zipped_args = zip(args, args[-1:] + args[:-1])

    def test_abc(self):
        self.assertTrue(isinstance(Identifier, ABCMeta))
        self.assertRaises(TypeError, Identifier, 'a')
        self.assertRaises(TypeError, Identifier, 5)

    def test_copy(self):
        for arg in self.test_args:
            id = Id(arg)
            self.assertTrue(copy(id) is id)
            self.assertTrue(deepcopy(id) is id)

    def test_hash(self):
        for arg in self.test_args:
            self.assertNotEqual(hash(Id(arg)), hash(Id2(arg)))
        for arg1, arg2 in self.zipped_args:
            self.assertEqual(hash(Id(arg1)), hash(Id(arg1)))
            self.assertNotEqual(hash(Id(arg1)), hash(Id(arg2)))

    def test_eq(self):
        for arg in self.test_args:
            self.assertNotEqual(Id(arg), Id2(arg))
        for arg1, arg2 in self.zipped_args:
            self.assertEqual(Id(arg1), Id(arg1))
            self.assertNotEqual(Id(arg1), Id(arg2))
