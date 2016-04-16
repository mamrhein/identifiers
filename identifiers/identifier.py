# -*- coding: utf-8 -*-
##----------------------------------------------------------------------------
## Name:        identifier
## Purpose:     Abstract base class for identifiers
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


"""Abstract base class for identifiers"""


from __future__ import absolute_import
from abc import ABCMeta, abstractmethod


__metaclass__ = type


# decorator defining meta class, portable between Python 2 / Python 3
def _withMetaCls(metaCls):
    def _createCls(cls):
        namespace = dict(cls.__dict__)
        # remove descriptors for slots (will be recreated by metaclass)
        try:
            slots = namespace['__slots__']
        except KeyError:
            pass
        else:
            for name in slots:
                del namespace[name]
        return metaCls(cls.__name__, cls.__bases__, namespace)
    return _createCls


@_withMetaCls(ABCMeta)
class Identifier():

    """Abstract base class for identifiers."""

    __slots__ = ('_id',)

    @abstractmethod
    def __init__(self, *args, **kwds):
        """Initialize identifier."""

    def __copy__(self):
        """copy(self)"""
        return self         # Identifiers are immutable

    __deepcopy__ = __copy__

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
