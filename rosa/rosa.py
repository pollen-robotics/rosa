import json

from threading import Thread

from io import Serial, Ws


class Rosa(object):
    @classmethod
    def from_ws(cls, ip):
        return cls(io=Ws('ws://{}:81'.format(ip)))

    @classmethod
    def from_serial(cls, port):
        return cls(io=Serial(port, baudrate=115200))

    def __init__(self, io):
        self.io = io
        self.light_sensors = {'left': 0, 'right': 0}
        self.motors = {'left': 0, 'right': 0}

        _bg_sync = Thread(target=self._sync_loop)
        _bg_sync.daemon = True
        _bg_sync.start()

    def _sync_loop(self):
        while True:
            self._poll_sensors()
            self._push_motors_cmd()

    def _poll_sensors(self):
        try:
            state = self._read()

            _, _, _, left = state['light_sensor']['left']
            _, _, _, right = state['light_sensor']['right']

            self.light_sensors.update(
                left=left,
                right=right
            )

        except ValueError:
            pass

    def _push_motors_cmd(self):
        cmd = {
            'wheels': {'left': self.motors['left'], 'right': self.motors['right']}
        }
        self._send(cmd)


    def _send(self, msg):
        msg = json.dumps(msg)
        self.io.send(msg)

    def _read(self):
        state = self.io.read()
        state = json.loads(state)
        return state
