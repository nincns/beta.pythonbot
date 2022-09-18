# Import modules
from time import sleep
from pitop import ServoMotor
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

# Setup the devices
servo_x = ServoMotor("S0")
servo_y = ServoMotor("S1")
button = Button("D1")
light_sensor = LightSensor("A1")
sound_sensor = SoundSensor("A2")
buzzer = Buzzer("D0")
motor_right = EncoderMotor("M0", ForwardDirection.COUNTER_CLOCKWISE)
motor_left = EncoderMotor("M3", ForwardDirection.CLOCKWISE)
cam = Camera()

motor_right.breaking_type = BrakingType.COAST
motor_left.breaking_type = BrakingType.COAST

ultrasonic_front = UltrasonicSensor("D3", threshold_distance=0.75)
ultrasonic_rear = UltrasonicSensor("D2", threshold_distance=0.75)

miniscreen = Miniscreen()

#sets servo speed and direction
global sp
sp = 100

turnspeed = 0.1
drivespeed = 0.05
servo_x.sweep(sp)
servo_x.sweep(-sp)

servo_x.target_angle = 0
servo_y.target_angle = 0

while True:
    #start programm
    servo_y.target_angle = 25
    
    if button.is_pressed is True:
        exit()
         
    time_now = time.strftime("%Y%m%d-%H%M%S")

    if float(ultrasonic_front.distance) > 0.5: #inital distance check
        miniscreen.display_multiline_text('drive forward', font_size=14)
        motor_right.forward(target_speed=drivespeed)
        motor_left.forward(target_speed=drivespeed)

    elif float(ultrasonic_front.distance) < 0.5: #find obstacle on the way
         miniscreen.display_multiline_text('check distance', font_size=14)
         motor_right.stop()
         motor_left.stop()

         servo_x.target_angle = 0
         servo_y.target_angle = -35
         sleep(2)
         image = cam.get_frame()
         image.save("pictures/pitop_"+time_now+".jpg")
         sleep(2)
         servo_y.target_angle = 25

         servo_x.target_angle = -45
         sleep(4)
         distance_left = float(ultrasonic_front.distance)
         servo_x.target_angle = 45
         sleep(8)
         distance_right = float(ultrasonic_front.distance)
         servo_x.target_angle = 0

         if distance_left < 0.5 and distance_right < 0.5: #drive backward and tank turn
            miniscreen.display_multiline_text('U - turn', font_size=14)
            motor_right.backward(target_speed=drivespeed)
            motor_left.backward(target_speed=drivespeed)
            sleep(1.5)
            motor_right.backward(target_speed=turnspeed)
            motor_left.forward(target_speed=turnspeed)
            sleep(1.5)

         elif distance_left > distance_right:
            miniscreen.display_multiline_text('drive left', font_size=14)
            motor_left.forward(target_speed=turnspeed)
        
         elif distance_left < distance_right:
            miniscreen.display_multiline_text('drive right', font_size=14)
            motor_right.forward(target_speed=turnspeed)
        
         sleep(2)
    sleep(1)