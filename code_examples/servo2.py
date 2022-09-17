# Import modules
from pitop import ServoMotor
from pitop import UltrasonicSensor
from signal import pause

# Setup the servo on port S0 of the expansion plate
servo = ServoMotor("S0")
# Setup the ultrasonic on port D2
ultrasonic = UltrasonicSensor("D3", threshold_distance=0.3)
sp = 100 #sets servo speed and direction

#Move the servo using this is a function
def triggerServo():
  global sp
  servo.sweep(sp)
  sp = -sp
  # Print to the console
  print("Servo triggered with speed: " + str(sp))

# Trigger the servo when an object comes within 30cm (the threshold distqnce).
ultrasonic.when_in_range = triggerServo
pause()