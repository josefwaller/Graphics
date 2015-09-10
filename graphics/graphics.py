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

		print(Globals.block_size)

		self.play_game()



	def play_game(self):

		white = 50, 50, 50

		player = Player(0, 12)

		Globals.platforms = [
			Platform(x=1, y=10, w=5, h=1, top_block=pygame.image.load("assets/images/blocks/temp_block.png"), inner_block=None),
			Platform(x=7, y=4, w=3, h=2, top_block=pygame.image.load("assets/images/blocks/temp_block.png"), inner_block=pygame.image.load("assets/images/blocks/temp_block.png")),
			Platform(x=12, y=7, w=2, h=1, top_block=pygame.image.load("assets/images/blocks/temp_block.png"), inner_block=None),
			Platform(x=0, y=15, w=25, h=1, top_block=pygame.image.load("assets/images/blocks/temp_block.png"), inner_block=None)
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