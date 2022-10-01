#!/usr/local/bin/python
from selfcheck import LED_check, Buzzer_check, LightSensor_check, Servo_check, Ultrasonic_check, LightSensor_check, SoundSensor_check
import sys


def bot_selfcheck(): 
    print("start self check")
    LED_check.start()
    Buzzer_check.start()
    Servo_check.start()
    Ultrasonic_check.start()
    LightSensor_check.start()
    SoundSensor_check.start()

def discover_terrain(): 
    print("discover terrain")

def discover_dimension(): 
    print("start measurement areal dimension")

def find_noise(): 
    print("find noise")

def handle_menu(menu):
    while True:
        for index, item in enumerate(menu, 1):
            print("{}  {}".format(index, item[0]))
        choice = int(input("start programm? ")) - 1
        if 0 <= choice < len(menu):
            menu[choice][1]()
        else:
            print("only numbers between 1 - {} ".format(
                                                                    len(menu)))

menu = [
    ["start self check", bot_selfcheck],
    ["discover terrain", discover_terrain],
    ["start measurement areal dimension", discover_dimension],
    ["find noise", find_noise],
]

handle_menu(menu)