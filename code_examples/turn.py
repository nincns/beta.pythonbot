from pitop import BrakingType, EncoderMotor, ForwardDirection
from time import sleep

mr = EncoderMotor("M0", ForwardDirection.COUNTER_CLOCKWISE)
ml = EncoderMotor("M3", ForwardDirection.CLOCKWISE)
mr.breaking_type = BrakingType.COAST
ml.breaking_type = BrakingType.COAST
mr.wheel_diameter=0.05
ml.wheel_diameter=0.05

tsl = input("set turnspeed left 0.2 - 1.0: ")
tsl = float(tsl)
tsr = input("set turnspeed right 0.2 - 1.0: ")
tsr = float(tsr)

dtl = input("set dtrivedistance left: ")
dtl = float(dtl)
dtr = input("set dtrivedistance right: ")
dtr = float(dtr)

if dtl > 0:
    lc = ml.rotation_counter + dtl
elif dtl < 0:
    lc = ml.rotation_counter - dtl*-1
elif dtl == 0:
    lc = ml.rotation_counter

if dtr > 0:
    rc = mr.rotation_counter + dtr
elif dtr < 0:
    rc = mr.rotation_counter - dtr*-1
elif dtr == 0:
    rc = mr.rotation_counter

turn = True

while turn is True:
     if lc > ml.rotation_counter:
        ml.set_power(tsl)
     if lc < ml.rotation_counter:
        ml.set_power(tsl*-1)
     if lc+0.1 > ml.rotation_counter and lc-0.1<ml.rotation_counter:
        ml.stop()
    
     if rc > mr.rotation_counter:
        mr.set_power(tsr)
     if rc < mr.rotation_counter:
        mr.set_power(tsr*-1)
     if rc+0.1 > mr.rotation_counter and rc-0.1<mr.rotation_counter:
        mr.stop()

     if rc+0.1 > mr.rotation_counter and rc-0.1<mr.rotation_counter and lc+0.1 > ml.rotation_counter and lc-0.1<ml.rotation_counter:
        print("arrived")
        turn = False


