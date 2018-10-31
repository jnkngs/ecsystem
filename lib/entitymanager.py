"""
Created 26.1.2017 by Jani Kangas(jnkngs@gmail.com)
"""
import random

from entity import Entity


class EntityManager(object):
    _database = {}

    def __init__(self):
        self._database = {}

    def _create_id(self):
        return int(random.random() * 10000000)

    @property
    def database(self):
        return self._database

    @property
    def entity_count(self):
        entities = {}
        for component in self._database.keys():
            for entity_id in self._database[component].keys():
                try:
                    entities[entity_id] += 1
                except KeyError:
                    entities[entity_id] = 1

        return len(entities)

    def create_entity(self):
        id = self._create_id()
        return Entity(id, self)

    def add_component_to_entity(self, entity, component):
        try:
            self._database[component.type][entity.id] = component.value
        except KeyError:
            self._database[component.type] = {}
            if component.type is not 'entity':
                self._database[component.type][entity.id] = component.value
            else:
                self._database[component.type][entity.id] = None
        except AttributeError:
            if component.type is not 'entity':
                self._database[component.type][entity.id] = component.value
            else:
                if component.type not in self._database:
                    self._database[component.type] = {}
                self._database[component.type][entity.id] = None

    def get_component_value(self, entity_id, component_type):
        try:
            return self._database[component_type][entity_id]
        except KeyError:
            return None

    def set_component_value(self, entity_id, component_type, component_value):
        try:
            self._database[component_type][entity_id] = component_value
        except KeyError:
            pass

    def remove_component(self, entity, component_name):
        del self._database[component_name][entity.id]

    def entities_by_type(self, component_type):
        entities = []
        for ent_id in self._database[component_type]:
            entities.append(Entity(ent_id, self))
        return entities

    def remove_entity(self, entity_id):
        for component in self._database:
            if self._database[component][entity_id]:
                del self._database[component][entity_id]
