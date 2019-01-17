from .wheel import Wheel
from .remote_io import RemoteIO


class Rosa(object):
    def __init__(self, host):
        self._io = RemoteIO(host)

        self._left_wheel = Wheel(id='a', remote_io=self._io)
        self.right_wheel = Wheel(id='b', remote_io=self._io, inverse=True)

    @property
    def left_wheel(self):
        return self._left_wheel

    @property
    def right_wheel(self):
        return self._right_wheel
