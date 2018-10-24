import json
import asyncio
import websockets

FREQ = 25
PERIOD = 1.0 / FREQ


@asyncio.coroutine
def scratchext(websocket, path):
    while True:
        state = json.dumps(get_current_state())
        yield from websocket.send(state)

        cmd = yield from websocket.recv()
        handle_commands(json.loads(cmd))

        yield from asyncio.sleep(PERIOD)


def get_current_state():
    import numpy as np

    return {
        'light_sensor': {
            'left': [0, 0, 0, np.random.randint(100)],
            'right': [20, 20, 20, np.random.randint(200)],
        }
    }


def handle_commands(cmd):
    if 'wheels' in cmd:
        wheels = cmd['wheels']

        if 'left' in wheels:
            left_speed = wheels['left']
            print('Set left wheel speed to {}'.format(left_speed))

        if 'right' in wheels:
            right_speed = wheels['right']
            print('Set right wheel speed to {}'.format(right_speed))


start_server = websockets.serve(scratchext, '0.0.0.0', 1234)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
