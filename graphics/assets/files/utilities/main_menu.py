from assets.files.utilities.globals import Globals
from assets.files.utilities.level_reader import LevelReader

import pygame
import sys
import json

class MainMenu ():

	logo = None

	logo_x = 0
	logo_y = 0

	sky = None

	grey = (192, 192, 192)
	dark_grey = (64, 64, 64)

	last_keys = []

	buttons = []

	selected_button = 1

	def __init__(self):
		
		self.logo = pygame.image.load("assets/images/menu/logo.png").convert_alpha()
		self.sky = pygame.image.load("assets/images/props/sky.png").convert_alpha()

		w = Globals.window.get_size()

		#Rounds logo width closest to one thirds as wide of the screen
		pixel_size = Globals.block_size / Globals.pixels_per_block
		approx_logo_w = w[0] / 3
		logo_w_in_pixels = self.logo.get_size()[0] * pixel_size
		logo_w = int(approx_logo_w / logo_w_in_pixels * logo_w_in_pixels)
		logo_h = int(self.logo.get_size()[1] * (self.logo.get_size()[0] / self.logo.get_size()[1]))

		self.logo = pygame.transform.scale(self.logo, (logo_w, logo_h))
		self.logo_x = (w[0] - logo_w) / 2
		self.logo_y = int(w[1] / 4)

		#Scales sky
		converter = self.sky.get_size()[0] / self.sky.get_size()[1]
		new_w = int(w[1] * converter)
		new_h = w[1]
		self.sky = pygame.transform.scale(self.sky, (new_w, new_h))

		#Sets Buttons

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

	def update(self):

		self.render()

	def on_input (self, keys):

		if pygame.K_RETURN in keys:
			self.buttons[self.selected_button]['on_click']()

		elif pygame.K_UP in keys and self.selected_button >= 1:
			self.selected_button -= 1

		elif pygame.K_DOWN in keys and self.selected_button <= len(self.buttons) - 2:
			self.selected_button += 1

	def render (self):

		w = Globals.window.get_size()
		
		Globals.window.blit(self.sky, (0, 0))

		Globals.window.blit(self.logo, (self.logo_x, self.logo_y))

		for i in range(len(self.buttons)):

			y = self.b_min_y + i * (1.5 * self.b_h)

			if self.selected_button == i:
				box_color = self.dark_grey
				border_color = self.grey
			else:
				box_color = self.grey
				border_color = self.dark_grey

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

	def resume (self):
		
		#loads level
		level_file = open("assets/levels/l%s.json" % Globals.graphics_level,"r")
		r = LevelReader()
		r.read_level(level_file.read())
		level_file.close()

		Globals.in_menu = False

	def quit (self):
		pygame.quit()
		sys.exit()
	def new_game (self):

		#Resets everything
		settings_file = open("assets/settings/settings.json", "r+")
		old_settings = json.loads(settings_file.read())
		new_settings = old_settings.copy()
		new_settings['graphics_level'] = 0
		settings_file.seek(0)
		settings_file.write(json.dumps(new_settings))
		
		#loads level
		level_file = open("assets/levels/l1.json","r")
		r = LevelReader()
		r.read_level(level_file.read())
		level_file.close()

		Globals.in_menu = False


