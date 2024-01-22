#!/usr/bin/env python3

import time
import RPi.GPIO as GPIO

BUTTON_GPIO = 16


class ResetController:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(BUTTON_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        pressed = False

    def run(self):
        while True:
            if not GPIO.input(BUTTON_GPIO):
                if not pressed:
                    print("Button pressed!")
                    pressed = True
                    return True
            else:
                pressed = False
            time.sleep(0.1)
