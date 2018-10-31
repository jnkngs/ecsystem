import unittest
from lib.entity import Entity, Component
from lib.entitymanager import EntityManager


class TestEntityManager(unittest.TestCase):
    def test_create_entity(self):
        # should create new entity with unique identifier
        entitymanager = EntityManager()
        hp = Component('hitpoints', 15)
        dmg = Component(type='damage', value='2d4')
        e1 = entitymanager.create_entity()

        entitymanager.add_component_to_entity(e1, hp)
        entitymanager.add_component_to_entity(e1, dmg)

        hp2 = Component(type='hitpoints', value=10)
        e2 = entitymanager.create_entity()
        entitymanager.add_component_to_entity(e2, hp2)

        self.assertTrue(e1.id != e2.id)

        self.assertEqual(e1.hitpoints, 15)
        e1.hitpoints = 8
        self.assertEqual(e1.hitpoints, 8)
        self.assertEqual(e2.hitpoints, 10)
        self.assertEqual(entitymanager.entity_count, 2)

    def test_entitymanager_data_manipulation(self):
        entitymanager = EntityManager()
        hp = Component('hitpoints', 10)
        entity = entitymanager.create_entity()
        entitymanager.add_component_to_entity(entity, hp)

        hp = None
        id = entity.id
        entity = None

        entitymanager.set_component_value(id, 'hitpoints', 8)

        self.assertEqual(entitymanager.get_component_value(id, 'hitpoints'), 8)

    def test_remove_component_from_entity(self):
        entitymanager = EntityManager()
        self.assertEqual(entitymanager.entity_count, 0)
        hp = Component('hitpoints', 15)
        ench = Component('enchanted', True)
        e1 = entitymanager.create_entity()
        e2 = entitymanager.create_entity()

        entitymanager.add_component_to_entity(e1, hp)
        entitymanager.add_component_to_entity(e1, ench)
        entitymanager.add_component_to_entity(e2, hp)

        entitymanager.remove_component(e1, 'enchanted')

        db = entitymanager.database
        with self.assertRaises(KeyError) as cm:
            db['enchanted'][e1.id]

    def test_get_all_entities_with_component_name(self):
        # should get all the entities with certain component name
        entitymanager = EntityManager()
        self.assertEqual(entitymanager.entity_count, 0)
        hp = Component('hitpoints', 15)
        ench = Component('enchanted', True)
        e1 = entitymanager.create_entity()
        e2 = entitymanager.create_entity()

        entitymanager.add_component_to_entity(e1, hp)
        entitymanager.add_component_to_entity(e2, hp)

        entitymanager.add_component_to_entity(e1, ench)
        entitymanager.add_component_to_entity(e2, ench)

        enchanted = entitymanager.entities_by_type(ench.type)
        enchanted.sort(key=lambda x: x.id)
        should_be_enchanted = sorted([e1, e2], key=lambda x: x.id)
        for i in range(2):
            self.assertEqual(enchanted[i], should_be_enchanted[i])
        # Test that we can access components for fetched entity
        enchanted[0].hitpoints -= 10
        db = entitymanager.database
        self.assertEqual(db['hitpoints'][enchanted[0].id], 5)

    def test_remove_entity(self):
        entitymanager = EntityManager()
        hp = Component('hitpoints', 1)
        e1 = entitymanager.create_entity()
        entitymanager.add_component_to_entity(e1, hp)
        self.assertEqual(entitymanager.entity_count, 1)

        entitymanager.remove_entity(e1.id)
        self.assertEqual(entitymanager.entity_count, 0)

        self.assertEqual(entitymanager.get_component_value(e1.id, 'hitpoints'), None)


if __name__ == '__main__':
    unittest.main()
