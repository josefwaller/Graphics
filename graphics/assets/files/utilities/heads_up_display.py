from assets.files.utilities.globals import Globals

import pygame
import math

class HeadsUpDisplay ():

	border_color = (65, 65, 65)
	box_color = (128, 128, 128)
	text_color = (187, 187, 187)

	mb_is_showing = False

	mb_x = 0
	mb_y = 0
	mb_w = 0
	mb_h = 0

	mb_border_w = 0

	text_lines = [""]

	mb_title_font = None
	mb_message_font = None

	mb_title = "Testing line_inthat :"

	dl_is_showing = False

	dl_x = 0
	dl_y = 0
	dl_w = 0
	dl_h = 0

	dl_border_w = 0

	dl_index = 0

	dl_offset_left = 0
	dl_image_s = 0

	dl_images = []
	dl_dialogs = []

	dl_font = None

	dl_font = None
	def __init__(self):

		w = Globals.window.get_size()

		self.mb_w = math.floor((w[0] * (2/3)) / Globals.block_size) * Globals.block_size
		self.mb_h = math.floor((self.mb_w / Globals.block_size) * (3/4)) * Globals.block_size

		self.mb_border_w = (Globals.block_size / Globals.pixels_per_block) * 2

		self.mb_x = (w[0] - self.mb_w) / 2
		self.mb_y = (w[1] - self.mb_h) / 2

		self.dl_x = 0
		self.dl_y = w[1] * (9/10)
		self.dl_w = w[0]
		self.dl_h = w[1] - self.dl_y

		self.dl_border_w = 2
		self.dl_offset_left = int(self.dl_w * (1/10))
		self.dl_image_s = int(self.dl_h * (1/2))

		pygame.font.init()

		font_url = "assets/fonts/Minecraftia-Regular.ttf"

		self.mb_title_font = pygame.font.Font(font_url, int(self.mb_h / 9))
		self.mb_message_font = pygame.font.Font(font_url, int(self.mb_h / 13))

		self.dl_font = pygame.font.Font(font_url, int(self.dl_h / 5))

	def dialog_box (self, dialogs, images):

		self.dl_is_showing = True

		self.dl_index = 0

		for image in images:

			i = pygame.image.load(image).convert_alpha()
			i = pygame.transform.scale(i, (self.dl_image_s, self.dl_image_s))
			self.dl_images.append(i)

		for i in range(len(dialogs)):

			words = dialogs[i].split(" ")

			try:
				self.dl_dialogs[i] = [""]
			except IndexError:
				self.dl_dialogs.append("")

		for i in range(len(self.dl_dialogs)):
			for x in range(4):
				try:
					self.dl_dialogs[i][x] = ""
				except IndexError:
					self.dl_dialogs[i].append("")

		for i in range(len(self.dl_dialogs))

			line = 0

			for word in words:

				if not self.dl_font.size(self.dl_dialogs[i][line] + " " + word) < self.dl_h - self.dl_offset_left - self.dl_image_s - 20:
					line += 1

				self.dl_dialogs[i][line] += " %s" % word

	def render (self):

		if self.mb_is_showing:

			pygame.draw.rect(Globals.window, self.border_color, [
				self.mb_x - self.mb_border_w, 
				self.mb_y - self.mb_border_w, 
				self.mb_w + 2 *self.mb_border_w, 
				self.mb_h + 2 *self.mb_border_w
			])

			pygame.draw.rect(Globals.window, self.box_color, [
				self.mb_x,
				self.mb_y,
				self.mb_w,
				self.mb_h
			])

			#Prints Title

			x = (w[0] - self.mb_title_font.size(self.mb_title)[0])/2
			y = self.mb_y + 20

			while self.mb_title_font.size(self.mb_title)[0] > self.mb_w:
				h = self.mb_title.font.get_height()

				if self.mb_title.get_height() > 20:
					self.mb_title_font = pygame.font.Font(pygame.font.Font("assets/fonts/Minecraftia-Regular.ttf", h - 1))
				else:
					raise Exception("Title text '%s' is too long." % self.mb_title)

			ren = self.mb_title_font.render(self.mb_title, False, self.border_color)
			Globals.window.blit(ren, (x, y))


			#Prints MEssage

			line_indent = 0

			x = self.mb_x + 5
			y = self.mb_y + self.mb_title_font.size(self.mb_title)[1] + 5

			for line in self.text_lines:

				ren = self.mb_message_font.render(line, False, self.border_color)

				Globals.window.blit(ren, (x, y + self.mb_message_font.size(line)[1] * line_indent))

				line_indent += 1

		elif self.dl_is_showing:

			pygame.draw.rect(Globals.window, self.border_color, [
				self.dl_x, 
				self.dl_y - self.dl_border_w,
				self.dl_w,
				self.dl_border_w
			])

			pygame.draw.rect(Globals.window, self.box_color, [
				self.dl_x,
				self.dl_y, 
				self.dl_w,
				self.dl_h
			])

			img_y = int(self.dl_y + (self.dl_h - self.dl_image_s) / 2)

			Globals.window.blit(self.dl_images[self.dl_index], (self.dl_offset_left, img_y))

			for i in range(len(self.dl_dialogs[self.dl_index])):

				line = self.dl_dialogs[self.dl_index][i]

				r = self.dl_font.render(line)
				Globals.window.blit(r, (self.dl_offset_left + self.dl_image_s + 10))

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
				self.text_lines = [""]