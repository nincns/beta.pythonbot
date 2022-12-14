from pitop import Camera, DriveController, PanTiltController, Pitop
from pitop.labs import RoverWebController
from pitop.labs.web.blueprints.rover import drive_handler, pan_tilt_handler
from pitop import LED
from pitop import UltrasonicSensor
from pitop import SoundSensor
from pitop import LightSensor
from threading import Thread
import time
from time import sleep

led_left = LED("D0")
led_right = LED("D7")
ultrasonic_head = UltrasonicSensor("D4")
sound_sensor = SoundSensor("A3")
light_sensor = LightSensor("A1")

rover = Pitop()

class process1(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.running = True
        rover.add_component(DriveController())
        rover.add_component(PanTiltController())
        rover.add_component(Camera())
    def run(self):
        while self.running:
            rover_controller = RoverWebController(
                get_frame=rover.camera.get_frame,
                message_handlers={
                "left_joystick": lambda data: drive_handler(rover.drive, data),
                "right_joystick": lambda data: pan_tilt_handler(rover.pan_tilt, data), },
             )
            rover_controller.serve_forever()
    def stop(self):
        self.running = False

class process2(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.running = True

    def run(self):
        while self.running:
            led_left.on()
            time.sleep(0.1)
            led_left.off()
            time.sleep(0.1)
            led_left.on()
            time.sleep(0.1)
            led_left.off()
            sleep(0.5)
            led_right.on()
            time.sleep(0.1)
            led_right.off()
            time.sleep(0.1)
            led_right.on()
            time.sleep(0.1)
            led_right.off()
            sleep(0.5)
    def stop(self):
        self.running = False

class process3(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.running = True

    def run(self):
        while self.running:
            print("distance:", round(ultrasonic_head.distance.real, 2), "m - noise:", sound_sensor.reading, "- light:", light_sensor.reading)
            sleep(3)
    def stop(self):
        self.running = False

Rover = process1()
YellowBeacon = process2()
Measurement = process3()

Rover.start()
YellowBeacon.start()
Measurement.start()