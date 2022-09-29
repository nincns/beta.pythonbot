from pitop import LED

from threading import Thread
import time

led_left = LED("D1")
led_right = LED("D6")

class check_process1(Thread):
    def __init__(self):
        Thread.__init__(self)
    def start(self):

        led_left.on()
        if led_left.is_active is True:
            print("LED left ok")
        elif led_left.is_active is False:
            print("LED left not ok")
            led_left.off()

        led_right.on()
        if led_right.is_active is True:
            print("LED right ok")
        elif led_right.is_active is False:
            print("LED right not ok")
        led_right.off()

LED_check = check_process1()

