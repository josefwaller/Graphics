import sys
import pygame
import json
import time

from assets.files.entities.player import Player
from assets.files.entities.platform import Platform

from assets.files.entities.tools.bow_and_arrow import BowAndArrow

from assets.files.entities.enemies.walker import Walker
from assets.files.entities.enemies.wizard import Wizard
from assets.files.entities.enemies.archer import Archer
from assets.files.entities.enemies.jumper import Jumper

from assets.files.entities.checkpoint import Checkpoint
from assets.files.entities.sky import Sky

from assets.files.utilities.key_handler import KeyHandler
from assets.files.utilities.globals import Globals
from level_editor import LevelEditor

class Main ():

	def __init__(self):

		#creats the window, loads images, etc

		#initializes setting
		settings_file = open("assets/settings/settings.json", "r")
		settings = json.loads(settings_file.read())

		#Sets the window dimensions
		windowSize = width, height = settings['screenWidth'], settings['screenHeight']
		Globals.window = pygame.display.set_mode(windowSize)

		Globals.block_size = int(Globals.window.get_size()[1] / 16)
		Globals.pixel_size = int(Globals.window.get_size()[1] / 256)

		Globals.gravity_strength = 15 * Globals.block_size

		#loads level
		# level_file = open("assets/levels/l1.json","r")
		# level = json.loads(level_file.read())

		self.play_game()



	def play_game(self):

		Globals.player = Player(0, 11)

		sky = Sky()

		Globals.platforms = [
			Platform(x=1, y=10, w=5, h=1, top_block="blocks/snow_top.png", inner_block=None),
			Platform(x=7, y=4, w=10, h=2, top_block="blocks/snow_top.png", inner_block="blocks/snow.png"),
			Platform(x=12, y=7, w=2, h=1, top_block="blocks/snow_top.png", inner_block=None),
			Platform(x=0, y=15, w=45, h=1, top_block="blocks/snow_top.png", inner_block=None)
		]

		Globals.enemies = [
			Walker(x=7, y=1, turn1=7, turn2=10),
			Wizard(x=15, y=14),
			Archer(x=12, y=6),
			Archer(x=40, y=3),
			Jumper(x= 30, y=3)
		]

		checkpoint = Checkpoint(x=10, y=13)

		arrow = BowAndArrow(x=5, y=14)

		k = KeyHandler()

		while True:

			for event in pygame.event.get():

				keys = k.new_event(event)

				Globals.player.while_keys_down(keys)

			sky.update()

			Globals.player.base_update()

			checkpoint.base_update()

			arrow.base_update()

			for enemy in Globals.enemies:
				enemy.base_update()

			for platform in Globals.platforms:

				platform.base_update()

			for projectile in Globals.projectiles:

				projectile.base_update()

			pygame.display.flip()

			time.sleep(1 / 30)

if __name__ == "__main__":

	if sys.argv[1] == "playgame":

		main = Main()

	elif sys.argv[1] == "leveleditor":

		main = LevelEditor()


