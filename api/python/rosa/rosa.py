from .wheel import Wheel
from .remote_io import RemoteIO
from .remote_cam import Camera


class Rosa(object):
    def __init__(self, host):
        self._io = RemoteIO(host)

        self._left_wheel = Wheel(id='a', remote_io=self._io)
        self._right_wheel = Wheel(id='b', remote_io=self._io, inverse=True)

        self._cam = Camera(host)

    @property
    def left_wheel(self):
        return self._left_wheel

    @property
    def right_wheel(self):
        return self._right_wheel

    @property
    def camera(self):
        return self._cam
