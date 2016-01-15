from assets.files.utilities.globals import Globals

import pygame
import math
import time
import json


# Displays all overlaying boxes/dialogs/menu over the screen
class HeadsUpDisplay:

	# The different colors
	# In arrays, one value for each graphics level
	border_colors = [
		(192, 192, 192),
		(255, 255, 255),
		(192, 192, 192)
	]
	box_colors = [
		(64, 64, 64),
		(0, 0, 0),
		(64, 64, 64)
	]
	text_colors = [
		(192, 192, 192),
		(255, 255, 255),
		(192, 192, 192)
	]

	# Rectangle used for fading in/out
	rect_alpha = None
	fade_duration = 0.5
	fade_start_time = 0
	is_fading_out = False
	should_fade_out = False
	should_fade_in = False

	# Width of border
	border_w = 0

	# The lines of text
	# Used in all of mb, dl and pm
	text_lines = [""]

	# mb = Message Box
	# Different values for the message box
	mb = {
		"is_showing": False,
		"x": 0,
		"y": 0,
		"w": 0,
		"h": 0,
		"title_font": None,
		"message_font": None,
		"title": None
	}

	# dl = Dialog
	dl = {
		'is_showing': False,
		'x': 0,
		'y': 0,
		'w': 0,
		'h': 0,

		# the current index
		# which text and image to draw
		'index': 0,
		# Image offset and size
		'offset_left': 0,
		'image_s': 0,
		'padding': 0,
		# The images and text
		'images': [],
		'dialogs': [],
		'font': None
	}

	# pm = Pause Menu
	pm_is_showing = False

	pm_x = 0
	pm_y = 0
	pm_w = 0
	pm_h = 0

	pm_padding = 0
	pm_selected_button = 0

	pm_button_h = 0

	pm_title_font = None
	pm_button_font = None

	# Variables used in the credits
	showing_credits = False
	credit_time = 0
	credit_text = 0
	credit_gap = 0
	credit_start_time = 0
	credit_font = None
	credit_images = []
	credit_image_height = 0
	sprite_interval = 0.5
	credits_done = False

	def __init__(self):

		# Initializes the pygame font module
		pygame.font.init()

		# sets the colors according to the graphics level
		self.box_color = self.box_colors[Globals.graphics_level]
		self.text_color = self.text_colors[Globals.graphics_level]
		self.border_color = self.border_colors[Globals.graphics_level]

		# BGets window size for easy reference
		w = Globals.window.get_size()

		# Sets different dimensions/values for pm, dl and mb
		self.mb['w'] = math.floor((w[0] * (2/3)) / Globals.block_size) * Globals.block_size
		self.mb['h'] = math.floor((self.mb['w'] / Globals.block_size) * (3/4)) * Globals.block_size

		self.border_w = (Globals.block_size / Globals.pixels_per_block)

		self.mb['x'] = (w[0] - self.mb['w']) / 2
		self.mb['y'] = (w[1] - self.mb['h']) / 2

		self.dl['x'] = 0
		self.dl['y'] = w[1] * (8/10)
		self.dl['w'] = w[0]
		self.dl['h'] = w[1] - self.dl['y']

		self.dl['offset_left'] = int(self.dl['w'] * (1/10))
		self.dl['image_s'] = int(self.dl['h'] * (1/2))
		self.dl['padding'] = 10

		self.pm_w = w[0] * (1/3)
		self.pm_h = w[1] * (3/4)
		self.pm_x = (w[0] - self.pm_w) / 2
		self.pm_y = (w[1] - self.pm_h) / 2

		self.pm_padding = 20
		self.pm_button_h = self.pm_h / 8

		font_url = "assets/fonts/Minecraftia-Regular.ttf"

		self.mb['title_font'] = Globals.get_font_by_height(font_url, int(self.mb['h'] / 6))
		self.mb['message_font'] = Globals.get_font_by_height(font_url, int(self.mb['h'] / 15))

		self.dl['font'] = Globals.get_font_by_height(font_url, int(self.dl['h'] / 5))

		self.pm_title_font = Globals.get_font_by_height(font_url, int(self.pm_h / 10))
		self.pm_button_font = Globals.get_font_by_height(font_url, int(self.pm_button_h * (3/4)))

		# Sets up the buttons
		self.pm_buttons = [
			{
				"text": "RESUME",
				"on_click": self.resume
			},
			{
				"text": "EXIT",
				"on_click": self.quit
			}
		]

		self.is_fading_in = True
		self.fade_start_time = None

		self.credit_gap = 3 * Globals.block_size
		self.credit_time = 45
		self.credit_font = Globals.get_font_by_height(font_url, 40)
		self.showing_credits = False
		self.credit_surface = None

	# Displays a dialog box with the given dialog
	def dialog_box(self, dialogs, images):

		# Sets up the dialog box
		self.dl['is_showing'] = True
		Globals.is_paused = True
		self.dl['index'] = 0
		self.dl['images'] = []

		# Gets all the images
		for image in images:
			i = pygame.image.load("assets/images/props/dialogs/%s" % image).convert_alpha()
			i = pygame.transform.scale(i, (self.dl['image_s'], self.dl['image_s']))
			self.dl['images'].append(i)

		# Gets all the text
		self.dl['dialogs'] = []
		while len(self.dl['dialogs']) < len(dialogs):

			# Four strings for four lines
			self.dl['dialogs'].append(['', '', '', ''])

		for d in range(len(dialogs)):
			# indexes for which word and which line
			word_index = 0
			line_index = 0

			dialog = dialogs[d]
			words = dialog.split(' ')

			while word_index < len(words):

				# Adds the word to the string, but not in the same variable
				line_str = self.dl['dialogs'][d][line_index] + "  " + words[word_index]

				# Finds the max width the line can have
				max_width = self.dl['w'] - (self.dl['x'] + self.dl['offset_left'] + self.dl['image_s'] + 2 * self.dl['padding'])

				# If the word can fit on the line without exceeding the max width, add the word to the line
				# Otherwise create a new line
				if self.dl['font'].size(line_str)[0] > max_width:
					line_index += 1
				else:
					self.dl['dialogs'][d][line_index] = line_str
					word_index += 1

	# Sets up the credits
	def show_credits(self):
		file = open("assets/dialog/credits.json", "r")
		credits = json.loads(file.read())
		file.close()

		self.credit_text = credits['text'].copy()
		self.credit_images = credits['images'].copy()
		self.credit_image_height = 3 * Globals.block_size

		Globals.playing_credits = True

		for i in range(len(self.credit_images)):

			x = 0
			image = pygame.image.load("assets/images/%s" % self.credit_images[i][x]).convert_alpha()
			s = image.get_size()
			h = self.credit_image_height
			w = int(s[0] / s[1] * h)

			for x in range(len(self.credit_images[i])):
				self.credit_images[i][x] = pygame.image.load("assets/images/%s" % self.credit_images[i][x]).convert_alpha()
				self.credit_images[i][x] = pygame.transform.scale(self.credit_images[i][x], (w, h))

		self.credit_start_time = time.time()
		self.is_fading_out = True
		self.rect_alpha = 0
		self.fade_start_time = time.time()
		self.credits_done = False

		height = 0

		height += (self.credit_font.get_height() + self.credit_gap) * len(self.credit_text)

		height += (self.credit_image_height + self.credit_gap) * len(self.credit_images)

		self.credit_surface = pygame.Surface((Globals.window.get_size()[0], int(height)))

		for i in range(len(self.credit_text)):
			text = self.credit_text[i]
			r = self.credit_font.render(text, False, (255, 255, 255))
			x = (Globals.window.get_size()[0] - self.credit_font.size(text)[0]) / 2
			y = (self.credit_font.get_height() + self.credit_gap + self.credit_image_height + self.credit_gap) * i + self.credit_gap + self.credit_font.get_height()
			self.credit_surface.blit(r, (int(x), int(y)))

	# Draws Everything
	def render(self):

		# Gets window dimensions for easy reference
		win = Globals.window.get_size()

		if Globals.playing_credits:
			# checks if it is fading into the credits or into the menu
			if self.is_fading_out:
				if self.credits_done:
					# Fades into menu
					Globals.menu_fade_in = True
					self.fade_out()
				else:
					# Fades into credits
					self.fade_out(False)
					return

			# Checks if it should draw te credits
			if not self.is_fading_out or self.credits_done:
				# Draws background
				black = (0, 0, 0)
				pygame.draw.rect(Globals.window, black, [0, 0, win[0], win[1]])

				# Gets the time since
				time_since = time.time() - self.credit_start_time

				# Gets an editable version of the surface with the text already on it
				sur = self.credit_surface.copy()

				# Blits the images onto the surface
				for i in range(len(self.credit_images)):
					# Gets the index
					rounded_time = round(time_since, 1)
					time_since_change = rounded_time % (len(self.credit_images[i]) * self.sprite_interval)
					index = int(time_since_change / self.sprite_interval)

					# Gets the x and y coordinates
					x = (win[0] - self.credit_images[i][index].get_size()[0]) / 2
					y = i * (self.credit_image_height + 2 * self.credit_gap + self.credit_font.get_height())

					# Blits onto surface
					sur.blit(self.credit_images[i][index], (x, y))

				# blits sur onto the window with an offset depending on time
				# Makes the credits roll up the screen
				y = win[1] - (time_since / self.credit_time) * sur.get_size()[1]
				Globals.window.blit(sur, (0, y))

				# Checks if the credits are done
				if sur.get_size()[1] + y < win[1] and not self.credits_done:
					self.credits_done = True
					self.is_fading_out = True
					self.fade_start_time = time.time()

		# Draws Message Box
		if self.mb['is_showing']:

			# Draws rectangles
			pygame.draw.rect(Globals.window, self.border_color, [
				self.mb['x'] - self.border_w, 
				self.mb['y'] - self.border_w, 
				self.mb['w'] + 2 * self.border_w,
				self.mb['h'] + 2 * self.border_w
			])
			pygame.draw.rect(Globals.window, self.box_color, [
				self.mb['x'],
				self.mb['y'],
				self.mb['w'],
				self.mb['h']
			])

			# Gets title coordinates
			x = (win[0] - self.mb['title_font'].size(self.mb['title'])[0])/2
			y = self.mb['y'] + 20
			# Prints title
			ren = self.mb['title_font'].render(self.mb['title'], False, self.text_color)
			Globals.window.blit(ren, (x, y))

			# Prints Message
			line_indent = 0

			x = self.mb['x'] + 5
			y = self.mb['y'] + self.mb['title_font'].size(self.mb['title'])[1] + 5

			for line in self.text_lines:

				# Draws each line
				ren = self.mb['message_font'].render(line, False, self.text_color)
				Globals.window.blit(ren, (x, y + self.mb['message_font'].size(line)[1] * line_indent))
				line_indent += 1

			# Draws <Press ENTER to continue> in the bottom right corner
			text = "Press ENTER to continue"
			x = self.mb['x'] + self.mb['w'] - self.mb['message_font'].size(text)[0]
			y = self.mb['y'] + self.mb['h'] - self.mb['message_font'].size(text)[1]

			r = self.dl['font'].render(text, False, self.text_color)
			Globals.window.blit(r, (x, y))

		# Draws Dialog box
		elif self.dl['is_showing']:

			# Draws Rectangles
			pygame.draw.rect(Globals.window, self.border_color, [
				self.dl['x'], 
				self.dl['y'] - self.border_w,
				self.dl['w'],
				self.border_w
			])
			pygame.draw.rect(Globals.window, self.box_color, [
				self.dl['x'],
				self.dl['y'], 
				self.dl['w'],
				self.dl['h']
			])

			# draws Image
			img_y = int(self.dl['y'] + (self.dl['h'] - self.dl['image_s']) / 2)
			Globals.window.blit(self.dl['images'][self.dl['index']], (self.dl['offset_left'], img_y))

			# Draws Dialog
			line_height = self.dl['font'].get_linesize()
			base_x = self.dl['offset_left'] + self.dl['x'] + self.dl['image_s'] + 10

			for i in range(len(self.dl['dialogs'][self.dl['index']])):

				line = self.dl['dialogs'][self.dl['index']][i]
				r = self.dl['font'].render(line, False, self.text_color)
				Globals.window.blit(r, (base_x, self.dl['y'] + self.dl['padding'] + line_height * i))

			# Draws <Press ENTER to continue>
			text = "Press ENTER to continue"
			x = self.dl['x'] + self.dl['w'] - self.dl['font'].size(text)[0] - self.dl['padding']
			y = self.dl['y'] + self.dl['h'] - self.dl['font'].size(text)[1] - self.dl['padding']

			r = self.dl['font'].render(text, False, self.text_color)
			Globals.window.blit(r, (x, y))

		# Draws pause menu
		elif self.pm_is_showing:

			# Draws rectangles
			pygame.draw.rect(Globals.window, self.border_color, [
				self.pm_x - self.border_w,
				self.pm_y - self.border_w,
				self.pm_w + 2 * self.border_w,
				self.pm_h + 2 * self.border_w
			])
			pygame.draw.rect(Globals.window, self.box_color, [
				self.pm_x,
				self.pm_y,
				self.pm_w,
				self.pm_h
			])

			# Gets the title coordinates and draws the title
			title_x = self.pm_x + (self.pm_w - self.pm_title_font.size("MENU")[0]) / 2
			title_y = self. pm_y + self.pm_padding
			r = self.pm_title_font.render("MENU", False, self.text_color)
			Globals.window.blit(r, (title_x, title_y))

			# Gets the button offset due to the menu title
			offset_y = self.pm_y + 2 * self.pm_padding + self.pm_title_font.size("MENU")[1]

			# Gets button coordinates except y, because it will change with each button
			x = self.pm_x + self.pm_padding
			w = self.pm_w - 2 * self.pm_padding
			h = self.pm_button_h

			for i in range(len(self.pm_buttons)):

				# Draws buttons
				button = self.pm_buttons[i]
				y = offset_y + (self.pm_button_h + self.pm_padding) * i - self.border_w

				# Inverses the colors if the button is selected
				if self.pm_selected_button == i:

					fill_color = self.border_color
					text_color = self.box_color

				else:

					fill_color = self.box_color
					text_color = self.text_color

				# Draws the buttons
				pygame.draw.rect(Globals.window, self.border_color, [
					x - self.border_w,
					y - self.border_w,
					w + 2 * self.border_w,
					h + 2 * self.border_w
				])
				pygame.draw.rect(Globals.window, fill_color, [
					x,
					y,
					w,
					h
				])

				text_x = x + (w - self.pm_button_font.size(button['text'])[0]) / 2
				text_y = y + (h - self.pm_button_font.get_height()) / 2

				r = self.pm_button_font.render(button['text'], False, text_color)
				Globals.window.blit(r, (text_x, text_y))

		# Checks if it needs to fade out
		elif self.is_fading_out:
			self.fade_out()
		elif self.is_fading_in:
			self.fade_in()

	# Shows a message box with a given message
	def message_box(self, title, message, fade_out=False):

			Globals.is_paused = True
			self.mb['is_showing'] = True

			# Which line
			line_index = 0

			self.mb['title'] = title
			self.text_lines = ["", "", "", ""]
			word_index = 1

			# Checks whether the box should fade out when done
			self.should_fade_out = fade_out

			words = message.split(" ")

			self.text_lines[0] = words[0]
			create_new_line = True

			while create_new_line:

				create_new_line = False

				while len(words) - 1 >= word_index \
					and self.mb['message_font'].size(self.text_lines[line_index] + words[word_index])[0] < (self.mb['w'] - 10):

					create_new_line = True

					if words[word_index] == "\n":
						word_index += 1
						break

					self.text_lines[line_index] += "  %s" % words[word_index]

					word_index += 1

			# Adds a new line

				try:
					self.text_lines[line_index + 1]
				except IndexError:
					self.text_lines.append("")

				line_index += 1

	def on_input(self, keys):

		if not Globals.playing_credits:
		
			if self.mb['is_showing']:
				if pygame.K_RETURN in keys:

					if self.should_fade_out:
						self.mb['is_showing'] = False
						self.is_fading_out = True
						Globals.music_fade_out = True
						self.fade_start_time = time.time()
					else:
						self.mb['is_showing'] = False
						Globals.is_paused = False

			elif self.dl['is_showing']:

				if pygame.K_RETURN in keys:

					self.dl['index'] += 1
					if self.dl['index'] >= len(self.dl['dialogs']):

						self.text_lines = [""]
						self.dl['is_showing'] = False
						Globals.is_paused = False
						self.dl['dialogs'] = []

			else:
				if self.pm_is_showing:

					if pygame.K_RETURN in keys:
						self.pm_buttons[self.pm_selected_button]['on_click']()
						self.pm_is_showing = False

					elif pygame.K_UP in keys:
						if self.pm_selected_button >= 1:
							self.pm_selected_button -= 1
					elif pygame.K_DOWN in keys:
						if self.pm_selected_button < len(self.pm_buttons) - 1:
							self.pm_selected_button += 1

				if pygame.K_ESCAPE in keys:

					if self.pm_is_showing:
						self.pm_is_showing = False
						Globals.is_paused = False
					else:
						self.pm_is_showing = True
						self.pm_selected_button = 0
						Globals.is_paused = True

			if pygame.K_d in keys and Globals.debug:
				self.mb['is_showing'] = False
				self.dl['is_showing'] = False
				self.pm_is_showing = False
				Globals.is_paused = False

	def resume(self):
		Globals.is_paused = False
		self.pm_is_showing = False

	def quit(self):
		Globals.in_menu = True

	# Creates the fade to block look
	def fade_out(self, update_graphics=True):

		# Sets up initially
		if self.rect_alpha is None:
			self.rect_alpha = 0
			Globals.music_fade_out = True

		window = pygame.Surface(Globals.window.get_size())
		window.set_alpha(self.rect_alpha)
		window.fill((0, 0, 0))
		Globals.window.blit(window, (0, 0))

		self.rect_alpha = int((time.time() - self.fade_start_time) * (255 / self.fade_duration))

		# Checks if it is done fading
		if self.rect_alpha > 255:
			self.is_fading_out = False

			if update_graphics:
				# Changes to main menu
				Globals.is_paused = False
				# Updates graphics if nessecary
				if Globals.graphics_level < 2:
					Globals.graphics_level += 1
				# Sets music to fade in
				Globals.menu_fade_in = True
				Globals.in_menu = True

			else:
				# Pauses game for credits
				Globals.is_paused = True

	def fade_in(self):

		if self.rect_alpha is None:
			self.rect_alpha = 255

		if self.fade_start_time is None:
			self.fade_start_time = time.time()

		rect = pygame.Surface(Globals.window.get_size())
		rect.set_alpha(self.rect_alpha)
		rect.fill((0, 0, 0))
		Globals.window.blit(rect, (0, 0))

		self.rect_alpha = 255 - int((time.time() - self.fade_start_time) * (255 / self.fade_duration))
		if self.rect_alpha < 0:
			self.is_fading_in = False