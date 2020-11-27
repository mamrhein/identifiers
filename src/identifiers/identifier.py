# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Name:        identifier
# Purpose:     Abstract base class for identifiers
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


"""Abstract base class for identifiers"""


from abc import ABCMeta, abstractmethod


class Identifier(metaclass=ABCMeta):

    """Abstract base class for identifiers."""

    __slots__ = ('_id',)

    @abstractmethod
    def __init__(self, *args, **kwds):
        pass

    def __copy__(self):
        """copy(self)

        Returns self (identifiers are immutable)."""
        return self

    def __deepcopy__(self, memo):
        """deepcopy(self)

        Returns self (identifiers are immutable)."""
        return self.__copy__()

    def __hash__(self):
        """hash(self)"""
        return hash(self.__class__.__name__ + str(self._id))

    def __eq__(self, other):
        """self == other"""
        return self.__class__ == other.__class__ and self._id == other._id

    @abstractmethod
    def __str__(self):
        """str(self)"""

    def __repr__(self):
        """repr(self)"""
        return self.__class__.__name__ + "('" + str(self._id) + "')"
