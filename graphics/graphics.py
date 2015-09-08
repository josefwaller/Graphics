import sys
import pygame
import json
import time

from assets.files.player import Player
from assets.files.platform import Platform
from assets.files.key_handler import KeyHandler
from assets.files.globals import Globals

class Main ():

	def __init__(self):

		#creats the window, loads images, etc

		#initializes setting
		settingsFile = open("assets/settings/settings.json", "r")
		settings = json.loads(settingsFile.read())

		#Sets the window dimensions
		windowSize = width, height = settings['screenWidth'], settings['screenHeight']
		Globals.window = pygame.display.set_mode(windowSize)

		Globals.block_size = int(Globals.window.get_size()[1] / 16)
		Globals.pixel_size = int(Globals.window.get_size()[1] / 256)

		self.play_game()



	def play_game(self):

		white = 50, 50, 50

		player = Player(0, 1)

		Globals.platforms = [
			Platform(1, 9, 5, 1, pygame.image.load("assets/images/blocks/temp_block.png"), None)
		]

		k = KeyHandler()

		while True:

			for event in pygame.event.get():

				keys = k.new_event(event)

				player.while_keys_down(keys)

			Globals.window.fill(white)

			player.update()

			for platform in Globals.platforms:

				platform.render()

			platform.render()

			pygame.display.flip()

			time.sleep(1 / 30)

if __name__ == "__main__":

	main = Main()
	#main.playGame()