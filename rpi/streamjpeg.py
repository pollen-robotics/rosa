import cv2
import time

from collections import deque
from io import BytesIO
from threading import Thread

from PIL import Image
from SimpleWebSocketServer import WebSocket, SimpleWebSocketServer


ws = deque([], 1)
buff = deque([], 1)


def grab_frame_loop():
    cap = cv2.VideoCapture(0)

    while True:
        b, img = cap.read()
        if not b:
            continue

        with BytesIO() as bytes:
            pil_img = Image.fromarray(img)
            pil_img.save(bytes, 'jpeg')
            buff.append(bytes.getvalue())


def publish_loop():
    while True:
        if len(ws) and len(buff):
            ws[0].sendMessage(buff.pop())

        time.sleep(1 / 20)


class WsServer(WebSocket):
    def handleConnected(self):
        ws.append(self)

    def handleClose(self):
        ws.remove(self)


video_loop = Thread(target=grab_frame_loop)
video_loop.daemon = True
video_loop.start()

publish_t = Thread(target=publish_loop)
publish_t.daemon = True
publish_t.start()

server = SimpleWebSocketServer('', 5678, WsServer)
server.serveforever()
