from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty, Clock
from kivy.clock import CyClockBase
import threading
from threading import Thread

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

SCREEN_MANAGER = ScreenManager()
MAIN_SCREEN_NAME = 'main'


class StepperProgramGUI(App):

    def build(self):

        return SCREEN_MANAGER


Window.clearcolor = (1, 1, 1, 1)  # White


class MainScreen(Screen):

    def change_speed(self):
        self.slider_start_motor()

    def start_motor(self):
        global d
        global s
        d = 1
        s = self.slider.value
        if self.spinButton.state == "normal":
            if self.startMotorButton.text == "STOP":
                s0.softFree()
                self.startMotorButton.text = "START"
                self.startMotorButton.background_color = (1, 2, 0, 1)
                print("stop motor")

            else:
                s0.run(d, s)
                self.startMotorButton.text = "STOP"
                self.startMotorButton.background_color = (1, 0, 0, 1)
                print("start motor")
        else:
            pass

    def slider_start_motor(self):
        global d
        global s
        s = self.slider.value

        if self.startMotorButton.text == "STOP":
            s0.run(d, s)
        else:
           pass

    def direction_start_motor(self, direction):

        global d
        d = direction

        s0.run(d, s)

    def change_direction(self):
        global d

        if self.startMotorButton.text == "STOP":
            print("change direction")
            s0.softStop()
            sleep(0.1)
            if d == 1:
                self.direction_start_motor(0)
            else:
                self.direction_start_motor(1)

#//////////////////spin program functions////////////////////////#

    def change_variable(self, rotations, speed):
        global r
        global s2
        r = rotations
        s2 = speed
        print("change var, r: "+ str(r) + " " + "s2: " + str(s2))

    def move_motor(self, dt):
        global r
        global s2
        print("move motor" + str(r) + str(s2))
        s0.set_speed(s2)
        s0.start_relative_move(r)

    def go_home(self, dt):
        s0.goHome() #should be 5s

    def go_home2(self, dt):
        s0.goHome()
        Clock.schedule_once(self.change_color_normal, 20)

    def get_position(self, dt):
        self.positionLabel.text = str(s0.get_position_in_units())

    def change_color_normal(self, dt):
        self.spinButton.state = "normal"
        self.startMotorButton.disabled = False
        self.directionButton.disabled = False
        self.slider.disabled = False

    def spin_program(self):

        if self.spinButton.state == "down":
            self.startMotorButton.disabled = True
            self.directionButton.disabled = True
            self.slider.disabled = True
            s0.stop()
            s0.set_as_home()
            self.positionLabel.text = str(s0.get_position_in_units())
            #time: 0s, spin 15s
            Clock.schedule_once(lambda dt: self.change_variable(15, 1), 0)
            Clock.schedule_once(self.move_motor, 0)
            Clock.schedule_once(self.get_position, 15)
            #time 15s, wait 10s, spin 2s
            Clock.schedule_once(lambda dt: self.change_variable(10, 5), 25)
            Clock.schedule_once(self.move_motor, 25)
            Clock.schedule_once(self.get_position, 27.5)
            #time 27s, wait 8s, spin 5s
            Clock.schedule_once(self.go_home, 35)
            Clock.schedule_once(self.get_position, 40.5)
            #time 40s, wait 30s, spin 20s
            Clock.schedule_once(lambda dt: self.change_variable(-100, 5), 70)
            Clock.schedule_once(self.move_motor, 70)
            Clock.schedule_once(self.get_position, 90.5)
            #time 90s, wait 10s, spin 20s
            Clock.schedule_once(self.go_home2, 100)
            Clock.schedule_once(self.get_position, 120.5)
            #time 2 min.
        else:
            s0.stop()
            Clock.unschedule(self.move_motor)
            Clock.unschedule(self.change_variable)
            Clock.unschedule(self.get_position)
            Clock.unschedule(self.go_home)
            Clock.unschedule(self.go_home2)
            self.startMotorButton.disabled = False
            self.directionButton.disabled = False
            self.slider.disabled = False


Builder.load_file('StepperProgram.kv')


SCREEN_MANAGER.add_widget(MainScreen(name=MAIN_SCREEN_NAME))


if __name__ == "__main__":

    StepperProgramGUI().run()


