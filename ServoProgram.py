from pidev.Cyprus_Commands import Cyprus_Commands_RPi as cyprus
from time import sleep

import spidev
import os
from time import sleep
from threading import Timer
import RPi.GPIO as GPIO
from pidev.stepper import stepper
from Slush.Devices import L6470Registers
spi = spidev.SpiDev()

s0 = stepper(port=0, micro_steps=32, hold_current=20, run_current=20, accel_current=20, deaccel_current=20,
             steps_per_unit=200, speed=5)

cyprus.initialize()
cyprus.setup_servo(1)

while 1:
    if (cyprus.read_gpio() & 0b0001):
        cyprus.set_servo_position(1, 0)
        sleep(1)
    else:
        cyprus.set_servo_position(1, .5)
        sleep(1)

cyprus.setup_servo(2)
sleep(1)
cyprus.set_servo_speed(2, 0)
sleep(3)
cyprus.close()