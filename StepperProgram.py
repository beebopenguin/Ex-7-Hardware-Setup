from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty

import spidev
import os
from time import sleep
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
            s0.softStop()
            self.startMotorButton.text = "START"
            print("stop motor")

        else:
            s0.run(d, s)
            self.startMotorButton.text = "STOP"
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


Builder.load_file('StepperProgram.kv')


SCREEN_MANAGER.add_widget(MainScreen(name=MAIN_SCREEN_NAME))


if __name__ == "__main__":

    StepperProgramGUI().run()


