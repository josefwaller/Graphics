from assets.files.utilities.globals import Globals
from assets.files.utilities.level_reader import LevelReader

import pygame
import json
import time
import sys


class MainMenu:

	logo = None

	logo_x = 0
	logo_y = 0

	graphics_level = 0

	sky = None

	colors_one = [
		(192, 192, 192),
		(0, 0, 0),
		(192, 192, 192)
	]
	colors_two = [
		(64, 64, 64),
		(255, 255, 255),
		(64, 64, 64)
	]

	color_one = None
	color_two = None

	fade_in = True
	fade_out = False
	fade_alpha = 0
	fade_duration = 1
	fade_start_time = 0

	last_keys = []

	buttons = []

	selected_button = 0

	def __init__(self):

		self.grahpics_level = Globals.graphics_level
		
		self.logos = [
			pygame.image.load("assets/images/menu/t_logo.png").convert_alpha(),
			pygame.image.load("assets/images/menu/8_logo.png").convert_alpha(),
			pygame.image.load("assets/images/menu/16_logo.png").convert_alpha()
		]
		self.skies = [
			pygame.image.load("assets/images/props/t_sky.png").convert_alpha(),
			pygame.image.load("assets/images/props/8_sky.png").convert_alpha(),
			pygame.image.load("assets/images/props/16_sky.png").convert_alpha(),
		]

		w = Globals.window.get_size()

		# Sets Buttons

		self.buttons = [
			{
				"text": "CONTINUE",
				"on_click": self.resume
			},
			{
				"text": "NEW",
				"on_click": self.new_game
			},
			{
				"text": "QUIT",
				"on_click": self.quit
			}
		]

		self.b_min_y = w[1] / 2

		self.b_w = w[0] / 5
		self.b_h = (w[1] - self.b_min_y) / (2 * len(self.buttons))

		self.b_x = (w[0] - self.b_w) / 2

		self.b_border_w = 5

		self.b_font = pygame.font.Font("assets/fonts/Minecraftia-Regular.ttf", 20)

		self.set_up()

	def set_up(self):

		self.graphics_level = Globals.graphics_level

		w = Globals.window.get_size()

		self.logo = self.logos[Globals.graphics_level]
		self.sky = self.skies[Globals.graphics_level]

		# Rounds logo width closest to one thirds as wide of the screen
		pixel_size = Globals.block_size / Globals.pixels_per_block
		approx_logo_w = w[0] / 3
		logo_w_in_pixels = self.logo.get_size()[0] * pixel_size
		logo_w = int(approx_logo_w / logo_w_in_pixels * logo_w_in_pixels)
		logo_h = int(self.logo.get_size()[1] * (self.logo.get_size()[0] / self.logo.get_size()[1]))

		self.logo = pygame.transform.scale(self.logo, (logo_w, logo_h))
		self.logo_x = (w[0] - logo_w) / 2
		self.logo_y = int(w[1] / 4)

		# Scales sky
		converter = self.sky.get_size()[0] / self.sky.get_size()[1]
		new_w = int(w[1] * converter)
		new_h = w[1]
		self.sky = pygame.transform.scale(self.sky, (new_w, new_h))

		self.fade_in = True
		self.fade_alpha = 255
		self.fade_start_time = time.time()

		# Saves the graphics level
		settings_file = open("assets/settings/settings.json", "r+")
		settings = json.loads(settings_file.read())
		settings['graphics_level'] = Globals.graphics_level
		settings_file.seek(0)
		settings_file.write(json.dumps(settings))
		settings_file.close()

		self.color_one = self.colors_one[Globals.graphics_level]
		self.color_two = self.colors_two[Globals.graphics_level]

	def update(self):
		if not self.graphics_level == Globals.graphics_level:
			self.set_up()

		self.render()
		self.move_sky()

	def move_sky(self):

		pass

	def on_input(self, keys):

		if pygame.K_RETURN in keys:
			if not self.fade_in and not self.fade_out:
				self.buttons[self.selected_button]['on_click']()

		elif pygame.K_UP in keys and self.selected_button >= 1:
			self.selected_button -= 1

		elif pygame.K_DOWN in keys and self.selected_button <= len(self.buttons) - 2:
			self.selected_button += 1

	def render(self):

		Globals.window.blit(self.sky, (0, 0))
		Globals.window.blit(self.logo, (self.logo_x, self.logo_y))

		for i in range(len(self.buttons)):
			y = self.b_min_y + i * (1.5 * self.b_h)

			if self.selected_button == i:
				box_color = self.color_two
				border_color = self.color_one

			else:
				box_color = self.color_one
				border_color = self.color_two

			pygame.draw.rect(Globals.window, border_color, [
				self.b_x - self.b_border_w,
				y - self.b_border_w,
				self.b_w + 2 * self.b_border_w,
				self.b_h + 2 * self.b_border_w
			])

			pygame.draw.rect(Globals.window, box_color, [
				self.b_x,
				y,
				self.b_w,
				self.b_h
			])

			font_x = self.b_x + (self.b_w - self.b_font.size(self.buttons[i]["text"])[0]) / 2
			font_y = y + (self.b_h - self.b_font.get_height()) / 2

			r = self.b_font.render(self.buttons[i]["text"], False, border_color)
			Globals.window.blit(r, (font_x, font_y))

		if self.fade_in or self.fade_out:
			rect = pygame.Surface(Globals.window.get_size())
			rect.set_alpha(self.fade_alpha)
			Globals.window.blit(rect, (0, 0))

			time_since = time.time() - self.fade_start_time

			if self.fade_in:
				self.fade_alpha = int(255 - (time_since * (255 / self.fade_duration)))

				if self.fade_alpha < 0:
					self.fade_in = False

			elif self.fade_out:
				self.fade_alpha = int(time_since * (255 / self.fade_duration))

				if self.fade_alpha > 255:
					self.fade_out = False
					Globals.in_menu = False

	def resume(self):
		
		# loads level
		level_file = open("assets/levels/l%s.json" % (Globals.graphics_level + 1), "r")
		r = LevelReader()
		r.read_level(level_file.read())
		level_file.close()

		self.fade_out = True
		self.fade_alpha = 0
		self.fade_start_time = time.time()

	def new_game(self):

		# Resets everything
		settings_file = open("assets/settings/settings.json", "r+")
		old_settings = json.loads(settings_file.read())
		new_settings = old_settings.copy()
		new_settings['graphics_level'] = 0
		Globals.graphics_level = 0
		self.graphics_level = Globals.graphics_level
		settings_file.seek(0)
		settings_file.write(json.dumps(new_settings))
		
		# loads level
		level_file = open("assets/levels/l1.json", "r")
		r = LevelReader()
		r.read_level(level_file.read())
		level_file.close()

		self.fade_out = True
		self.fade_alpha = 0
		self.fade_start_time = time.time()

	@staticmethod
	def quit():
		pygame.quit()
		sys.exit()
