from rosa import Rosa


rosa = Rosa.from_serial('/dev/tty.SLAB_USBtoUART')

while True:
    if rosa.light_sensors['left'] < 10:
        rosa.motors['right'] = 100
    else:
        rosa.motors['right'] = 0

    if rosa.light_sensors['right'] < 10:
        rosa.motors['left'] = 100
    else:
        rosa.motors['left'] = 0
