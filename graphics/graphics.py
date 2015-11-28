import sys
import pygame
import json
import time

from assets.files.entities.player import Player
from assets.files.entities.platform import Platform
from assets.files.entities.trigger import Trigger

from assets.files.entities.current_tool import CurrentTool
from assets.files.entities.tools.bow_and_arrow import BowAndArrow
from assets.files.entities.tools.sword import Sword
from assets.files.entities.tools.staff import Staff

from assets.files.entities.enemies.walker import Walker
from assets.files.entities.enemies.wizard import Wizard
from assets.files.entities.enemies.archer import Archer
from assets.files.entities.enemies.jumper import Jumper

from assets.files.entities.checkpoint import Checkpoint
from assets.files.entities.sky import Sky
from assets.files.entities.end_block import EndBlock

from assets.files.utilities.key_handler import KeyHandler
from assets.files.utilities.globals import Globals
from assets.files.utilities.heads_up_display import HeadsUpDisplay

from level_editor import LevelEditor

class Main ():

	def __init__(self):
		pygame.init()

		#creats the window, loads images, etc

		#initializes setting
		settings_file = open("assets/settings/settings.json", "r")
		settings = json.loads(settings_file.read())

		#Sets the window dimensions
		windowSize = width, height = settings['screenWidth'], settings['screenHeight']
		Globals.window = pygame.display.set_mode(windowSize)

		Globals.block_size = int(Globals.window.get_size()[1] / 15)
		Globals.pixels_per_block = 16
		Globals.gravity_strength = 15 * Globals.block_size

		#loads level
		level_file = open("assets/levels/current_level.json","r")
		level = json.loads(level_file.read())

		Globals.hud = HeadsUpDisplay()


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
					inner_block="blocks/snow.png",
					update_inner_block="blocks/16_snow.png",
					update_top_block="blocks/16_snow_top.png"
				))

			elif thing['type'] == 'player':
				Globals.player = Player(x=thing['x'], y=thing['y'])
				print(thing['x'])

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

			elif thing['type'] == 'sword':
				Globals.tools.append(Sword(x=thing['x'], y=thing['y']))

			elif thing['type'] == "staff":
				Globals.tools.append(Staff(x=thing['x'], y=thing['y']))

			elif thing['type'] == 'checkpoint':
				c = Checkpoint(x=thing['x'], y=thing['y'])
				Globals.checkpoints.append(c)

				try:
					if thing['is_starter'] == True:
						Globals.player.checkpoint = c
						c.flag_rising = True
				except KeyError:
					pass

			elif thing['type'] == 'endblock':
				Globals.endblock = EndBlock(x=thing['x'], y=thing['y'])

			elif thing['type'] == 'level_settings':
				Globals.level_width = thing['width'] * Globals.block_size
				Globals.level_height = thing['height'] * Globals.block_size

		self.play_game()

	def play_game(self):

		sky = Sky("props/sky.png", "props/16_sky.png")

		k = KeyHandler()

		t = Trigger(x=0, y=0, w=5, h=5, on_enter=Globals.hud.dialog_box, parameters=[
			['Hello! I am the main player in the graphics game. I am so cool. Lad di da di da da doo. So cool. HAHAHAHAHAHA.',
			'This is the second line of dialog! LOLZ'],
			['assets/images/player/run_2.png',
			'assets/images/player/run_2.png']
		])

		Globals.player_tool_sprite = CurrentTool()

		while True:

			starting_frame_time = time.time()

			for event in pygame.event.get():

				keys = k.new_event(event)

				Globals.player.while_keys_down(keys)

				Globals.hud.on_input(keys)

			sky.base_update()

			Globals.player.base_update()

			Globals.player_tool_sprite.update()

			for c in Globals.checkpoints:
				c.base_update()

			for t in Globals.tools:
				t.base_update()

			for enemy in Globals.enemies:
				enemy.base_update()

			for platform in Globals.platforms:

				platform.update()

			for projectile in Globals.projectiles:

				projectile.base_update()

			Globals.endblock.base_update()

			t.update()

			Globals.hud.render()

			pygame.display.flip()

			while time.time() - starting_frame_time < 1 / 60:
				pass

if __name__ == "__main__":

	if sys.argv[1] == "playgame":

		main = Main()

	elif sys.argv[1] == "leveleditor":

		main = LevelEditor()


