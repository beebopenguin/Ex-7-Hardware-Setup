from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty, Clock


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

    def change_text(self, dt):
        self.positionLabel.text = str(s0.get_position_in_units())
        print("cahnge")

    def move_motor(self, dt):
        global r
        global s2
        print(str(s2))
        s0.set_speed(s2)
        s0.relative_move(r)
        self.positionLabel.text = str(s0.get_position_in_units())


    def spin_program(self):
        global r
        global s2
   #     self.positionLabel.text = str(s0.get_position_in_units()) #this doesn't work when sleep function is added in or when s0.start_relative_move is changed to s0.relative_move
        print("spin 15")
        s2 = 1
        r = 5
        Clock.schedule_once(self.move_motor, 0)

        print("wait 10s, spin 10")

        s2 = 5
        r = 10
        Clock.schedule_once(self.move_motor, 10)








    def notes(self):
        # spin program


        print("wait 8s, go home, wait 30s")
        sleep(8)
        s0.goHome()  #s0.goHome() is a non-blocking command (blocking commands can't do commands like get position or stop while it's running)
        sleep(30)
        self.positionLabel.text = str(s0.get_position_in_units())

        print("spin opposite 100")
        s0.set_speed(8)
        s0.relative_move(-100)
        self.positionLabel.text = str(s0.get_position_in_units())

        print("wait 10s, go home")
        sleep(10)
        s0.goHome()
        self.positionLabel.text = str(s0.get_position_in_units())

        s0.free()



Builder.load_file('StepperProgram.kv')


SCREEN_MANAGER.add_widget(MainScreen(name=MAIN_SCREEN_NAME))


if __name__ == "__main__":

    StepperProgramGUI().run()


