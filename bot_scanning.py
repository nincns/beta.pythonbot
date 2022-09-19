from time import sleep
from pitop import ServoMotor, ServoMotorSetting
from pitop import UltrasonicSensor
from pitop import Button
from pitop import SoundSensor
from pitop import LightSensor
from pitop import Camera
from threading import Thread
import time

servo_x = ServoMotor("S0")
servo_y = ServoMotor("S1")
ultrasonic_phalanx = UltrasonicSensor("D3")
ultrasonic_front = UltrasonicSensor("D2")
button = Button("D1")
sound_sensor = SoundSensor("A0")
light_sensor = LightSensor("A1")
cam = Camera()

servo_settings = ServoMotorSetting()
servo_settings.speed = 50

servo_x.target_angle = 0
servo_y.target_angle = 0

class MoveServoX(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.running = True
    def run(self):
        servo_x.target_angle = 0
        scandirection = "left"
        while self.running: #running process 1
         if servo_x.current_angle < 90 and scandirection == "left":
            print("left ",servo_x.current_angle, "distance ", round(ultrasonic_phalanx.distance.real, 2), "noise ", sound_sensor.reading, "light ", light_sensor.reading)
            servo_x.target_angle = servo_x.current_angle + 1
         elif servo_x.current_angle == 90:
            scandirection = "right"
         if servo_x.current_angle > -90 and scandirection == "right":
            print("right ",servo_x.current_angle, "distance ", round(ultrasonic_phalanx.distance.real, 2), "noise ", sound_sensor.reading, "light ", light_sensor.reading)
            servo_x.target_angle = servo_x.current_angle - 1
         elif servo_x.current_angle == -90:
            scandirection = "left"
         sleep(0.1)
    def stop(self):
        self.running = False

class Scan(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.running = True
    def run(self):
        while self.running: #running process 2
            time_now = time.strftime("%Y%m%d-%H%M%S")
            if round(ultrasonic_front.distance.real, 2) < 0.5:
                servo_x.target_angle = 0
                servo_y.target_angle = 25
                sleep(2)
                image = cam.get_frame()
                image.save("pictures/pitop_"+time_now+".jpg")
                servo_y.target_angle = 0
                sleep(2)
                process1.start()
            time.sleep(1)
    def stop(self):
        self.running = False

process1 = MoveServoX()
process2 = Scan()

process1.start()
process2.start()
