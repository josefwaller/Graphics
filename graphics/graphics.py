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
from assets.files.entities.end_block import EndBlock

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
		level_file = open("assets/levels/l1.json","r")
		level = json.loads(level_file.read())


		Globals.enemies = [
		]

		Globals.platforms = [
		]
		for thing in level:
			if thing['type'] == 'platform':
				Globals.platforms.append(Platform(
					x=thing['x'], 
					y=thing['y'], 
					w=thing['w'],
					h=thing['h'],
					top_block="blocks/snow_top.png", 
					inner_block="blocks/snow.png"
				))

			elif thing['type'] == 'player':
				Globals.player = Player(x=thing['x'], y=thing['y'])

			elif thing['type'] == 'archer':
				Globals.enemies.append(Archer(x=thing['x'], y=thing['y'],))

			elif thing['type'] == 'walker':
				Globals.enemies.append(Walker(x=thing['x'], y=thing['y'], turn1=thing['turn1'], turn2=thing['turn2']))

			elif thing['type'] == 'wizard':
				Globals.enemies.append(Wizard(x=thing['x'], y=thing['y']))

			elif thing['type'] == 'jumper':
				Globals.enemies.append(Jumper(x=thing['x'], y=thing['y']))

			elif thing['type'] == 'bar':
				Globals.tools.append(BowAndArrow(x=thing['x'], y=thing['y']))

			elif thing['type'] == 'checkpoint':
				c = Checkpoint(x=thing['x'], y=thing['y'])
				Globals.checkpoints.append(c)

				try:
					if thing['is_starter'] == True:
						Globals.player.checkpoint = c
						c.flag_rising = True
						print("ASDF")
				except IndexError:
					pass

		self.play_game()

	def play_game(self):

		sky = Sky()

		k = KeyHandler()

		g = EndBlock(x=5, y=2, num=16)

		while True:

			for event in pygame.event.get():

				keys = k.new_event(event)

				Globals.player.while_keys_down(keys)

			sky.update()

			Globals.player.base_update()

			for c in Globals.checkpoints:
				c.base_update()

			for t in Globals.tools:
				t.base_update()

			for enemy in Globals.enemies:
				enemy.base_update()

			for platform in Globals.platforms:

				platform.base_update()

			for projectile in Globals.projectiles:

				projectile.base_update()

			g.base_update()

			pygame.display.flip()

			time.sleep(1 / 30)

if __name__ == "__main__":

	if sys.argv[1] == "playgame":

		main = Main()

	elif sys.argv[1] == "leveleditor":

		main = LevelEditor()


