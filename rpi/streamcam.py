import asyncio

import cv2
import websockets

RES = (176, 144)

cam = cv2.VideoCapture(0)


@asyncio.coroutine
def videostream(websocket, path):
    while True:
        success, img = cam.read()
        if success:
            img = cv2.resize(img, RES)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            yield from websocket.send(img.tobytes())


start_server = websockets.serve(videostream, '0.0.0.0', 5678)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
