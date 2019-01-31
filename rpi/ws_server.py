import json
import time

import cv2 as cv

from PIL import Image
from io import BytesIO
from threading import Thread
from collections import deque

from SimpleWebSocketServer import WebSocket, SimpleWebSocketServer


import io_controller as io
from line_tracking import get_line_center


verbose = True
use_cam = [False]
line_center = [None]


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

        if use_cam[0]:
            state['line-center'] = line_center[0]

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

        if 'camera' in cmd and cmd['camera']:
            use_cam[0] = True

    def handleClose(self):
        for m in ('a', 'b'):
            io.set_motor_speed(m, 0)

        self._send_loop_running = False
        self._sender.join()

        use_cam[0] = False


ws = deque([], 1)
buff = deque([], 1)


def grab_frame_loop():
    cap = cv.VideoCapture(0)

    while True:
        if not use_cam[0] and not len(ws):
            time.sleep(0.1)
            continue

        b, img = cap.read()
        if not b:
            continue

        with BytesIO() as bytes:
            pil_img = Image.fromarray(img)
            pil_img.save(bytes, 'jpeg')
            buff.append(bytes.getvalue())

        if use_cam[0]:
            center = get_line_center(img)
            if center is not None:
                center = (center[0] / img.shape[1],
                          center[1] / img.shape[0])
            line_center[0] = center


def publish_loop():
    while True:
        if len(ws) and len(buff):
            ws[0].sendMessage(buff.pop())

        time.sleep(1.0 / 20)


class WsCamServer(WebSocket):
    def handleConnected(self):
        ws.append(self)

    def handleClose(self):
        ws.remove(self)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--verbose', action='store_true')
    args = parser.parse_args()

    io_server = SimpleWebSocketServer('', 1234, WsIOHandler)
    cam_server = SimpleWebSocketServer('', 5678, WsCamServer)

    if args.verbose:
        print('Server up and running.')

    video_loop = Thread(target=grab_frame_loop)
    video_loop.daemon = True
    video_loop.start()

    publish_t = Thread(target=publish_loop)
    publish_t.daemon = True
    publish_t.start()

    servers = [
        Thread(target=server.serveforever)
        for server in (io_server, cam_server)
    ]
    for server in servers:
        server.start()

    for server in servers:
        server.join()
