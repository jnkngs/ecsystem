import unittest
from lib.entity import Entity, Component
from lib.entitymanager import EntityManager
from lib.systemmanager import System, SystemManager


class SampleSystem(System):
    def __init__(self):
        self._time = None

    @property
    def time(self):
        # this property is used to store the entity id - bad naming 
        return self._time

    @time.setter
    def time(self, time):
        self._time = time

    def update(self, entitymanager, tick):
        entitymanager.set_component_value(self.time, self.name, tick)

class TestSystemManager(unittest.TestCase):
    def test_add_system_with_different_priorities(self):
        systemmanager = SystemManager()
        system1 = System()
        system2 = System()
        systemmanager.add_system(system1, 1)
        systemmanager.add_system(system2, 2)

        self.assertEqual(systemmanager.number_of_systems, 2)

    def test_add_systems_with_same_priorities(self):
        # systemmanager should accept same system only once
        systemmanager = SystemManager()
        system1 = System()
        system2 = System()
        systemmanager.add_system(system1, 1)
        systemmanager.add_system(system2, 1)    # <-- NOTE!

        self.assertEqual(systemmanager.number_of_systems, 1)
        self.assertEqual(systemmanager.systems[0], system1)

    def test_system_priority_order(self):
        systemmanager = SystemManager()
        system1 = System()
        system2 = System()
        system3 = System()
        systemmanager.add_system(system2, 2)
        systemmanager.add_system(system1, 1)
        systemmanager.add_system(system3, 3)

        self.assertEqual(systemmanager.systems[0], system1)
        self.assertEqual(systemmanager.systems[1], system2)
        self.assertEqual(systemmanager.systems[2], system3)

    def test_remove_system(self):
        systemmanager = SystemManager()
        system1 = System()
        system2 = System()
        system3 = System()
        systemmanager.add_system(system2, 2)
        systemmanager.add_system(system1, 1)
        systemmanager.add_system(system3, 3)

        systemmanager.remove_system(system2)
        self.assertEqual(systemmanager.systems[0], system1)
        self.assertEqual(systemmanager.systems[1], system3)

    def test_update_systems(self):
        # This acts more of an integration test as entities
        # are also linked to test case. See TestSystem class at the
        # top of the file for more info.

        # sample systems
        system1 = SampleSystem()
        system1.name = 'Test1'

        system2 = SampleSystem()
        system2.name = 'Test2'
        
        system3 = SampleSystem()
        system3.name = 'Test3'

        # entity manager for data storing and sample components
        entitymanager = EntityManager()
        component1 = Component('Test1', 0)
        component2 = Component('Test2', 0)
        component3 = Component('Test3', 0)

        entity = entitymanager.create_entity()
        # store entity id to systems
        system1.time = entity.id    # We have to store entity ids somewhere so system
        system2.time = entity.id    # is able to use them in each update loop. Id is 
        system3.time = entity.id    # is needed for accessing entities and components
        entitymanager.add_component_to_entity(entity, component1)
        entitymanager.add_component_to_entity(entity, component2)
        entitymanager.add_component_to_entity(entity, component3)
        
        systemmanager = SystemManager()

        systemmanager.add_system(system1, 1)
        systemmanager.add_system(system2, 2)
        systemmanager.add_system(system3, 3)

        # this will act as our sample game loop
        for i in range(1,4):
            systemmanager.update_systems(entitymanager, i)

        # Assert that components updated by SampleSystems are really updated during 
        # the "game" loop
        self.assertEqual(entitymanager.get_component_value(entity.id, system1.name), 3)
        self.assertEqual(entitymanager.get_component_value(entity.id, system2.name), 3)
        self.assertEqual(entitymanager.get_component_value(entity.id, system3.name), 3)

if __name__ == '__main__':
    unittest.main()
