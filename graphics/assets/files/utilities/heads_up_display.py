from assets.files.utilities.globals import Globals

import pygame
import math
import time


# Displays all overlaying boxes/dialogs/menu over the screen
class HeadsUpDisplay:

	# The different colors
	# In arrays, one value for each graphics level
	border_colors = [
		(192, 192, 192),
		(0, 0, 0),
		(192, 192, 192)
	]
	box_colors = [
		(64, 64, 64),
		(255, 255, 255),
		(64, 64, 64)
	]
	text_colors = [
		(192, 192, 192),
		(0, 0, 0),
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
	mb_is_showing = False

	mb_x = 0
	mb_y = 0
	mb_w = 0
	mb_h = 0

	mb_title_font = None
	mb_message_font = None

	mb_title = "Testing line in that :"

	# dl = Dialog
	dl_is_showing = False

	dl_x = 0
	dl_y = 0
	dl_w = 0
	dl_h = 0

	# the current index
	# which tet and image to draw
	dl_index = 0

	# Image offset and size
	dl_offset_left = 0
	dl_image_s = 0

	dl_padding = 0

	# The images and text
	dl_images = []
	dl_dialogs = []

	dl_font = None

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
		self.mb_w = math.floor((w[0] * (2/3)) / Globals.block_size) * Globals.block_size
		self.mb_h = math.floor((self.mb_w / Globals.block_size) * (3/4)) * Globals.block_size

		self.border_w = (Globals.block_size / Globals.pixels_per_block) * 2

		self.mb_x = (w[0] - self.mb_w) / 2
		self.mb_y = (w[1] - self.mb_h) / 2

		self.dl_x = 0
		self.dl_y = w[1] * (8/10)
		self.dl_w = w[0]
		self.dl_h = w[1] - self.dl_y

		self.dl_offset_left = int(self.dl_w * (1/10))
		self.dl_image_s = int(self.dl_h * (1/2))
		self.dl_padding = 10

		self.pm_w = w[0] * (1/3)
		self.pm_h = w[1] * (3/4)
		self.pm_x = (w[0] - self.pm_w) / 2
		self.pm_y = (w[1] - self.pm_h) / 2

		self.pm_padding = 20
		self.pm_button_h = 40

		font_url = "assets/fonts/Minecraftia-Regular.ttf"

		self.mb_title_font = pygame.font.Font(font_url, 30)
		self.mb_message_font = pygame.font.Font(font_url, 22)

		self.dl_font = pygame.font.Font(font_url, 20)

		self.pm_title_font = pygame.font.Font(font_url, 30)
		self.pm_button_font = pygame.font.Font(font_url, 22)

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

	# Displays a dialog box with the given dialog
	def dialog_box(self, dialogs, images):

		# Sets up the dialog box
		self.dl_is_showing = True
		Globals.is_paused = True
		self.dl_index = 0

		# Gets all the images
		for image in images:
			i = pygame.image.load("assets/images/props/dialogs/%s" % image).convert_alpha()
			i = pygame.transform.scale(i, (self.dl_image_s, self.dl_image_s))
			self.dl_images.append(i)

		# Gets all the text
		self.dl_dialogs = []
		while len(self.dl_dialogs) < len(dialogs):

			# Four strings for four lines
			self.dl_dialogs.append(['', '', '', ''])

		for d in range(len(dialogs)):
			# indexes for which word and which line
			word_index = 0
			line_index = 0

			dialog = dialogs[d]
			words = dialog.split(' ')

			while word_index < len(words):

				# Adds the word to the string, but not in the same variable
				line_str = self.dl_dialogs[d][line_index] + " " + words[word_index]

				# Finds the max width the line can have
				max_width = self.dl_w - (self.dl_x + self.dl_offset_left + self.dl_image_s + 2 * self.dl_padding)

				# If the word can fit on the line without exceeding the max width, add the word to the line
				# Otherwise create a new line
				if self.dl_font.size(line_str)[0] > max_width:
					line_index += 1
				else:
					self.dl_dialogs[d][line_index] = line_str
					word_index += 1

	# Draws Everything
	def render(self):

		# Gets window dimensions for easy reference
		win = Globals.window.get_size()

		# Draws Message Box
		if self.mb_is_showing:

			# Draws rectangles
			pygame.draw.rect(Globals.window, self.border_color, [
				self.mb_x - self.border_w, 
				self.mb_y - self.border_w, 
				self.mb_w + 2 * self.border_w,
				self.mb_h + 2 * self.border_w
			])
			pygame.draw.rect(Globals.window, self.box_color, [
				self.mb_x,
				self.mb_y,
				self.mb_w,
				self.mb_h
			])

			# Gets title coordinates
			x = (win[0] - self.mb_title_font.size(self.mb_title)[0])/2
			y = self.mb_y + 20
			# Prints title
			ren = self.mb_title_font.render(self.mb_title, False, self.text_color)
			Globals.window.blit(ren, (x, y))

			# Prints Message
			line_indent = 0

			x = self.mb_x + 5
			y = self.mb_y + self.mb_title_font.size(self.mb_title)[1] + 5

			for line in self.text_lines:

				# Draws each line
				ren = self.mb_message_font.render(line, False, self.text_color)
				Globals.window.blit(ren, (x, y + self.mb_message_font.size(line)[1] * line_indent))
				line_indent += 1

			# Draws <Press ENTER to continue> in the bottom right corner
			text = "Press ENTER to continue"
			x = self.mb_x + self.mb_w - self.mb_message_font.size(text)[0]
			y = self.mb_y + self.mb_h - self.mb_message_font.size(text)[1]

			r = self.dl_font.render(text, False, self.text_color)
			Globals.window.blit(r, (x, y))

		# Draws Dialog box
		elif self.dl_is_showing:

			# Draws Rectangles
			pygame.draw.rect(Globals.window, self.border_color, [
				self.dl_x, 
				self.dl_y - self.border_w,
				self.dl_w,
				self.border_w
			])
			pygame.draw.rect(Globals.window, self.box_color, [
				self.dl_x,
				self.dl_y, 
				self.dl_w,
				self.dl_h
			])

			# draws Image
			img_y = int(self.dl_y + (self.dl_h - self.dl_image_s) / 2)
			Globals.window.blit(self.dl_images[self.dl_index], (self.dl_offset_left, img_y))

			# Draws Dialog
			line_height = self.dl_font.get_linesize()
			base_x = self.dl_offset_left + self.dl_x + self.dl_image_s + 10

			for i in range(len(self.dl_dialogs[self.dl_index])):

				line = self.dl_dialogs[self.dl_index][i]
				r = self.dl_font.render(line, False, self.text_color)
				Globals.window.blit(r, (base_x, self.dl_y + self.dl_padding + line_height * i))

			# Draws <Press ENTER to continue>
			text = "Press ENTER to continue"
			x = self.dl_x + self.dl_w - self.dl_font.size(text)[0] - self.dl_padding
			y = self.dl_y + self.dl_h - self.dl_font.size(text)[1] - self.dl_padding

			r = self.dl_font.render(text, False, self.text_color)
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
			self.mb_is_showing = True

			# Which line
			line_index = 0

			self.mb_title = title
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
					and self.mb_message_font.size(self.text_lines[line_index] + words[word_index])[0] < (self.mb_w - 10):

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
		
		if self.mb_is_showing:
			if pygame.K_RETURN in keys:

				if self.should_fade_out:
					self.mb_is_showing = False
					self.is_fading_out = True
					Globals.music_fade_out = True
					self.fade_start_time = time.time()
				else:
					self.mb_is_showing = False
					Globals.is_paused = False

		elif self.dl_is_showing:

			if pygame.K_RETURN in keys:

				self.dl_index += 1
				if self.dl_index >= len(self.dl_dialogs):

					self.text_lines = [""]
					self.dl_is_showing = False
					Globals.is_paused = False
					self.dl_dialogs = []

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
				
			else:
				if pygame.K_ESCAPE in keys:
					self.pm_is_showing = True
					self.pm_selected_button = 0
					Globals.is_paused = True

		if pygame.K_d in keys and Globals.debug:
			self.mb_is_showing = False
			self.dl_is_showing = False
			self.pm_is_showing = False
			Globals.is_paused = False

	def resume(self):
		Globals.is_paused = False
		self.pm_is_showing = False

	def quit(self):
		Globals.in_menu = True

	# Creates the fade to block look
	def fade_out(self):

		# Sets up initially
		if self.rect_alpha is None:
			self.rect_alpha = 0
			Globals.music_fade_out = True

		window = pygame.Surface(Globals.window.get_size())
		window.set_alpha(self.rect_alpha)
		window.fill((0, 0, 0))
		Globals.window.blit(window, (0, 0))

		self.rect_alpha = int((time.time() - self.fade_start_time) * (255 / self.fade_duration))

		if self.rect_alpha > 255:
			self.is_fading_out = False
			Globals.is_paused = False
			Globals.graphics_level += 1
			Globals.music_fade_in = True
			Globals.in_menu = True

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
