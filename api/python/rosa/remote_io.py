import json
import websocket as ws

from threading import Thread


class RemoteIO(object):
    def __init__(self, host):
        url = 'ws://{}:1234'.format(host)
        self.ws = ws.create_connection(url)

        self.last_state = {}

        self._poll_t = Thread(target=self._update_state)
        self._poll_t.daemon = True
        self._poll_t.start()

    def set_speed(self, motor, speed):
        self.ws.send(json.dumps({
            'wheels': {
                motor: speed
            }
        }))

    def buzz(self, duration):
        self.ws.send(json.dumps({'buzz': duration}))

    def _update_state(self):
        while True:
            self.last_state.update(json.loads(self.ws.recv()))
