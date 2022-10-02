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
drive_right = input("set drivedistance right: ")
drive_right = float(drive_right)

if drive_left > 0:
    lc = motor_left.rotation_counter + drive_left
elif drive_left < 0:
    lc = motor_left.rotation_counter - drive_left
elif drive_left == 0:
    lc = motor_left.rotation_counter = drive_left
print(lc)

if drive_right > 0:
    rc = motor_right.rotation_counter + drive_right
elif drive_right < 0:
    rc = motor_right.rotation_counter - drive_right
elif drive_right == 0:
    rc = motor_right.rotation_counter = drive_right
print(rc)

turn = True

while turn is True:
     if lc != motor_left.rotation_counter:
        if drive_left > 0:
            motor_left.set_power(turnspeed)
        elif drive_left < 0:
            motor_left.set_power(-turnspeed)
        elif drive_left == 0:
            motor_left.stop()
     elif lc == motor_left.rotation_counter:
        motor_left.stop()

     if rc != motor_right.rotation_counter:
        if drive_right > 0:
            motor_left.set_power(turnspeed)
        elif drive_right < 0:
            motor_right.set_power(-turnspeed)
        elif drive_left == 0:
            motor_right.stop()
     elif rc == motor_right.rotation_counter:
        motor_right.stop()
     if rc == motor_left.rotation_counter and rc == motor_right.rotation_counter:
        turn = False