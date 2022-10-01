from time import sleep
from pitop import ServoMotor, ServoMotorSetting
from pitop import UltrasonicSensor
from pitop import Button
from pitop import SoundSensor
from pitop import LightSensor
from pitop import Camera
from pitop import BrakingType, EncoderMotor, ForwardDirection
from pitop import LED
from threading import Thread
import time

servo_pan = ServoMotor("S0")
servo_tilt = ServoMotor("S3")
ultrasonic_front = UltrasonicSensor("D3")
ultrasonic_head = UltrasonicSensor("D4")

button = Button("D1")
sound_sensor = SoundSensor("A3")
light_sensor = LightSensor("A1")
cam = Camera()

motor_right = EncoderMotor("M0", ForwardDirection.COUNTER_CLOCKWISE)
motor_left = EncoderMotor("M3", ForwardDirection.CLOCKWISE)

led_left = LED("D0")
led_right = LED("D7")

motor_right.breaking_type = BrakingType.COAST
motor_left.breaking_type = BrakingType.COAST

turnspeed = 0.1
drivespeed = 0.1

servo_settings = ServoMotorSetting()
servo_settings.speed = 50

servo_pan.target_angle = 0
servo_tilt.target_angle = 20

class process1(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.running = True
        self.move = True

    def run(self):
        scandirection = "left"
        pan_distance = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18,]
        while self.running: #running process 1
         if servo_pan.current_angle < 90 and scandirection == "left" and self.move is True: #Servo will try start scanning in right direction
            print(servo_pan.current_angle, "distance ", round(ultrasonic_head.distance.real, 2), "noise ", sound_sensor.reading, "light ", light_sensor.reading)
            if servo_pan.current_angle <= 80: #error handling when something interupt process and angle will not 10, 20 or something will execpt with error servo can not set to 90+ degree same for left direction
                servo_pan.target_angle = servo_pan.current_angle + 10
            elif servo_pan.current_angle >= 81:
                servo_pan.target_angle = 90
         elif servo_pan.current_angle == 90:
            scandirection = "right"
         if servo_pan.current_angle > -90 and scandirection == "right" and self.move is True:
            print(servo_pan.current_angle, "distance ", round(ultrasonic_head.distance.real, 2), "noise ", sound_sensor.reading, "light ", light_sensor.reading)
            if servo_pan.current_angle >= -80:
                servo_pan.target_angle = servo_pan.current_angle - 10
            elif servo_pan.current_angle <= -81:
                servo_pan.target_angle = -90
         elif servo_pan.current_angle == -90:
            scandirection = "left"
         sleep(0.25)
        
         if servo_pan.current_angle <= 0:
            i = int((servo_pan.current_angle*-1)/10)
            pan_distance[i] = servo_pan.current_angle, round(ultrasonic_head.distance.real, 2), sound_sensor.reading, light_sensor.reading
         elif servo_pan.current_angle == 10:
            i = 10
            pan_distance[i] = servo_pan.current_angle, round(ultrasonic_head.distance.real, 2), sound_sensor.reading, light_sensor.reading
         elif servo_pan.current_angle > 10:
            i = int(servo_pan.current_angle/10+9)
            pan_distance[i] = servo_pan.current_angle, round(ultrasonic_head.distance.real, 2), sound_sensor.reading, light_sensor.reading
         print(pan_distance)

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
                MovePiTop.pause()
                MoveServoX.pause()
                servo_pan.target_angle = 0
                servo_tilt.target_angle = 0
                sleep(2)
                image = cam.get_frame()
                image.save("pictures/pitop_"+time_now+".jpg")
                servo_tilt.target_angle = 20
                sleep(2)
                MoveServoX.resume()
                MovePiTop.analyse()
            time.sleep(1)
    def stop(self):
        self.running = False
    def pause(self):
        self.scan = False
    def resume(self):
        self.scan = True

class process3(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.running = True
        self.turnforward = True
        self.turnleft = False
        self.turnright = False

    def run(self):
        while self.running: #running process 3
            if self.turnforward is True:
                motor_right.forward(target_speed=drivespeed)
                motor_left.forward(target_speed=drivespeed)
            elif self.turnforward is False:
                motor_right.stop()
                motor_left.stop()

            sleep(1)

    def stop(self):
        self.running = False
    def pause(self):
        self.turnforward = False
    def resume(self):
        self.turnforward = True
    def left(self):
        self.turnleft = True
    def right(self):
        self.turnforward = True
    def analyse(self):
        print("analyse moving direction")

class process4(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.running = True
    def run(self):
        while self.running:
            led_left.on()
            sleep(0.5)
            led_left.off()
            led_right.on()
            sleep(0.5)
            led_right.off()
    def stop(self):
        self.running = False

MoveServoX = process1()
CamScan = process2()
MovePiTop = process3()
YellowBeacon = process4()

MovePiTop.start()
MoveServoX.start()
CamScan.start()
YellowBeacon.start()