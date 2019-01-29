import json

import io_controller as io

from SimpleWebSocketServer import WebSocket, SimpleWebSocketServer

verbose = True


class WsMotorHandler(WebSocket):
    def handleMessage(self):
        cmd = json.loads(self.data)

        if verbose:
            print('Got cmd: {}'.format(cmd))

        if 'setup' in cmd:
            io.setup(**cmd['setup'])
            if verbose:
                print('Setup with', cmd['setup'])

        if 'wheels' in cmd:
            wheels = cmd['wheels']

            for m in ('a', 'b'):
                if m in wheels:
                    s = wheels[m]
                    io.set_motor_speed(m, s)
                    if verbose:
                        print('Set motor {} speed to {}'.format(m, s))

    def handleClose(self):
        for m in ('a', 'b'):
            io.set_motor_speed(m, 0)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--verbose', action='store_true')
    args = parser.parse_args()

    server = SimpleWebSocketServer('', 1234, WsMotorHandler)

    if args.verbose:
        print('Server up and running.')

    server.serveforever()
