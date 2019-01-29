class Ground(object):
    def __init__(self, name, remote_io):
        self._name = name
        self._io = remote_io

    @property
    def distance(self):
        return self._io.last_state['ground'][self._name]
