from pitop import BrakingType, EncoderMotor, ForwardDirection
from time import sleep

motor_right = EncoderMotor("M0", ForwardDirection.COUNTER_CLOCKWISE)
motor_left = EncoderMotor("M3", ForwardDirection.CLOCKWISE)
motor_right.breaking_type = BrakingType.COAST
motor_left.breaking_type = BrakingType.COAST
motor_right.wheel_diameter=0.05
motor_left.wheel_diameter=0.05

turnspeed = 0.2

drive_left = input("set drivedistance left: ")
drive_left = float(drive_left)

if drive_left > 0:
    lc = motor_left.rotation_counter + drive_left
elif drive_left < 0:
    drive_left = drive_left*-1
    lc = motor_left.rotation_counter - drive_left
elif drive_left == 0:
    lc = motor_left.rotation_counter

turn_left = True

while turn_left is True:
     print(lc)
     if lc > motor_left.rotation_counter:
        motor_left.set_power(turnspeed)
     if lc < motor_left.rotation_counter:
        motor_left.set_power(turnspeed*-1)
     if lc == motor_left.rotation_counter:
        motor_left.stop()
        turn_left = False
     print(motor_left.rotation_counter)
     #sleep(0.1)
