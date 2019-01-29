class Distance(object):
    def __init__(self, name, remote_io):
        self._name = name
        self._io = remote_io

    @property
    def distance(self):
        return self._io.last_state['distance'][self._name]

    @property
    def color(self):
        return self._io.last_state['color'][self._name]
