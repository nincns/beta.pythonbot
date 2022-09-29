# Import modules
from time import sleep
from pitop import ServoMotor, ServoMotorSetting
from pitop import UltrasonicSensor
from pitop import Button
from pitop import LightSensor
from pitop import SoundSensor
from pitop import Buzzer
from pitop import BrakingType, EncoderMotor, ForwardDirection
from pitop import LED
from pitop import Camera
from pitop.miniscreen import Miniscreen
from signal import pause
import time
import math

# Setup the devices
servo_x = ServoMotor("S2")
servo_y = ServoMotor("S3")
button = Button("D1")
light_sensor = LightSensor("A1")
sound_sensor = SoundSensor("A3")
buzzer = Buzzer("D0")
motor_right = EncoderMotor("M0", ForwardDirection.COUNTER_CLOCKWISE)
motor_left = EncoderMotor("M3", ForwardDirection.CLOCKWISE)
cam = Camera()
ultrasonic_front = UltrasonicSensor("D4")
ultrasonic_phalanx = UltrasonicSensor("D5")
miniscreen = Miniscreen()

motor_right.breaking_type = BrakingType.COAST
motor_left.breaking_type = BrakingType.COAST

#sets servo speed and direction

turnspeed = 0.1
drivespeed = 0.2

drive_wheel_circumfence = 50
chain_width = 45
chain_base = 120

target_degrees = 180
target_rotations = math.pi * (chain_base + chain_width) * target_degrees / 360 / drive_wheel_circumfence
print ("target rotations: ", target_rotations)

left_rotation_counter = motor_left.rotation_counter
right_rotation_counter = motor_right.rotation_counter

motor_right.backward(target_speed=turnspeed)
motor_left.forward(target_speed=turnspeed)
#miniscreen.display_multiline_text('doing a ' + str(target_degrees), font_size=14)

while True:
    #start programm
    
    if button.is_pressed is True:
        exit()

    if motor_left.rotation_counter - left_rotation_counter > target_rotations or motor_right.rotation_counter - right_rotation_counter > -target_rotations:
        motor_right.stop()
        motor_left.stop()
        miniscreen.display_multiline_text('done turning', font_size=14)
        print ("rotations left: ", motor_left.rotation_counter - left_rotation_counter)
        print ("rotations right: ", motor_right.rotation_counter - right_rotation_counter)
        exit()

    sleep(0.05)