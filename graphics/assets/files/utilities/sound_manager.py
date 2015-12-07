import pygame
import time

from assets.files.utilities.globals import Globals


# Manages the background music and sound
class SoundManager:

	# The current music playing
	menu_music = None
	game_music = None

	playing_menu_music = True
	reset_music = False

	graphics_level = 0

	def __init__(self):
		self.update_graphics()
		pygame.mixer.music.load("assets/music/%s" % self.menu_music)
		pygame.mixer.music.play(-1)

	def update_graphics(self):

		# Updates music
		if Globals.graphics_level == 0:
			self.menu_music = "t_menu.wav"
			self.game_music = "t.wav"
		elif Globals.graphics_level == 1:
			self.menu_music = "8_menu.wav"
			self.game_music = "8.wav"
		elif Globals.graphics_level == 2:
			self.menu_music = "16_menu.wav"
			self.game_music = "16.wav"

		self.graphics_level = Globals.graphics_level

		self.reset_music = True

	def update(self):

		if not Globals.is_paused or Globals.in_menu:

			if self.graphics_level is not Globals.graphics_level:
				self.update_graphics()

			if not self.playing_menu_music == Globals.in_menu or self.reset_music:
				self.playing_menu_music = not self.playing_menu_music
				if self.playing_menu_music:
					self.play_music(self.menu_music)
				else:
					self.play_music(self.game_music)

				self.reset_music = False
	@staticmethod
	def play_music(music):
		pygame.mixer.music.load("assets/music/%s" % music)
		pygame.mixer.music.play(-1)



