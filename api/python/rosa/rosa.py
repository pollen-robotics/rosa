import numpy as np

from .led import LED
from .wheel import Wheel
from .remote_io import RemoteIO
from .remote_cam import Camera


class Rosa(object):
    def __init__(self, host):
        self._io = RemoteIO(host)

        self._left_wheel = Wheel(id='b', remote_io=self._io, inverse=True)
        self._right_wheel = Wheel(id='a', remote_io=self._io)

        self._cam = Camera(host)

        self._left_led = LED(side='left', remote_io=self._io)
        self._right_led = LED(side='right', remote_io=self._io)

    @property
    def left_wheel(self):
        return self._left_wheel

    @property
    def right_wheel(self):
        return self._right_wheel

    @property
    def left_led(self):
        return self._left_led

    @property
    def right_led(self):
        return self._right_led

    @property
    def camera(self):
        return self._cam

    @property
    def front_distance_sensors(self):
        return ['front-left', 'front-center', 'front-right']

    def get_front_distances(self):
        return np.array([self.get_distance(name) for name in self.front_distance_sensors])

    @property
    def ground_distance_sensors(self):
        return [
            'ground-front-left', 'ground-front-right',
            'ground-rear-left', 'ground-rear-right',
        ]

    def get_ground_distances(self):
        return np.array([self.get_distance(name) for name in self.ground_distance_sensors])

    @property
    def distance_sensors(self):
        return self.front_distance_sensors + self.ground_distance_sensors

    def get_distance(self, sensor):
        if sensor not in self.distance_sensors:
            raise ValueError('sensor should be one of {}!'.format(self.distance_sensors))

        return self._io.last_state['distance'][sensor]

    def buzz(self, duration):
        self._io.buzz(duration)
