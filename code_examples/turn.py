from pitop import BrakingType, EncoderMotor, ForwardDirection
from time import sleep

motor_right = EncoderMotor("M0", ForwardDirection.COUNTER_CLOCKWISE)
motor_left = EncoderMotor("M3", ForwardDirection.CLOCKWISE)
motor_right.breaking_type = BrakingType.COAST
motor_left.breaking_type = BrakingType.COAST
motor_right.wheel_diameter=0.05
motor_left.wheel_diameter=0.05

turnspeed = input("set turnspeed 0.2 - 1.0: ")
turnspeed = float(turnspeed)

drive_left = input("set drivedistance left: ")
drive_left = float(drive_left)
drive_right = input("set drivedistance right: ")
drive_right = float(drive_right)

if drive_left > 0:
    lc = motor_left.rotation_counter + drive_left
elif drive_left < 0:
    drive_left = drive_left*-1
    lc = motor_left.rotation_counter - drive_left
elif drive_left == 0:
    lc = motor_left.rotation_counter

if drive_right > 0:
    rc = motor_right.rotation_counter + drive_right
elif drive_right < 0:
    drive_right = drive_right*-1
    rc = motor_right.rotation_counter - drive_right
elif drive_right == 0:
    rc = motor_right.rotation_counter

turn = True

while turn is True:
     if lc > motor_left.rotation_counter:
        motor_left.set_power(turnspeed)
     if lc < motor_left.rotation_counter:
        motor_left.set_power(turnspeed*-1)
     if lc+0.1 > motor_left.rotation_counter and lc-0.1<motor_left.rotation_counter:
        motor_left.stop()
    
     if rc > motor_right.rotation_counter:
        motor_right.set_power(turnspeed)
     if rc < motor_right.rotation_counter:
        motor_right.set_power(turnspeed*-1)
     if rc+0.1 > motor_right.rotation_counter and rc-0.1<motor_right.rotation_counter:
        motor_right.stop()
     if rc+0.1 > motor_right.rotation_counter and rc-0.1<motor_right.rotation_counter and lc+0.1 > motor_left.rotation_counter and lc-0.1<motor_left.rotation_counter:
        print("arived")
        turn = False


