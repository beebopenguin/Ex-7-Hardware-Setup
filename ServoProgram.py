from pidev.Cyprus_Commands import Cyprus_Commands_RPi as cyprus
from time import sleep
import numpy as np

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
cyprus.set_servo_speed(2, 0)
sleep(1)


def step1():

    while 1:
        if (cyprus.read_gpio() & 0b0001):
            cyprus.set_servo_position(1, 0)
            sleep(1)
        else:
            cyprus.set_servo_position(1, .5)
            sleep(1)


def step2():

    cyprus.set_servo_speed(2, 1)
    sleep(5)
    cyprus.set_servo_speed(2, 0)
    sleep(5)
    cyprus.set_servo_speed(2, -1)
    sleep(5)
    cyprus.set_servo_speed(2, 0)


def step2a():

    for i in np.arange(0, 1.2, 0.2):
        cyprus.set_servo_speed(2, i)
        print(i)
        sleep(4)
    cyprus.set_servo_speed(2, 0)


def step2b():
    while 1:

        if (cyprus.read_gpio() & 0b0001):
            cyprus.set_servo_speed(2, 0)
            sleep(0.05)
        else:
            cyprus.set_servo_position(2, 1)
            sleep(0.05)


def step3():
    cyprus.set_pwm_values(2, period_value=100000, compare_value=50000, compare_mode=cyprus.LESS_THAN_OR_EQUAL)
    sleep(5)
    cyprus.set_pwm_values(2, period_value=100000, compare_value=0, compare_mode=cyprus.LESS_THAN_OR_EQUAL)
    sleep(5)
    cyprus.set_pwm_values(2, period_value=100000, compare_value=50000, compare_mode=cyprus.LESS_THAN_OR_EQUAL)
    sleep(5)
    cyprus.set_pwm_values(2, period_value=100000, compare_value=0, compare_mode=cyprus.LESS_THAN_OR_EQUAL)


def step3a():
    while 1:

        if (cyprus.read_gpio() & 0b0001):
            cyprus.set_pwm_values(2, period_value=100000, compare_value=0, compare_mode=cyprus.LESS_THAN_OR_EQUAL)
            print("HIGH")
        else:
            cyprus.set_pwm_values(2, period_value=100000, compare_value=50000, compare_mode=cyprus.LESS_THAN_OR_EQUAL)
            print("LOW")
