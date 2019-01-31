import json
import time

from threading import Thread

import io_controller as io

from SimpleWebSocketServer import WebSocket, SimpleWebSocketServer

verbose = True


class WsIOHandler(WebSocket):
    pub_period = 1.0 / 60.0

    def handleConnected(self):
        io.setup(AIN1=18, AIN2=17, PWMA=4,
                 BIN1=24, BIN2=27, PWMB=22,
                 STBY=23)

        self._send_loop_running = True

        def _send_loop():
            while self._send_loop_running:
                self.sendState()
                time.sleep(WsIOHandler.pub_period)

        self._sender = Thread(target=_send_loop)
        self._sender.start()

    # TODO: qu'est-ce qui declenche l'envoie du state ?
    #
    # Timer ?
    # REQ/REP ?
    #
    # Problematique : eviter les lags/buffer overflow en cas de latence reseau

    def sendState(self):
        state = {
            'ground': {
                sensor: io.get_ground(sensor)
                for sensor in ('front-left', 'front-right', 'rear-left', 'rear-right')
            },
            'color': {
                sensor: io.get_color(sensor)
                for sensor in ('front-left', 'front-center', 'front-right')
            },
            'distance': {
                sensor: io.get_dist(sensor)
                for sensor in ('front-left', 'front-center', 'front-right')
            }
        }

        self.sendMessage(json.dumps(state))

    def handleMessage(self):
        cmd = json.loads(self.data)

        if verbose:
            print('Got cmd: {}'.format(cmd))

        if 'wheels' in cmd:
            wheels = cmd['wheels']

            for m in ('a', 'b'):
                if m in wheels:
                    s = wheels[m]
                    io.set_motor_speed(m, s)
                    if verbose:
                        print('Set motor {} speed to {}'.format(m, s))

        if 'buzz' in cmd:
            duration = cmd['buzz']
            io.buzz(duration)

    def handleClose(self):
        for m in ('a', 'b'):
            io.set_motor_speed(m, 0)

        self._send_loop_running = False
        self._sender.join()


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--verbose', action='store_true')
    args = parser.parse_args()

    server = SimpleWebSocketServer('', 1234, WsIOHandler)

    if args.verbose:
        print('Server up and running.')

    server.serveforever()
