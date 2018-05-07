""" test modeler doc string test aded to this docscring will show up in modeller plugin selection in gui"""

from Products.DataCollector.plugins.CollectorPlugin import PythonPlugin
from Products.DataCollector.plugins.DataMaps import (
    ObjectMap,
    RelationshipMap,
    MultiArgs
)


class TestMap1(PythonPlugin):
    """"Return dummy output for modeler demo"""

    def collect(self, device, log):
        """
        normally you are going out on the network to model here

        WARNING:  I would not set device title or ip this way normally...this is jsut a demonstration


        titles are used to associate external events to their component objects in transforms
        but most access to a component title is called via component.titleOrId() that fails to using id
        if title isnt there..
        I wouldnt set an ip this way its just a demonstration on how to use a method in modelling
        if you have more than one arg you need to wrap your return in the MultiArgs() function

        """

        log.info('Collecting {} for {}'.format(self.__class__.__name__, device.id))

        # naked object map with no relations will set property on device by default
        dev_om = ObjectMap({
            'title':  'test_device',
            'setManageIp': '44.44.44.44',
            'setProductKey': MultiArgs('FakeOS v1 SP1', 'FakeOSManufaturer'),
        })

        """ would be create if in zenpacklib there were helpers/classmethods so you dont have to hard code
        compname and relname and prepid everything over and over.  i usually add in a mixin class to do this...
        will add an example at some point.

        there are instance methods to get containing relationship  but that doesnt really help here

        note:  if you try to set non-containing relationships before the object on the other side of the relationship is
        created then the relation will get added on the next model...so best to try to add the non-containing
        relationships setters as the end...not sure if that even resolved it 100% of the time
        in this case better to add subclass 2 to the end of the results list
        """

        results = [
            RelationshipMap(
                modname="ZenPacks.NWN.Zplibtests.SubClass1",
                relname="subClass1s",
                objmaps=[ObjectMap({
                    'id': self.prepId('subComponent-1'),
                    'title': 'subComponent-1',
                    'my_prop_1': 'testprop1',
                    'my_prop_2': 'testprop2',
                    'sub_prop_1': 'subprop1',
                    'set_subClass2s': map(self.prepId, ['subComponent-2', ]),
                })]),

            RelationshipMap(
                modname="ZenPacks.NWN.Zplibtests.SubClass2",
                relname="subClass2s",
                objmaps=[ObjectMap({
                    'id': self.prepId('subComponent-2'),
                    'title': 'subComponent-2',
                    'set_subClass3s': map(self.prepId, ['subComponent-3', ]),
                    'set_subClass4s': map(self.prepId, ['subComponent-4', ]), })]),

            RelationshipMap(
                modname="ZenPacks.NWN.Zplibtests.SubClass3",
                relname="subClass3s",
                objmaps=[ObjectMap({
                    'id': self.prepId('subComponent-3'),
                    'title': 'subComponent-3'})]),

            RelationshipMap(
                modname="ZenPacks.NWN.Zplibtests.SubClass4",
                relname="subClass4s",
                objmaps=[ObjectMap({
                    'id': self.prepId('subComponent-4'),
                    'title': 'subComponent-4'})]),
        ]

        # if you need python debugger...
        # import pdb; pdb.set_trace()

        # note, you cant just do this...
        # rms.append(dev_om)...wont work because of the way ObjectMap was written
        results.extend([dev_om, ])

        return results

    def process(self, device, results, log):
        """ after collllect runs preprocess then process"""

        log.info('processing {} for {}: {}'.format(self.__class__.__name__, device.id, results))
        return results
