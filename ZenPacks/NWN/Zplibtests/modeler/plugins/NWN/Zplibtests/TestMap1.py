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
        return [
            # naked object map with no relations will set property on device by default
            ObjectMap({
                'title':  'test_device',
                'setManageIp': '44.44.44.44', 
                'setProductKey': MultiArgs('FakeOS v1 SP1', 'FakeOSManufaturer'), }  
            ),
            RelationshipMap(
                modname="ZenPacks.NWN.Zplibtests.SubClass1",   # this sucks easier on larger zenacks to import the modeule and get the name
                relname="subClass1s",                          # this again sucks better go have a class method to get the primary containing rel name
                objmaps=[ObjectMap({'id': self.prepId('subComponent-1'),
                                    'title': 'subComponent-1',
                                    'set_subClass2s': map(self.prepId, ['subComponent-2', ])
                                    })]),
            RelationshipMap(
                modname="ZenPacks.NWN.Zplibtests.SubClass2",
                relname="subClass2s",
                objmaps=[ObjectMap({'id': self.prepId('subComponent-2'),
                                    'title': 'subComponent-2',
                                    'set_subClass3s': map(self.prepId, ['subComponent-3', ])
                                    })]),
            RelationshipMap(
                modname="ZenPacks.NWN.Zplibtests.SubClass3",
                relname="subClass3s",
                objmaps=[ObjectMap({'id': self.prepId('subComponent-3'),
                                    'title': 'subComponent-3'
                                    })]),
        ]

    def process(self, device, results, log):
        """"""

        log.info('processing {} for {}: {}'.format(self.__class__.__name__, device.id, results))
        return results