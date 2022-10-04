from time import sleep
from turtle import distance
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

#device & sensor settings
ultrasonic_front = UltrasonicSensor("D3")
ultrasonic_head = UltrasonicSensor("D4")
#button = Button("D1") not used actually
sound_sensor = SoundSensor("A3")
light_sensor = LightSensor("A1")
cam = Camera()
led_left = LED("D0")
led_right = LED("D7")
#motor settings
motor_right = EncoderMotor("M0", ForwardDirection.COUNTER_CLOCKWISE)
motor_left = EncoderMotor("M3", ForwardDirection.CLOCKWISE)
motor_right.breaking_type = BrakingType.COAST
motor_left.breaking_type = BrakingType.COAST
motor_right.wheel_diameter=0.05
motor_left.wheel_diameter=0.05
#drive settings input
turnspeed = input("set turnspeed (0.2-1.0): ")
turnspeed = float(turnspeed)
drivespeed = input("set basis drivespeed (0.2-1.0): ")
drivespeed = float(drivespeed)
#servo settings
servo_pan = ServoMotor("S0")
servo_tilt = ServoMotor("S3")
servo_settings = ServoMotorSetting()
servo_settings.speed = 50
#set servo default position
servo_pan.target_angle = 0
servo_tilt.target_angle = 20
#set default array for head ultrasonic maesurements from -90, -80.... 0, 10, 20.... 90 (19valuess)
pan_maesure  = [(0, 0, 0, 0)] * 19
degree = [0] * 19 
range  = [0] * 19 
noise  = [0] * 19 
light  = [0] * 19 
#input drive logic
drive_logic = input("please type programm number (1 = discover terrain, 2 = find noise, 3 = find light): ")
drive_logic = int(drive_logic)

class process1(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.running = True
        self.move = True

    def run(self):
        scandirection = "left"
        while self.running: #running process 1
         if servo_pan.current_angle < 90 and scandirection == "left" and self.move is True: #Servo will try start scanning in right direction
            #print(servo_pan.current_angle, "distance ", round(ultrasonic_head.distance.real, 2), "noise ", sound_sensor.reading, "light ", light_sensor.reading)
            if servo_pan.current_angle <= 80: #error handling when something interupt process and angle will not 10, 20 or something will execpt with error servo can not set to 90+ degree same for left direction
                #add Ultrasonic distance value to pan_distance array
                if servo_pan.current_angle <= 0:
                    i = int((servo_pan.current_angle*-1)/10)
                    pan_maesure[i] = servo_pan.current_angle, round(ultrasonic_head.distance.real, 2), sound_sensor.reading, light_sensor.reading
                elif servo_pan.current_angle == 10:
                    i = 10
                    pan_maesure[i] = servo_pan.current_angle, round(ultrasonic_head.distance.real, 2), sound_sensor.reading, light_sensor.reading
                elif servo_pan.current_angle > 10:
                    i = int(servo_pan.current_angle/10+9)
                pan_maesure[i] = servo_pan.current_angle, round(ultrasonic_head.distance.real, 2), sound_sensor.reading, light_sensor.reading
                #change current angle of servo for next measurement 
                servo_pan.target_angle = servo_pan.current_angle + 10
            elif servo_pan.current_angle >= 81:
                servo_pan.target_angle = 90
         elif servo_pan.current_angle == 90:
            scandirection = "right"
         if servo_pan.current_angle > -90 and scandirection == "right" and self.move is True:
            #print(servo_pan.current_angle, "distance ", round(ultrasonic_head.distance.real, 2), "noise ", sound_sensor.reading, "light ", light_sensor.reading)
            if servo_pan.current_angle >= -80:
                #add Ultrasonic distance value to pan_distance array
                if servo_pan.current_angle <= 0:
                    i = int((servo_pan.current_angle*-1)/10)
                    pan_maesure[i] = servo_pan.current_angle, round(ultrasonic_head.distance.real, 2), sound_sensor.reading, light_sensor.reading
                elif servo_pan.current_angle == 10:
                    i = 10
                    pan_maesure[i] = servo_pan.current_angle, round(ultrasonic_head.distance.real, 2), sound_sensor.reading, light_sensor.reading
                elif servo_pan.current_angle > 10:
                    i = int(servo_pan.current_angle/10+9)
                pan_maesure[i] = servo_pan.current_angle, round(ultrasonic_head.distance.real, 2), sound_sensor.reading, light_sensor.reading
                #change current angle of servo for next measurement
                servo_pan.target_angle = servo_pan.current_angle - 10
            elif servo_pan.current_angle <= -81:
                servo_pan.target_angle = -90
         elif servo_pan.current_angle == -90:
            scandirection = "left"
         sleep(0.25)
         
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
            if round(ultrasonic_front.distance.real, 2) < 0.75 and self.scan is True:
                MovePiTop.reducespeed()
                MoveServoPan.pause()
                servo_pan.target_angle = 0
                servo_tilt.target_angle = 0
                sleep(2)
                MovePiTop.pause()
                image = cam.get_frame()
                image.save("pictures/pitop_"+time_now+".jpg")
                servo_tilt.target_angle = 20
                sleep(2)
                MoveServoPan.resume()
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
        self.turnleftright = True
        self.tsl = 0
        self.tsr = 0
        self.dtl = 0
        self.dtr = 0
    def run(self):
        while self.running: #running process 3
            if self.turnforward is True:
                motor_right.set_power(drivespeed)
                motor_left.set_power(drivespeed)
            elif self.turnforward is False:
                motor_right.stop()
                motor_left.stop()
            sleep(5)
    def stop(self):
        self.running = False
    def pause(self):
        self.turnforward = False
    def reducespeed(self):
        self.turnforward = False
        if motor_right.current_rpm and motor_left.current_rpm > 0:
            motor_right.set_power(turnspeed)
            motor_left.set_power(turnspeed)
    def resume(self):
        self.turnforward = True
    def turn(self):
        #PiTop turn
        if self.dtl > 0:
            lc = motor_left.rotation_counter + self.dtl
        elif self.dtl < 0:
            lc = motor_left.rotation_counter - self.dtl*-1
        elif self.dtl == 0:
            lc = motor_left.rotation_counter

        if self.dtr > 0:
            rc = motor_right.rotation_counter + self.dtr
        elif self.dtr < 0:
            rc = motor_right.rotation_counter - self.dtr*-1
        elif self.dtr == 0:
            rc = motor_right.rotation_counter

        while self.turnleftright is True:
            if lc > motor_left.rotation_counter:
                motor_left.set_power(self.tsl)
            if lc < motor_left.rotation_counter:
                motor_left.set_power(self.tsl*-1)
            if lc+0.1 > motor_left.rotation_counter and lc-0.1<motor_left.rotation_counter:
                motor_left.stop()
    
            if rc > motor_right.rotation_counter:
                motor_right.set_power(self.tsr)
            if rc < motor_right.rotation_counter:
                motor_right.set_power(self.tsr*-1)
            if rc+0.1 > motor_right.rotation_counter and rc-0.1<motor_right.rotation_counter:
                motor_right.stop()

            if rc+0.1 > motor_right.rotation_counter and rc-0.1<motor_right.rotation_counter and lc+0.1 > motor_left.rotation_counter and lc-0.1<motor_left.rotation_counter:
                self.turnleftright = False
                self.turnforward = True
                print("run")
        
    def analyse(self):
        print("analyse moving direction")
        if drive_logic == 1:
            print("discover terrain - look for the best way")
            print("Break 5 sec")
            degree,range,noise,light=list(zip(*pan_maesure))
            print('space right:',sum(range[1:8])/8)
            print('space left:',sum(range[9:18])/8)
            sleep(5)
            if sum(range[1:8])/8 > sum(range[9:18])/8:
                #drive right direction
                self.tsl = 0.4
                self.tsr = 0.2
                self.dtl = 3.6
                self.dtr = 1.8
                self.turnleftright = True
                MovePiTop.turn()
            elif sum(range[1:8])/8 < sum(range[9:18])/8:
                #drive left direction
                self.tsl = 0.2
                self.tsr = 0.4
                self.dtl = 1.8
                self.dtr = 3.6
                self.turnleftright = True
                MovePiTop.turn()
        elif drive_logic == 2:
            print("search for noise - look for sources of noise")
            print("Break 5 sec")
            degree,range,noise,light=list(zip(*pan_maesure))
            print('noise right:',sum(noise[1:8])/8)
            print('noise left:',sum(noise[9:18])/8)
        elif drive_logic == 3:
            print("search for light - look for bright sources and lights")
            print("Break 5 sec")
            degree,range,noise,light=list(zip(*pan_maesure))
            print('light right:',sum(light[1:8])/8)
            print('light left:',sum(light[9:18])/8)

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

MoveServoPan = process1()
CamScan = process2()
MovePiTop = process3()
YellowBeacon = process4()

MovePiTop.start()
MoveServoPan.start()
CamScan.start()
YellowBeacon.start()
