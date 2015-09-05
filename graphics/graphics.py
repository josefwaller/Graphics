import sys
from pygame import *
import json

class Main ():

	def __init__(self):

		#creats the window, loads images, etc

		#initializes setting
		settingsFile = open("assets/settings/settings.json", "r")

		print(json.loads(settingsFile.read()))



	def startGame(self):

		print("game started")

if __name__ == "__main__":

	main = Main()
	main.startGame()