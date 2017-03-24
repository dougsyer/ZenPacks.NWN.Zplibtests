"""
test modeler doc string test aded to this docscring will show up in modeller plugin selection in gui
TIP:  if you have any doubt that you could get bad data in a relationship map, just raise an error
or return None...returning empty data in valid Relationship Maps can remove your relations....bad!
"""

from Products.DataCollector.plugins.CollectorPlugin import PythonPlugin
from Products.DataCollector.plugins.DataMaps import (
    ObjectMap,
    RelationshipMap,
    MultiArgs
)


class TestMap1(PythonPlugin):
    """"Return dummy output for modeler demo"""

    def _prepIdStuff(component_id_or_ids, toMany=True):
        """
        prepID and purposely crash modeller if you try to pass a string if you send a string as ToMany
        I cant tell you how many times ive tried to pass a string into a to-many rel setter in the past...ugh
        """

        if toMany and isinstance(component_id_or_ids, basestring):
            # this wont give you what device is failing model but you will see it in the event, just keeping it simple..
            raise Exception('tried to pass base string into toMany relationship setter')

        return [self.prepId(_id) for _id in component_id_or_ids] if toMany else self.prepId(component_id_or_ids)

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

        modeled_data = [
            {
                'title': 'test-device'
                '_type': 'device',  # if you pass a dict into an OM directly, _attributes will be ignored
                '_os_make_model': ['FakeOS v1 SP1', 'FakeOSManufaturer'],
                # this will call setManageIP method on the device, if you have a method you need to mirror
                # a set... and get... method so that the  modeler can determin if the value has changed
                'setManageIp':  '44.44.44.44',  # is a valid method on device so will be set ...but o
            },

            {
                'title': 'subComponent-1',
                '_type': 'SubClass1'
                '_connected_SC2s': ['subComponent-2'],
            },

            {
                'title': 'subComponent-2',
                '_type': 'subClass1'
                '_connected_SC3s': ['subComponent-2'],
            },


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

        rms = [
            RelationshipMap(
                modname="ZenPacks.NWN.Zplibtests.SubClass1",
                relname="subClass1s",
                objmaps=[
                    ObjectMap({
                        'id': _prepIdStuff('subComponent-1', toMany=False),
                        'title': 'subComponent-1',
                        'set_subClass2s': _prepIdStuff(['subComponent-2', ]),
                    })
                ]
            ),
            RelationshipMap(
                modname="ZenPacks.NWN.Zplibtests.SubClass2",
                relname="subClass2s",
                objmaps=[
                    ObjectMap({
                        'id': self.prepId('subComponent-2'),
                        'title': 'subComponent-2',
                        'set_subClass3s': _prepIdStuff ['subComponent-3', ]),
                        'set_subClass4s': _prepIdStuff(['subComponent-4', ]})
                ]
            ),
            RelationshipMap(
                modname="ZenPacks.NWN.Zplibtests.SubClass3",
                relname="subClass3s",
                objmaps=[
                    ObjectMap({
                        'id': self.prepId('subComponent-3'),
                        'title': 'subComponent-3'})
                ]
            ),
            RelationshipMap(
                modname="ZenPacks.NWN.Zplibtests.SubClass4",
                relname="subClass4s",
                objmaps=[
                    ObjectMap({
                        'id': self.prepId('subComponent-4'),
                        'title': 'subComponent-4'})
                ]
            ),
        ]

        # if you need python debugger...
        import pdb; pdb.set_trace()
        results = rms.append(dev_om)

        return results


    def process(self, device, results, log):
        """
        after collllect runs preprocess then process
        note if you have a really simple modeller you can set relname, compname and modname
        as variables as class attributes and doing that you can avoid some of the complexity
        of defining relmaps/object maps.  but...i prefer just to consistently create
        OMS and RM objects in my modellers to avoid confusion

        """

        log.info('processing {} for {}: {}'.format(self.__class__.__name__, device.id, results))


        return results
