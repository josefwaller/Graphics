import sys
import pygame
import json
import time

from assets.files.utilities.key_handler import KeyHandler
from assets.files.utilities.globals import Globals
from assets.files.utilities.main_menu import MainMenu

from level_editor import LevelEditor

class Main ():

	settings = None

	def __init__(self):
		pygame.init()

		#creats the window, loads images, etc

		#initializes setting
		settings_file = open("assets/settings/settings.json", "r")
		self.settings = json.loads(settings_file.read())
		settings_file.close()

		#Sets the window dimensions
		windowSize = width, height = self.settings['screen_width'], self.settings['screen_height']
		Globals.window = pygame.display.set_mode(windowSize)

		Globals.block_size = int(Globals.window.get_size()[1] / 15)
		Globals.pixels_per_block = 10
		Globals.gravity_strength = 15 * Globals.block_size
		Globals.graphics_level = self.settings['graphics_level']

		self.play_game()

	def play_game(self):

		k = KeyHandler()

		m = MainMenu()

		keys = [[],[]]

		while True:

			starting_frame_time = time.time()

			keys[1] = []

			for event in pygame.event.get():

				keys = k.new_event(event)

				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()

			if Globals.in_menu:

				m.update()
				m.on_input(keys[1])

			else:

				if not Globals.is_paused:

					Globals.player.while_keys_down(keys[0])

				Globals.hud.on_input(keys[0])

				Globals.sky.base_update()

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

			while time.time() - starting_frame_time < 1 / self.settings['fps']:
				pass

if __name__ == "__main__":

	if sys.argv[1] == "playgame":

		main = Main()

	elif sys.argv[1] == "leveleditor":

		main = LevelEditor()


