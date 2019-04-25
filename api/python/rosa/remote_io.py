import json
import websocket as ws

from threading import Thread, Event


class RemoteIO(object):
    def __init__(self, host):
        url = 'ws://{}:1234'.format(host)
        self.ws = ws.create_connection(url)

        self.last_state = {}

        self._poll_t = Thread(target=self._update_state)
        self._poll_t.daemon = True
        self._poll_t.start()

        self._synced = Event()
        self._synced.wait()

    def set_speed(self, motor, speed):
        self.ws.send(json.dumps({
            'wheels': {
                motor: speed
            }
        }))

    def set_led(self, led, val):
        self.ws.send(json.dumps({
            'leds': {
                led: val
            }
        }))

    def buzz(self, duration):
        self.ws.send(json.dumps({'buzz': duration}))

    def _update_state(self):
        while True:
            self.last_state.update(json.loads(self.ws.recv()))
            self._synced.set()
