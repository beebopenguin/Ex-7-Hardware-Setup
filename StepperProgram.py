from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty, Clock
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

    def change_text(self): #function to display start position 0.0 after press & release spin program button
        if self.startMotorButton.text == "START":
            s0.set_as_home()
            self.positionLabel.text = str(s0.get_position_in_units())
            print("cahnge")

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
        s0.relative_move(r)
        self.positionLabel.text = str(s0.get_position_in_units())

    def go_home(self, dt):
        s0.goHome() #should be 5s
        Clock.schedule_once(self.get_position, 5.5)

    def go_home2(self, dt):
        s0.goHome()
        Clock.schedule_once(self.get_position, 20)
        Clock.schedule_once(self.change_color_normal, 20)

    def get_position(self, dt):
        self.positionLabel.text = str(s0.get_position_in_units())

    def change_color_normal(self, dt):
        self.spinButton.background_color = (1, 1, 1, 1)

    def spin_program(self):
        if self.startMotorButton.text == "START":
            self.spinButton.background_color = (1, 1, 3, 1)
            #time: 0s, spin 15s
            Clock.schedule_once(lambda dt: self.change_variable(15, 1), 0)
            Clock.schedule_once(self.move_motor, 0)
            #time 15s, wait 10s, spin 2s
            Clock.schedule_once(lambda dt: self.change_variable(10, 5), 25)
            Clock.schedule_once(self.move_motor, 25)
            #time 27s, wait 8s, spin 5s
            Clock.schedule_once(self.go_home, 35)
            #time 40s, wait 30s, spin 20s
            Clock.schedule_once(lambda dt: self.change_variable(-100, 5), 70)
            Clock.schedule_once(self.move_motor, 70)
            #time 90s, wait 10s
            Clock.schedule_once(self.go_home2, 100)
            #time 2 min.

    spin_program_thread = Thread(target = spin_program)


Builder.load_file('StepperProgram.kv')


SCREEN_MANAGER.add_widget(MainScreen(name=MAIN_SCREEN_NAME))


if __name__ == "__main__":

    StepperProgramGUI().run()


