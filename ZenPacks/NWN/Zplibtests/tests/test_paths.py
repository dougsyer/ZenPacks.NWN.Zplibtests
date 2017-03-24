#!/usr/bin/env python
# pylint: disable=C0111, W0201
import Globals
from Products.ZenUtils.Utils import unused

from Products.ZenTestCase.BaseTestCase import BaseTestCase

# zenpacklib Imports
from ZenPacks.zenoss.ZenPackLib.tests.ZPLTestHarness import ZPLTestHarness

from .test_utils import my_dev_factory

unused(Globals)

with open('../zenpack.yaml', 'r') as f:
    zpl_yaml = f.read()

print 'loading yaml'
t_zp = ZPLTestHarness(zpl_yaml)


class TestPaths(BaseTestCase):
    """
    test to make sure that components with nested base classes get appropriate paths so
    that subcomponent panels on non-containing relations work
    """

    def afterSetUp(self):
        super(TestPaths, self).afterSetUp()
        self.dmd.REQUEST = None

        # Create standard objects the ZenPack relies on.
        self.CFG = t_zp.cfg

        # to zccess zpl config in pdb uncomment
        # import pdb; pdb.set_trace()

        _ = my_dev_factory(self.dmd)
        self.test_my_dev = self.dmd.Devices.MyTestOrganizer.getDevices()[0]

    def test_mydev_creation(self):
        """ test basic instantiation of mydev """
        from ZenPacks.NWN.Zplibtests.MyDev import MyDev

        self.assertIsInstance(self.test_my_dev, MyDev, msg='My device not being created')
        print self.test_my_dev.subClass1s()[0].getAllPaths()
        print self.test_my_dev.subClass2s()[0].getAllPaths()
        print self.test_my_dev.subClass3s()[0].getAllPaths()


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestPaths))
    return suite

if __name__ == "__main__":
    from zope.testrunner.runner import Runner  # pylint: disable=C0413,E0611
    runner = Runner(found_suites=[test_suite()])
    runner.run()
