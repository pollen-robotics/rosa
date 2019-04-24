import numpy as np
import gpiozero as gpio

pins = {}


###########################
# Motor related functions #
###########################

motor_pins = {
    'AIN1': gpio.DigitalOutputDevice(27),
    'AIN2': gpio.DigitalOutputDevice(23),
    'PWMA': gpio.PWMOutputDevice(22),
    'BIN1': gpio.DigitalOutputDevice(17),
    'BIN2': gpio.DigitalOutputDevice(15),
    'PWMB': gpio.PWMOutputDevice(14),
    'STBY': gpio.DigitalOutputDevice(18),
}


def get_motor_pins(motor):
    if motor not in ('a', 'b'):
        raise ValueError('motor should be in ("a", "b")!')

    in1, in2, pwm = ((motor_pins['AIN1'], motor_pins['AIN2'], motor_pins['PWMA'])
                     if motor == 'a' else
                     (motor_pins['BIN1'], motor_pins['BIN2'], motor_pins['PWMB']))
    return in1, in2, pwm


def set_motor_speed(motor, speed):
    speed = np.clip(speed, -1, 1)

    motor_pins['STBY'].on()

    in1, in2, pwm = get_motor_pins(motor)

    if speed < 0:
        in1.off()
        in2.on()
    else:
        in1.on()
        in2.off()

    pwm.value = abs(speed)


def motor_short_brake(motor):
    in1, in2, _ = get_motor_pins(motor)
    in1.on()
    in2.on()


def buzz(duration):
    # TODO: impl.
    print('BUUUUUUUUZZZZZ for', duration, 's')
    # pins['buzzer'].beep(on_time=duration, n=1)
    pass


def get_ground(sensor):
    # TODO: impl.
    # return pins['ground-{}'.format(sensor)].value()
    return np.random.rand()


def get_color(sensor):
    # TODO: impl.
    return (np.random.rand(), np.random.rand(), np.random.rand())


def get_dist(sensor):
    # TODO: impl.
    return np.random.rand()
