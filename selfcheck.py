#!/usr/local/bin/python
from distutils.command.sdist import sdist
from matplotlib.pyplot import pause
from pitop import LED
from pitop import Buzzer
from pitop import ServoMotor
from pitop import UltrasonicSensor
from pitop import LightSensor
from pitop import SoundSensor

from threading import Thread
import time

led_left = LED("D0")
led_right = LED("D7")
buzzer = Buzzer("D5")
servo_pan = ServoMotor("S0")
servo_tilt = ServoMotor("S3")
ultrasonic_front = UltrasonicSensor("D3")
ultrasonic_head = UltrasonicSensor("D4")
light_sensor = LightSensor("A1")
soundsensor = SoundSensor("A3")


class check_process1(Thread):
    def __init__(self):
        Thread.__init__(self)
    def start(self):

        led_left.on()
        pause(1)
        if led_left.is_active is True:
            print("LED left ok")
        elif led_left.is_active is False:
            print("LED left not ok")
        led_left.off()

        led_right.on()
        pause(1)
        if led_right.is_active is True:
            print("LED right ok")
        elif led_right.is_active is False:
            print("LED right not ok")
        led_right.off()

class check_process2(Thread):
    def __init__(self):
        Thread.__init__(self)
    def start(self):

        buzzer.on()
        pause(1)
        if buzzer.is_active is True:
            print("Buzzer ok")
        elif buzzer.is_active is False:
            print("Buzzer not ok")
        buzzer.off()

class check_process3(Thread):
    def __init__(self):
        Thread.__init__(self)
    def start(self):
        servo_pan.target_angle=0
        servo_tilt.target_angle=0
        servo_pan.target_speed=50
        servo_tilt.target_speed=50
        servo_pan.smooth_acceleration=True
        servo_tilt.smooth_acceleration=True
        servo_pan.sweep()
        servo_tilt.sweep()
        servo_pan.target_angle=-90
        servo_tilt.target_angle=90
        pause(3)
        print("Servo lowest position ok")
        servo_pan.target_angle=90
        servo_tilt.target_angle=-90
        pause(6)
        print("Servo highest position ok")
        servo_pan.target_angle=0
        servo_tilt.target_angle=0
        pause(3)

class check_process4(Thread):
    def __init__(self):
        Thread.__init__(self)
    def start(self):
        if (round(ultrasonic_front.distance)) > 0:
            print("Ultrasonic front ok")
        elif (round(ultrasonic_front.distance)) < 0.1:
            print("Ultrasonic front failed")
        if (round(ultrasonic_head.distance)) > 0:
            print("Ultrasonic head ok")
        elif (round(ultrasonic_head.distance)) < 0.1:
            print("Ultrasonic head failed")

class check_process5(Thread):
    def __init__(self):
        Thread.__init__(self)
    def start(self):
        print("Lightsensor: ", light_sensor.reading)

class check_process6(Thread):
    def __init__(self):
        Thread.__init__(self)
    def start(self):
        if soundsensor.value == 1:  
            print("SoundSensor ok")
        elif soundsensor.value != 1:
            print("SoundSensor failed")

LED_check = check_process1()
Buzzer_check = check_process2()
Servo_check = check_process3()
Ultrasonic_check = check_process4()
LightSensor_check = check_process5()
SoundSensor_check = check_process6()

LED_check.start()
Buzzer_check.start()
Servo_check.start()
Ultrasonic_check.start()
LightSensor_check.start()
SoundSensor_check.start()