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
             steps_per_unit=200, speed=8)

SCREEN_MANAGER = ScreenManager()
MAIN_SCREEN_NAME = 'main'


class StepperProgramGUI(App):

    def build(self):

        return SCREEN_MANAGER


Window.clearcolor = (1, 1, 1, 1)  # White


class MainScreen(Screen):

    def set_direction(self, direction, speed):
        global d
        global s
        self.d = direction
        self.s = speed

    def change_speed(self):
            self.startMotor()


    def startMotor(self):
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


    def startMotor2(self, direction):
        global d
        d = direction

        s0.run(d, s)

    def changeDirection(self):

        if self.set_direction().d == 1:
            self.set_direction().d = 0
        else:
            self.set_direction().d = 1

  #      if self.startMotorButton.text == "STOP":
  #          print("change direction")
  #          s0.softStop()
  #          if d == 1:
  #              self.startMotor2(0)
  #          else:
  #              self.startMotor2(1)



Builder.load_file('StepperProgram.kv')


SCREEN_MANAGER.add_widget(MainScreen(name=MAIN_SCREEN_NAME))


if __name__ == "__main__":

    StepperProgramGUI().run()


