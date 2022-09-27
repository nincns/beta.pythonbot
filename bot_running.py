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

# Setup the devices
servo_x = ServoMotor("S2")
servo_y = ServoMotor("S3")
button = Button("D1")
light_sensor = LightSensor("A1")
sound_sensor = SoundSensor("A3")
buzzer = Buzzer("D0")
motor_right = EncoderMotor("M2", ForwardDirection.COUNTER_CLOCKWISE)
motor_left = EncoderMotor("M1", ForwardDirection.CLOCKWISE)
cam = Camera()
ultrasonic_front = UltrasonicSensor("D4")
ultrasonic_phalanx = UltrasonicSensor("D5")
miniscreen = Miniscreen()

motor_right.breaking_type = BrakingType.COAST
motor_left.breaking_type = BrakingType.COAST

#sets servo speed and direction

turnspeed = 0.1
drivespeed = 0.05

servo_x.target_angle = 0
servo_y.target_angle = 0

while True:
    #start programm
    servo_y.target_angle = 35
    
    if button.is_pressed is True:
        exit()
         
    time_now = time.strftime("%Y%m%d-%H%M%S")

    if round(ultrasonic_front.distance, 2) > 0.75: #inital distance check
        print ("distance front: ", round(ultrasonic_front.distance.real, 2))
        miniscreen.display_multiline_text('drive forward', font_size=14)
        motor_right.forward(target_speed=drivespeed)
        motor_left.forward(target_speed=drivespeed)

    elif round(ultrasonic_front.distance, 2) < 0.75: #find obstacle on the way
         miniscreen.display_multiline_text('check distance', font_size=14)
         motor_right.stop()
         motor_left.stop()

         servo_x.target_angle = 0
         servo_y.target_angle = -25
         sleep(2)
         miniscreen.display_multiline_text('take a photo', font_size=14)
         image = cam.get_frame()
         image.save("pictures/pitop_"+time_now+".jpg")
         sleep(2)
         servo_y.target_angle = 35

         servo_x.target_angle = -45
         sleep(4)
         distance_left = round(ultrasonic_phalanx.distance.real, 2)
         print ("distance right: ", distance_left)
         servo_x.target_angle = 45
         sleep(8)
         distance_right = round(ultrasonic_phalanx.distance.real, 2)
         print("distance left: ", distance_right)
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
            miniscreen.display_multiline_text('drive right', font_size=14)
            motor_left.forward(target_speed=turnspeed)
        
         elif distance_left < distance_right:
            miniscreen.display_multiline_text('drive left', font_size=14)
            motor_right.forward(target_speed=turnspeed)
        
         sleep(2)
    sleep(1)