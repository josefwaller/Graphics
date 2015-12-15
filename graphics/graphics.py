import sys
import pygame
import json
import time
import os

from assets.files.utilities.key_handler import KeyHandler
from assets.files.utilities.globals import Globals
from assets.files.utilities.main_menu import MainMenu
from assets.files.utilities.music_manager import MusicManager

from level_editor import LevelEditor
from assets.files.utilities.level_reader import LevelReader


class Main:

	settings = None

	def __init__(self):
		pygame.init()

		# creates the window, loads images, etc

		# initializes setting
		settings_directory = "assets/settings/settings.json"
		if os.path.isfile(settings_directory):
			settings_file = open("assets/settings/settings.json", "r")
			self.settings = json.loads(settings_file.read())
			settings_file.close()
		else:
			settings_file = open(settings_directory, "w")
			settings_file.seek(0)
			default_settings = {
				"screen_width": 800,
				"screen_height": 600,
				"volume": 1,
				"fps": 60,
				"graphics_level": 0
			}
			settings_file.write(json.dumps(default_settings))
			settings_file.close()
			self.settings = default_settings

		# Sets the window dimensions
		window_size = self.settings['screen_width'], self.settings['screen_height']
		if window_size[0] == 0 and window_size[0] == 0:
			info = pygame.display.Info()
			window_size = (info.current_w, info.current_h)
			Globals.window = pygame.display.set_mode(window_size, pygame.FULLSCREEN)
		else:
			Globals.window = pygame.display.set_mode(window_size)

		pygame.display.set_caption("Graphics")
		pygame.display.set_icon(pygame.image.load("assets/images/menu/icon.png").convert_alpha())

		Globals.block_size = int(Globals.window.get_size()[1] / 15)
		Globals.pixels_per_block = 10
		Globals.gravity_strength = 15 * Globals.block_size
		Globals.graphics_level = self.settings['graphics_level']

	def play_game(self):

		k = KeyHandler()
		m = MainMenu()
		s = MusicManager()

		keys = [[], []]

		while True:

			s.update()

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

				Globals.hud.on_input(keys[1])

				Globals.sky.base_update()

				Globals.player.base_update()

				Globals.player_tool_sprite.update()

				for c in Globals.checkpoints:
					c.base_update()

				for t in Globals.tools:
					t.base_update()

				for platform in Globals.platforms:
					platform.update()

				for enemy in Globals.enemies:
					enemy.base_update()

				for projectile in Globals.projectiles:
					projectile.base_update()

				for prop in Globals.props:
					prop.update()

				if Globals.endblock is not None:
					Globals.endblock.base_update()

				Globals.hud.render()

			pygame.display.flip()

			while time.time() - starting_frame_time < 1 / self.settings['fps']:
				pass

	def test_level (self, lvl_string):

		Globals.in_menu = False
		file = open("assets/levels/%s" % lvl_string)
		Globals.graphics_level = 2

		l = LevelReader()
		l.read_level(file.read())
		file.close()
		self.play_game()

if __name__ == "__main__":

	if sys.argv[1] == "playgame":

		main = Main()
		main.play_game()

	elif sys.argv[1] == "leveleditor":

		args = sys.argv[2:].copy()
		# while len(args) < 4:
		# 	args.append(None)

		main = LevelEditor(*args)

	elif sys.argv[1] == "testlevel":
		main = Main()
		main.test_level(sys.argv[2])
		print("ASDF")

