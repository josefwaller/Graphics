from assets.files.utilities.globals import Globals

import pygame
import math
import sys

class HeadsUpDisplay ():

	border_color = (255, 255, 255)
	box_color = (0, 0, 0)
	text_color = (255, 255, 255)

	mb_is_showing = False

	mb_x = 0
	mb_y = 0
	mb_w = 0
	mb_h = 0

	border_w = 0

	text_lines = [""]

	mb_title_font = None
	mb_message_font = None

	mb_title = "Testing line_inthat :"

	dl_is_showing = False

	dl_x = 0
	dl_y = 0
	dl_w = 0
	dl_h = 0

	dl_index = 0

	dl_offset_left = 0
	dl_image_s = 0
	dl_padding = 0

	dl_images = []
	dl_dialogs = []

	dl_font = None

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

		w = Globals.window.get_size()

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

		pygame.font.init()

		font_url = "assets/fonts/Minecraftia-Regular.ttf"

		self.mb_title_font = pygame.font.Font(font_url, 30)
		self.mb_message_font = pygame.font.Font(font_url, 22)

		self.dl_font = pygame.font.Font(font_url, 20)

		self.pm_title_font = pygame.font.Font(font_url, 30)
		self.pm_button_font = pygame.font.Font(font_url, 22)

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

	def dialog_box (self, dialogs, images):

		self.dl_is_showing = True

		Globals.is_paused = True

		self.dl_index = 0

		for image in images:

			i = pygame.image.load(image).convert_alpha()
			i = pygame.transform.scale(i, (self.dl_image_s, self.dl_image_s))
			self.dl_images.append(i)

		self.dl_dialogs = []

		while len(self.dl_dialogs) < len(dialogs):
			#Four strings for four lines
			self.dl_dialogs.append(['', '', '', ''])

		for d in range(len(dialogs)):

			dialog = dialogs[d]
			words = dialog.split(' ')

			word_index = 0
			line_index = 0

			while word_index < len(words):

				line_str = self.dl_dialogs[d][line_index] + " " + words[word_index]
				max_width = self.dl_w - (self.dl_x + self.dl_offset_left + self.dl_image_s + 2 * self.dl_padding)

				if self.dl_font.size(line_str)[0] > max_width:
					line_index += 1
				else:
					self.dl_dialogs[d][line_index] = line_str
					word_index += 1

	def render (self):

		win = Globals.window.get_size()

		if self.mb_is_showing:

			#Draws rectangles

			pygame.draw.rect(Globals.window, self.border_color, [
				self.mb_x - self.border_w, 
				self.mb_y - self.border_w, 
				self.mb_w + 2 *self.border_w, 
				self.mb_h + 2 *self.border_w
			])

			pygame.draw.rect(Globals.window, self.box_color, [
				self.mb_x,
				self.mb_y,
				self.mb_w,
				self.mb_h
			])

			#Prints Title

			x = (win[0] - self.mb_title_font.size(self.mb_title)[0])/2
			y = self.mb_y + 20

			ren = self.mb_title_font.render(self.mb_title, False, self.text_color)
			Globals.window.blit(ren, (x, y))


			#Prints Message

			line_indent = 0

			x = self.mb_x + 5
			y = self.mb_y + self.mb_title_font.size(self.mb_title)[1] + 5

			for line in self.text_lines:

				ren = self.mb_message_font.render(line, False, self.text_color)

				Globals.window.blit(ren, (x, y + self.mb_message_font.size(line)[1] * line_indent))

				line_indent += 1


			text = "Press ENTER to continue"
			x = self.mb_x + self.mb_w - self.mb_message_font.size(text)[0]
			y = self.mb_y + self.mb_h - self.mb_message_font.size(text)[1]

			r = self.dl_font.render(text, False, self.text_color)
			Globals.window.blit(r, (x, y))

		elif self.dl_is_showing:

			#Draws Rectangles

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

			#draws Image

			img_y = int(self.dl_y + (self.dl_h - self.dl_image_s) / 2)
			Globals.window.blit(self.dl_images[self.dl_index], (self.dl_offset_left, img_y))

			#Draws Dialog

			line_height = self.dl_font.get_linesize()
			base_x = self.dl_offset_left + self.dl_x + self.dl_image_s + 10

			for i in range(len(self.dl_dialogs[self.dl_index])):

				line = self.dl_dialogs[self.dl_index][i]

				r = self.dl_font.render(line, False, self.text_color)

				Globals.window.blit(r, (base_x, self.dl_y + self.dl_padding + line_height * i))

			text = "Press ENTER to continue"
			x = self.dl_x + self.dl_w - self.dl_font.size(text)[0] - self.dl_padding
			y = self.dl_y + self.dl_h - self.dl_font.size(text)[1] - self.dl_padding

			r = self.dl_font.render(text, False, self.text_color)
			Globals.window.blit(r, (x, y))

		elif self.pm_is_showing:

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

			title_x = self.pm_x + (self.pm_w - self.pm_title_font.size("MENU")[0]) / 2
			title_y = self. pm_y + self.pm_padding
			r = self.pm_title_font.render("MENU", False, self.text_color)
			Globals.window.blit(r, (title_x, title_y))

			offset_y = self.pm_y + 2 * self.pm_padding + self.pm_title_font.size("MENU")[1]

			x = self.pm_x + self.pm_padding
			w = self.pm_w - 2 * self.pm_padding
			h = self.pm_button_h

			for i in range(len(self.pm_buttons)):

				button = self.pm_buttons[i]

				y = offset_y + (self.pm_button_h + self.pm_padding) * i - self.border_w

				if self.pm_selected_button == i:

					fill_color = self.border_color
					text_color = self.box_color

				else:

					fill_color = self.box_color
					text_color = self.text_color

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

	def message_box(self, title, message):

			Globals.is_paused = True

			self.mb_is_showing = True

			line_index = 0

			self.mb_title = title

			word_index = 1

			words = message.split(" ")

			self.text_lines[0] = words[0]

			create_new_line = True

			while create_new_line:

				create_new_line = False

				while  len(words) - 1 >= word_index and self.mb_message_font.size(self.text_lines[line_index] + words[word_index])[0] < (self.mb_w - 10):

					create_new_line = True

					if words[word_index] == "\n":
						word_index += 1
						break

					self.text_lines[line_index] += "  %s" % words[word_index]

					word_index += 1

			#Adds a new line

				try:
					self.text_lines[line_index + 1]
				except IndexError:
					self.text_lines.append("")

				line_index += 1

	def on_input (self, keys):
		
		if self.mb_is_showing:
			if pygame.K_RETURN in keys:

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

	def resume (self):
		Globals.is_paused = False
		self.pm_menu_is_Showing = False

	def quit (self):
		pygame.exit()
		sys.exit()