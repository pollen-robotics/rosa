import json

import motors_controller as controller

from SimpleWebSocketServer import WebSocket, SimpleWebSocketServer

verbose = True


class WsMotorHandler(WebSocket):
    def handleMessage(self):
        cmd = json.loads(self.data)

        if verbose:
            print('Got cmd: {}'.format(cmd))

        if 'setup' in cmd:
            controller.setup(**cmd['setup'])
            if verbose:
                print('Setup with', cmd['setup'])

        if 'wheels' in cmd:
            wheels = cmd['wheels']

            for m in ('a', 'b'):
                if m in wheels:
                    s = wheels[m]
                    controller.set_speed(m, s)
                    if verbose:
                        print('Set motor {} speed to {}'.format(m, s))

    def handleClose(self):
        for m in ('a', 'b'):
            controller.set_speed(m, 0)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--verbose', action='store_true')
    args = parser.parse_args()

    server = SimpleWebSocketServer('', 1234, WsMotorHandler)

    if args.verbose:
        print('Server up and running.')

    server.serveforever()
