from collections import namedtuple


Component = namedtuple('Component', 'type value')


class Entity(dict):
    def __init__(self, id, entitymanager):
        self['id'] = id
        self['type'] = 'entity'
        self['entitymanager'] = entitymanager

    def __getattr__(self, name):
        try:
            if name == 'id':
                return self['id']
            elif name == 'type':
                return self['type']
            else:
                return self['entitymanager'].get_component_value(self['id'], name)
        except:
            raise AttributeError("Entity.get: no such component - {}".format(name))

    def __setattr__(self, name, value):
        self['entitymanager'].set_component_value(self['id'], name, value)

    def __delattr__(self, name):
        if name in self:
            del self[name]
        else:
            raise AttributeError("Entity.del: no such component - {}".format(name))

