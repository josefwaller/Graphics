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

	# Fading variables
	fading_in = False
	fading_out = False
	fade_time = 0
	fade_duration = 0.5

	# Last known value of globals.in_menu
	# Used to change the song playing, because it should only change in between menu and game
	in_menu = True

	def __init__(self):
		self.update_graphics()
		pygame.mixer.music.load("assets/music/%s" % self.menu_music)
		pygame.mixer.music.play(-1)

	def update_graphics(self):

		# Updates music
		if Globals.graphics_level == 0:
			self.menu_music = "t_menu.wav"
			self.game_music = "t_game.wav"
		elif Globals.graphics_level == 1:
			self.menu_music = "8_menu.wav"
			self.game_music = "8_game.wav"
		elif Globals.graphics_level == 2:
			self.menu_music = "16_menu.wav"
			self.game_music = "16_game.wav"

		self.graphics_level = Globals.graphics_level

		self.reset_music = True

	def update(self):

		if not Globals.is_paused or Globals.in_menu:

			if self.graphics_level is not Globals.graphics_level:
				self.update_graphics()

			if not Globals.in_menu == self.in_menu:
				self.playing_menu_music = not self.playing_menu_music
				if self.playing_menu_music:
					self.play_music(self.menu_music)
				else:
					self.play_music(self.game_music)

				self.in_menu = Globals.in_menu

		# Fading in and out
		if self.fading_out:
			volume = (self.fade_duration - (time.time() - self.fade_time)) / self.fade_duration
			if volume <= 0:
				self.fading_out = False
				pygame.mixer.music.set_volume(0)
			else:
				pygame.mixer.music.set_volume(volume)

		elif self.fading_in:
			volume = (time.time() - self.fade_time) / self.fade_duration
			if volume >= 1:
				self.fading_in = False
				pygame.mixer.music.set_volume(1)
			else:
				pygame.mixer.music.set_volume(volume)

		# Checks globals to see if it should fade in or out
		if Globals.music_fade_in:
			self.fading_in = True
			self.fade_time = time.time()
			pygame.mixer.music.set_volume(0)
			Globals.music_fade_in = False

		elif Globals.music_fade_out:
			self.fading_out = True
			self.fade_time = time.time()
			pygame.mixer.music.set_volume(1)
			Globals.music_fade_out = False

	@staticmethod
	def play_music(music):
		pygame.mixer.music.load("assets/music/%s" % music)
		pygame.mixer.music.play(-1)
