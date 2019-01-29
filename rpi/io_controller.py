import numpy as np
import gpiozero as gpio

pins = {}


def setup(AIN1, AIN2, PWMA,
          BIN1, BIN2, PWMB,
          STBY):
    if not pins:
        pins['AIN1'] = gpio.DigitalOutputDevice(AIN1)
        pins['AIN2'] = gpio.DigitalOutputDevice(AIN2)
        pins['PWMA'] = gpio.PWMOutputDevice(PWMA)
        pins['BIN1'] = gpio.DigitalOutputDevice(BIN1)
        pins['BIN2'] = gpio.DigitalOutputDevice(BIN2)
        pins['PWMB'] = gpio.PWMOutputDevice(PWMB)
        pins['STBY'] = gpio.DigitalOutputDevice(STBY)

        # pins['ground-front-left'] = gpio.SmoothedInputDevice(GD_FL)


def get_motor_pins(motor):
    if motor not in ('a', 'b'):
        raise ValueError('motor should be in ("a", "b")!')

    in1, in2, pwm = ((pins['AIN1'], pins['AIN2'], pins['PWMA'])
                     if motor == 'a' else
                     (pins['BIN1'], pins['BIN2'], pins['PWMB']))
    return in1, in2, pwm


def set_motor_speed(motor, speed):
    speed = np.clip(speed, -1, 1)

    pins['STBY'].on()

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
