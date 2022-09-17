# Import modules
from pitop import Camera
from further_link import send_image
from pitop import Pitop
from signal import pause

#Create objects
pitop = Pitop()
select = pitop.miniscreen.select_button
cam = Camera()

#A function that takes a picture and sends it to Further
def take_picture():
  print('Say cheese!')
  send_image(cam.get_frame())

#The main program
select.when_pressed = take_picture
print('Press the select button (O) on the pi-top[4] to take a picture')
pause()
