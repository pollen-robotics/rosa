class Wheel(object):
    def __init__(self, id, remote_io, inverse=False, init_speed=0.0):
        self.id = id
        self._io = remote_io

        self._speed = init_speed
        self._inverse = inverse

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, new_speed):
        self._speed = new_speed
        self._io.set_speed(self.id,
                           -self.speed if self._inverse else self.speed)
