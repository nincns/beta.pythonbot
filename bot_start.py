from bot_scanning import MoveServoX, CamScan
import sys


def bot_selfcheck(): 
    print("start self check")
    MoveServoX.start()

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
    ["01 start self check", bot_selfcheck],
    ["02 discover terrain", discover_terrain],
    ["03 start measurement areal dimension", discover_dimension],
    ["04 find noise", find_noise],
]

handle_menu(menu)