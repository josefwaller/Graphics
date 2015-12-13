from assets.files.utilities.globals import Globals
from assets.files.utilities.level_reader import LevelReader

import pygame
import json
import time
import sys


class MainMenu:
	# The logo image
	logo = None

	# Logo coords
	logo_x = 0
	logo_y = 0

	# Graphics level to compare with globals
	graphics_level = 0

	# Sky image, coords, speed and last time it moved
	sky = None
	sky_x = 0
	sky_speed = 20
	sky_last_time = 0

	# Different colors for different graphics levels
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

	# The colors currently being used
	color_one = None
	color_two = None

	# Font file url
	font_file_url = "assets/fonts/Minecraftia-Regular.ttf"

	border_width = 0

	# Fading variables
	fade_in = True
	fade_out = False
	fade_alpha = 0
	fade_duration = 0.5
	fade_start_time = 0

	# Settings variables
	is_showing_settings = False

	# The settings, to be saved to file

	# Different FPS
	fps = [
		20,
		40,
		60,
		80
	]

	# The music volume
	volume = 0
	volume_index = 0

	# The different available resolutions
	# Note they all have the same ratio of 1:3/4
	resolutions = [
		[
			800,
			600
		],
		[
			1000,
			750
		],
		[
			1200,
			900
		],
		[
			1400,
			1050
		],
		[
			0,
			0
		]
	]
	# The indexes
	resolution_index = 0
	fps_index = 0

	# The buttons
	buttons = []
	# Index of selected button
	selected_button = 0

	# Settings screen coordinates/scale

	# The displacement because of the logo
	offset_y = 0
	# The height each option has
	height_each = 0

	# the text positioning
	text_x = 0
	text_font = 0

	option_font = None

	# X and width of the buttons
	button_x = 0
	button_w = 0
	button_h = 0

	# The buttons for Save and Cancel
	bottom_button_h = 0
	bottom_button_w = 0

	selected_setting = 0

	bottom_font = None
	bottom_selected = 0

	def __init__(self):

		# Sets graphics level
		self.graphics_level = Globals.graphics_level

		# Loads images
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

		# Gets window size for easy reference
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
				"text": "SETTINGS",
				"on_click": self.show_settings
			},
			{
				"text": "QUIT",
				"on_click": self.quit
			}
		]

		# Sets button dimensions

		self.b_min_y = w[1] / 2

		self.b_w = w[0] / 5
		self.b_h = (w[1] - self.b_min_y) / (2 * len(self.buttons))

		self.b_x = (w[0] - self.b_w) / 2

		self.b_border_w = Globals.block_size / Globals.pixels_per_block

		self.b_font = pygame.font.Font("assets/fonts/Minecraftia-Regular.ttf", 20)

		self.set_up()

	# Called when the graphics level is not the same as the Globals graphics level
	def set_up(self):

		# Gets window dimensions for easy reference
		w = Globals.window.get_size()

		# Sets graphics level
		self.graphics_level = Globals.graphics_level

		# Sets up sky
		self.sky_last_time = time.time()

		# Sets logo and sky images
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

		# Gets the button colors
		self.color_one = self.colors_one[Globals.graphics_level]
		self.color_two = self.colors_two[Globals.graphics_level]

		# Sets the selected button to continues
		self.selected_button = 0

		self.border_width = int(Globals.block_size / Globals.pixels_per_block)

		# Sets the settings screen dimensions
		self.offset_y = self.logo_y + (self.logo.get_size()[1]) * 2

		self.height_each = (w[1] - self.offset_y) / 4

		self.text_font = self.get_font_by_height(self.font_file_url, self.height_each * 1 / 4)
		self.option_font = self.get_font_by_height(self.font_file_url, self.height_each * 1 / 2)
		self.bottom_font = self.get_font_by_height(self.font_file_url, self.height_each * (1 / 5))

		self.button_w = (w[0] * 2 / 3) * 1 / 2
		self.button_x = (w[0] * 1 / 3) + ((w[0] * 2 / 3) - self.button_w) / 2
		self.button_h = self.height_each * 4 / 5

		self.bottom_button_h = self.height_each * (3 / 4)
		self.bottom_button_w = (w[0] / 2) / 3

		self.selected_setting = 0

		self.volume = range(11)

		self.volume_index = int(Globals.volume * 10)

	def update(self):

		# Checks if it should set up again
		if not self.graphics_level == Globals.graphics_level:
			self.set_up()

		# Moves sky and renders
		self.move_sky()
		self.render()

	def move_sky(self):
		# Gets the sky size
		s = self.sky.get_size()

		# Gets delta time
		delta_time = time.time() - self.sky_last_time

		# Moves the sky
		self.sky_x -= self.sky_speed * delta_time

		# Checks if the sky should be moved back
		if self.sky_x <= 0 - s[0]:
			self.sky_x += s[0]

		# Sets last time
		self.sky_last_time = time.time()

	def on_input(self, keys):

		if pygame.K_RETURN in keys:
			if not self.fade_in and not self.fade_out and not self.is_showing_settings:
				self.buttons[self.selected_button]['on_click']()
			elif self.is_showing_settings:
				if self.selected_setting == 3:
					# Save and Cancel buttons
					if self.bottom_selected == 0:
						self.save_settings()
						self.is_showing_settings = False
					else:
						self.is_showing_settings = False

		elif pygame.K_UP in keys:
			if not self.is_showing_settings and self.selected_button >= 1:
				self.selected_button -= 1
			elif self.is_showing_settings and self.selected_setting > 0:
				self.selected_setting -= 1

		elif pygame.K_DOWN in keys:
			if not self.is_showing_settings and self.selected_button <= len(self.buttons) - 2:
				self.selected_button += 1
			elif self.is_showing_settings and self.selected_setting < 3:
				self.selected_setting += 1
		elif pygame.K_LEFT in keys or pygame.K_RIGHT in keys:
			if self.is_showing_settings:
				if pygame.K_LEFT in keys:
					increment = -1
				else:
					increment = 1

				setting = None
				setting_index = 0

				if self.selected_setting == 0:
					setting = self.resolutions
					setting_index = self.resolution_index
				elif self.selected_setting == 1:
					setting = self.fps
					setting_index = self.fps_index
				elif self.selected_setting == 2:
					setting = self.volume
					setting_index = self.volume_index
				else:
					if increment + self.bottom_selected >= 0 and increment + self.bottom_selected < 2:
						self.bottom_selected += increment
					return

				if setting_index + increment >= 0 and setting_index + increment <= len(setting) - 1:

					if self.selected_setting == 0:
						self.resolution_index += increment

					elif self.selected_setting == 1:
						self.fps_index += increment

					else:
						self.volume_index += increment

	def render(self):

		Globals.window.blit(self.sky, (self.sky_x, 0))
		Globals.window.blit(self.sky, (self.sky_x + self.sky.get_size()[0], 0))
		Globals.window.blit(self.logo, (self.logo_x, self.logo_y))

		if self.is_showing_settings:

			texts = [
				{
					"text": "Resolution*",
					"type": "resolution"
				},
				{
					"text": "Frames per second*",
					"type": "fps"
				},
				{
					"text": "Volume",
					"type": "volume"
				}
			]

			for i in range(len(texts)):

				text = texts[i]['text'].upper()

				x = (Globals.window.get_size()[0] * 1 / 3 - self.text_font.size(text)[0]) / 2
				y = self.offset_y + (self.height_each - self.text_font.get_height()) / 2 + self.height_each * i

				r = self.text_font.render(text, False, (0, 0, 0))
				Globals.window.blit(r, (x, y))

				# Draws options

				x = self.button_x
				y = self.offset_y + self.height_each * i
				w = self.button_w
				h = self.button_h

				if self.selected_setting == i:
					color_one = self.color_two
					color_two = self.color_one
				else:
					color_one = self.color_one
					color_two = self.color_two

				pygame.draw.rect(Globals.window, color_one, [
					x,
					y,
					w,
					h
				])

				pygame.draw.rect(Globals.window, color_two, [
					x,
					y,
					w,
					h
				], self.border_width)

				# Draws text

				text = ""

				if texts[i]['type'].lower() == "resolution":
					if self.resolutions[self.resolution_index][0] == 0:
						text = "Fullscreen"
					else:
						text = "%sx%s" % (
							self.resolutions[self.resolution_index][0], self.resolutions[self.resolution_index][1])
					index = self.resolution_index
					max_index = len(self.resolutions) - 1

				elif texts[i]['type'].lower() == "fps":
					text = str(self.fps[self.fps_index])
					index = self.fps_index
					max_index = len(self.fps) - 1

				elif texts[i]['type'].lower() == "volume":
					text = "%s" % int(self.volume[self.volume_index] * 10)
					text += "%"
					index = self.volume_index
					max_index = len(self.volume) - 1

				text_x = x + (w - self.option_font.size(text)[0]) / 2
				text_y = y + (h - self.option_font.get_height()) / 2

				r = self.option_font.render(text, False, color_two)
				Globals.window.blit(r, (text_x, text_y))

				if index == 0:
					left_arrow = False
				else:
					left_arrow = True

				if index == max_index:
					right_arrow = False
				else:
					right_arrow = True

				# Draws triangles

				triangle_top = y + (h * 1 / 6)
				triangle_bot = y + (h * 5 / 6)
				triangle_mid = y + (h * 1 / 2)
				triangle_offset = 3 * self.border_width
				triangle_w = triangle_bot - triangle_top

				if right_arrow:
					pygame.draw.polygon(Globals.window, color_one, [
						(x + w + triangle_offset, triangle_top),
						(x + w + triangle_offset, triangle_bot),
						(x + w + triangle_offset + triangle_w, triangle_mid)
					])

					pygame.draw.polygon(Globals.window, color_two, [
						(x + w + triangle_offset, triangle_top),
						(x + w + triangle_offset, triangle_bot),
						(x + w + triangle_offset + triangle_w, triangle_mid)
					], self.border_width)

				if left_arrow:
					pygame.draw.polygon(Globals.window, color_one, [
						(x - triangle_offset, triangle_top),
						(x - triangle_offset, triangle_bot),
						(x - triangle_offset - triangle_w, triangle_mid)
					])
					pygame.draw.polygon(Globals.window, color_two, [
						(x - triangle_offset, triangle_top),
						(x - triangle_offset, triangle_bot),
						(x - triangle_offset - triangle_w, triangle_mid)
					], self.border_width)

			# draws bottom text
			text = "*the game will need to restart to take effect"
			offset_y = self.offset_y + 3 * self.height_each
			x = (Globals.window.get_size()[0] - self.bottom_font.size(text)[0]) / 2
			y = (self.height_each / 8 - self.bottom_font.get_height()) / 2
			r = self.bottom_font.render(text, False, self.color_two)
			Globals.window.blit(r, (x, offset_y + y))

			# Draws bottom save/cancel button

			for i in range(2):
				y = self.offset_y + 3 * self.height_each + self.bottom_font.get_height()
				x = (Globals.window.get_size()[0] * (3 / 4) - self.bottom_button_w) / 2 + Globals.window.get_size()[
																							  0] * (i / 4)

				color_one = self.color_one
				color_two = self.color_two

				if self.selected_setting == 3:
					if self.bottom_selected == i:
						color_one = self.color_two
						color_two = self.color_one
				pygame.draw.rect(Globals.window, color_one, [
					x,
					y,
					self.bottom_button_w,
					self.bottom_button_h
				])
				pygame.draw.rect(Globals.window, color_two, [
					x,
					y,
					self.bottom_button_w,
					self.bottom_button_h
				], self.border_width)

				# Draws text on buttons
				if i == 0:
					text = "Save".upper()
				else:
					text = "Cancel".upper()
				text_x = x + (self.bottom_button_w - self.bottom_font.size(text)[0]) / 2
				text_y = y + (self.bottom_button_h - self.bottom_font.get_height()) / 2
				r = self.bottom_font.render(text, False, color_two)
				Globals.window.blit(r, (text_x, text_y))

		else:
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
					Globals.music_fade_in = True

	def save_settings(self):
		file = open("assets/settings/settings.json", "r+")
		old_settings = json.loads(file.read())
		file.close()

		to_save = old_settings.copy()
		to_save["fps"] = self.fps[self.fps_index]
		to_save['screen_width'] = self.resolutions[self.resolution_index][0]
		to_save['screen_height'] = self.resolutions[self.resolution_index][1]

		file = open("assets/settings/settings.json", "w")
		file.write(json.dumps(to_save))
		file.close()

	def resume(self):

		# loads level
		level_file = open("assets/levels/l%s.json" % (Globals.graphics_level + 1), "r")
		r = LevelReader()
		r.read_level(level_file.read())
		level_file.close()

		self.fade_out = True
		Globals.music_fade_out = True
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
		Globals.music_fade_out = True
		self.fade_alpha = 0
		self.fade_start_time = time.time()

	@staticmethod
	def quit():
		pygame.quit()
		sys.exit()

	def show_settings(self):

		self.is_showing_settings = True

		file = open("assets/settings/settings.json", "r")
		settings = json.loads(file.read())
		file.close()

		# Loads the current FPS and resolution

		for i in range(len(self.fps)):
			if settings['fps'] == self.fps[i]:
				self.fps_index = i
				break

		for i in range(len(self.resolutions)):
			if settings['screen_width'] == self.resolutions[i][0]:
				if settings['screen_height'] == self.resolutions[i][1]:
					self.resolution_index = i
					break

		self.selected_setting = 0

	@staticmethod
	def get_font_by_height(url, height):

		h = int(height)
		font = pygame.font.Font(url, h)

		while font.get_height() > height:
			h -= 1
			font = pygame.font.Font(url, h)

		return font
