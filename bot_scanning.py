from time import sleep
from pitop import ServoMotor, ServoMotorSetting
from pitop import UltrasonicSensor
from pitop import Button
from pitop import SoundSensor
from pitop import LightSensor
from pitop import Camera
from threading import Thread
import time

servo_x = ServoMotor("S2")
servo_y = ServoMotor("S3")
ultrasonic_phalanx = UltrasonicSensor("D7")
ultrasonic_front = UltrasonicSensor("D2")
button = Button("D1")
sound_sensor = SoundSensor("A3")
light_sensor = LightSensor("A2")
cam = Camera()

servo_settings = ServoMotorSetting()
servo_settings.speed = 50

servo_x.target_angle = 0
servo_y.target_angle = -25

class process1(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.running = True
        self.move = True
    def run(self):
        scandirection = "left"
        while self.running: #running process 1
         if servo_x.current_angle < 90 and scandirection == "left" and self.move is True: #Servo will try start scanning in right direction
            print("left ",servo_x.current_angle, "distance ", round(ultrasonic_phalanx.distance.real, 2), "noise ", sound_sensor.reading, "light ", light_sensor.reading)
            if servo_x.current_angle <= 80: #error handling when something interupt process and angle will not 10, 20 or something will execpt with error servo can not set to 90+ degree same for left direction
                servo_x.target_angle = servo_x.current_angle + 10
            elif servo_x.current_angle >= 81:
                servo_x.target_angle = 90
         elif servo_x.current_angle == 90:
            scandirection = "right"
         if servo_x.current_angle > -90 and scandirection == "right" and self.move is True:
            print("right ",servo_x.current_angle, "distance ", round(ultrasonic_phalanx.distance.real, 2), "noise ", sound_sensor.reading, "light ", light_sensor.reading)
            if servo_x.current_angle >= -80:
                servo_x.target_angle = servo_x.current_angle - 10
            elif servo_x.current_angle <= -81:
                servo_x.target_angle = -90
         elif servo_x.current_angle == -90:
            scandirection = "left"
         sleep(0.5)
    def stop(self):
        self.running = False
    def pause(self):
        self.move = False
    def resume(self):
        self.move = True

class process2(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.running = True
        self.scan = True
    def run(self):
        while self.running: #running process 2
            time_now = time.strftime("%Y%m%d-%H%M%S")
            if round(ultrasonic_front.distance.real, 2) < 0.5 and self.scan is True:
                MoveServoX.pause()
                servo_x.target_angle = 0
                servo_y.target_angle = 0
                sleep(2)
                image = cam.get_frame()
                image.save("pictures/pitop_"+time_now+".jpg")
                servo_y.target_angle = -25
                sleep(2)
                MoveServoX.resume()
            time.sleep(1)
    def stop(self):
        self.running = False
    def pause(self):
        self.scan = False
    def resume(self):
        self.scan = True

MoveServoX = process1()
CamScan = process2()