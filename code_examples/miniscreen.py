# Import modules
from pitop.miniscreen import Miniscreen
from time import sleep

# Initialise the Miniscreen
miniscreen = Miniscreen()

# Prompt for user input from the console
name = input("Type your name here, then press Enter: ")

# Draw the message to the screen for 5 seconds
miniscreen.display_multiline_text('Hello, ' + name, font_size=20)
sleep(5)