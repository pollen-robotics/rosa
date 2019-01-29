from .wheel import Wheel
from .ground import Ground
from .distance import Distance
from .remote_io import RemoteIO
from .remote_cam import Camera


class Rosa(object):
    def __init__(self, host):
        self._io = RemoteIO(host)

        self._left_wheel = Wheel(id='b', remote_io=self._io, inverse=True)
        self._right_wheel = Wheel(id='a', remote_io=self._io)

        self._front_left_ground = Ground('front-left', remote_io=self._io)
        self._front_right_ground = Ground('front-right', remote_io=self._io)
        self._rear_left_ground = Ground('rear-left', remote_io=self._io)
        self._rear_right_ground = Ground('rear-right', remote_io=self._io)

        self._front_left_sensor = Distance('front-left', remote_io=self._io)
        self._front_center_sensor = Distance('front-center', remote_io=self._io)
        self._front_right_sensor = Distance('front-right', remote_io=self._io)

        self._cam = Camera(host)

    @property
    def left_wheel(self):
        return self._left_wheel

    @property
    def right_wheel(self):
        return self._right_wheel

    @property
    def front_left_ground(self):
        return self._front_left_ground

    @property
    def front_right_ground(self):
        return self._front_right_ground

    @property
    def rear_left_ground(self):
        return self._rear_left_ground

    @property
    def rear_right_ground(self):
        return self._rear_right_ground

    @property
    def front_left_sensor(self):
        return self._front_left_sensor

    @property
    def front_center_sensor(self):
        return self._front_center_sensor

    @property
    def front_right_sensor(self):
        return self._front_right_sensor

    @property
    def camera(self):
        return self._cam
