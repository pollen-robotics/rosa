import serial
import websocket


class Serial(object):
    def __init__(self, port, baudrate):
        self.s = serial.Serial(port=port, baudrate=baudrate)

    def send(self, msg):
        self.s.write('{}\n'.format(msg))

    def read(self):
        return self.s.readline()


class Ws(object):
    def __init__(self, url):
        self.ws = websocket.create_connection(url)

    def send(self, msg):
        self.ws.send(msg)

    def read(self):
        return self.ws.recv()
