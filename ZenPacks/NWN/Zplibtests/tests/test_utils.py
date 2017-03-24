"""
shared utilities used for zenpack testing
many of these utilities are copied from Zenoss's testing code in zenpacklib or vsphere tests
"""
# pylint: disable=C0111, W0201, W0612

import logging

import Globals

import functools
import random
import importlib
import unittest

import zope.component
from zope.traversing.adapters import DefaultTraversable

from Products.Five import zcml
import Products.ZenTestCase
from Products.ZenTestCase.BaseTestCase import BaseTestCase, ZenossTestCaseLayer
from Products.DataCollector.ApplyDataMap import ApplyDataMap
from Products.ZenRelations.RelationshipBase import RelationshipBase
from Products.ZenRelations.ToManyContRelationship import ToManyContRelationship
from Products.ZenUtils.Utils import unused

from transaction._transaction import Transaction

import os
unused(Globals)

LOG = logging.getLogger('zen.nwnzplibtest')


def addContained(obj, relname, target):
    """
    COPIED FROM zenpacklib.tests.test_exta_paths

    When a manually-created python object is first added to its container, we
    need to reload it, as its in-memory representation is changed.
    """
    rel = getattr(obj, relname)

    # contained via a relationship
    if isinstance(rel, ToManyContRelationship):
        rel._setObject(target.id, target)
        return rel._getOb(target.id)

    elif isinstance(rel, RelationshipBase):
        rel.addRelation(target)
        return rel._getOb(target.id)

    # contained via a property
    else:
        # note: in this scenario, you must have the target object's ID the same
        #       as the relationship from the parent object.

        assert relname == target.id
        obj._setObject(target.id, target)
        return getattr(obj, relname)


def addNonContained(obj, relname, target):
    """ add a non containnig relation """
    rel = getattr(obj, relname)
    rel.addRelation(target)
    return target


def my_dev_factory(dmd):  # pylint: disable=R0914
    """ create a mydevice objects"""

    # DeviceClass
    dc = dmd.Devices.createOrganizer('/MyTestOrganizer')
    dc.setZenProperty('zPythonClass', 'ZenPacks.NWN.Zplibtests.MyDev')

    # cluster
    my_dev = dc.createInstance('test_mydev')
    # not needed just for superstition
    my_dev.setManageIp('44.44.44.44')

    # create device
    from ZenPacks.NWN.Zplibtests.MyDev import MyDev
    from ZenPacks.NWN.Zplibtests.SubClass1 import SubClass1
    from ZenPacks.NWN.Zplibtests.SubClass2 import SubClass2
    from ZenPacks.NWN.Zplibtests.SubClass3 import SubClass3

    # wish the containing_relname method was a classproperty..
    sub1 = addContained(my_dev, 'subClass1s', SubClass1('sub1'))
    sub2 = addContained(my_dev, 'subClass2s', SubClass2('sub2'))
    sub3 = addContained(my_dev, 'subClass3s', SubClass3('sub3'))

    # use facet name to create 2nd param to do..?
    addNonContained(sub1, "subClass2s", sub2)
    addNonContained(sub2, "subClass3s", sub3)

    return my_dev

