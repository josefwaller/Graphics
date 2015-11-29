import sys
import pygame
import json
import time

from assets.files.utilities.key_handler import KeyHandler
from assets.files.utilities.globals import Globals
from assets.files.utilities.level_reader import LevelReader
from assets.files.utilities.main_menu import MainMenu

from assets.files.entities.sky import Sky
from assets.files.entities.current_tool import CurrentTool

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

		r = LevelReader()
		r.read_level(level_file.read())

		self.play_game()

	def play_game(self):

		sky = Sky("props/sky.png", "props/16_sky.png")

		k = KeyHandler()

		m = MainMenu()

		Globals.player_tool_sprite = CurrentTool()

		while True:

			starting_frame_time = time.time()

			for event in pygame.event.get():

				keys = k.new_event(event)

				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()

			if Globals.in_menu:

				m.update()

			else:

				if not Globals.is_paused:

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

				for prop in Globals.props:
					prop.update()

				Globals.endblock.base_update()

				Globals.hud.render()

			pygame.display.flip()

			while time.time() - starting_frame_time < 1 / 60:
				pass

if __name__ == "__main__":

	if sys.argv[1] == "playgame":

		main = Main()

	elif sys.argv[1] == "leveleditor":

		main = LevelEditor()


