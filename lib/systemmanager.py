class DuplicateSystemError(Exception):
    pass

class System(object):
    def __init__(self):
        self._name = None
        self._priority = None
        self._systemmanager = None

    @property
    def priority(self):
        return self._priority

    @property
    def name(self):
        return self._name

    @name.setter 
    def name(self, name):
        self._name = name

    @priority.setter
    def priority(self, priority):
        self._priority = priority

    @property
    def systemmanager(self):
        return self._systemmanager

    @systemmanager.setter
    def systemmanager(self, systemmanager):
        self._systemmanager = systemmanager


    def update(self, entitymanager, tick):
        raise NotImplementedError

class SystemManager(object):

    def __init__(self):
        self._systems = []

    @property
    def number_of_systems(self):
        return len(self._systems)

    @property
    def systems(self):
        return self._systems

    def add_system(self, system, priority):
        for s in self._systems:
            if s == system:
                raise DuplicateSystemError
            if priority == s.priority:
                return

        system.priority = priority
        system.systemmanager = self
        self._systems.append(system)
        self._systems.sort(key=lambda x: x.priority)

    def remove_system(self, system):
        for s in self._systems:
            if s is system:
                self._systems.remove(s)
                return

    def update_systems(self, entitymanager, tick):
        for system in self._systems:
            try:
                system.update(entitymanager, tick)
            except Exception as err:
                print('{} system crashed with {}'.format(self.name, err))
