from distutils.command.sdist import sdist
from matplotlib.pyplot import pause
from pitop import LED
from pitop import Buzzer
from pitop import ServoMotor, ServoMotorSetting
from pitop import UltrasonicSensor

from threading import Thread
import time

led_left = LED("D0")
led_right = LED("D6")
buzzer = Buzzer("D2")
servo_x = ServoMotor("S3")
servo_y = ServoMotor("S0")
ultrasonic_front = UltrasonicSensor("D3")
ultrasonic_head = UltrasonicSensor("D5")


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
        servo_x.target_angle=0
        servo_y.target_angle=0
        servo_x.target_speed=50
        servo_y.target_speed=50
        servo_x.smooth_acceleration=True
        servo_y.smooth_acceleration=True
        servo_x.sweep()
        servo_y.sweep()
        servo_x.target_angle=-90
        servo_y.target_angle=-90
        pause(3)
        print("Servo lowest position ok")
        servo_x.target_angle=90
        servo_y.target_angle=90
        pause(6)
        print("Servo highest position ok")
        servo_x.target_angle=0
        servo_y.target_angle=0
        pause(3)

class check_process4(Thread):
    def __init__(self):
        Thread.__init__(self)
    def start(self):
        if round(float(ultrasonic_front.distance)) > 0:
            print("Ultrasonic front ok")
        elif (float(ultrasonic_front.distance)) < 0.1:
            print("Ultrasonic front failed")
        if (float(ultrasonic_head.distance)) > 0:
            print("Ultrasonic head ok")
        elif (float(ultrasonic_head.distance)) < 0.1:
            print("Ultrasonic head failed")


LED_check = check_process1()
Buzzer_check = check_process2()
Servo_check = check_process3()
Ultrasonic_check = check_process4()
