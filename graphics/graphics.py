import sys
from pygame import *
import json

class Main ():

	def __init__(self):

		#creats the window, loads images, etc

		#initializes setting
		settingsFile = open("assets/settings/settings.json", "r")
		settings = json.loads(settingsFile.read())

		#Sets the window dimensions
		windowSize = height, width = settings['screenWidth'], settings['screenHeight']
		window = display.set_mode(windowSize)



	def playGame(self):

		print("game started")

		while True:

			display.flip()

if __name__ == "__main__":

	main = Main()
	main.playGame()