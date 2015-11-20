from assets.files.utilities.globals import Globals

import pygame
import math

class HeadsUpDisplay ():

	is_showing = False

	mb_x = 0
	mb_y = 0
	mb_w = 0
	mb_h = 0

	mb_border_color = (65, 65, 65)
	mb_border_w = 0
	mb_box_color = (128, 128, 128)

	text_lines = [""]

	mb_title_font = None
	mb_message_font = None

	mb_title = "Testing line_inthat :"
	def __init__(self):

		self.mb_w = math.floor((Globals.window.get_size()[0] * (2/3)) / Globals.block_size) * Globals.block_size
		self.mb_h = math.floor((self.mb_w / Globals.block_size) * (3/4)) * Globals.block_size

		self.mb_border_w = (Globals.block_size / Globals.pixels_per_block) * 2

		self.mb_x = (Globals.window.get_size()[0] - self.mb_w) / 2
		self.mb_y = (Globals.window.get_size()[1] - self.mb_h) / 2

		pygame.font.init()

		self.mb_title_font = pygame.font.Font("assets/fonts/Minecraftia-Regular.ttf", 30)
		self.mb_message_font = pygame.font.Font("assets/fonts/Minecraftia-Regular.ttf", 16)

		
	def render (self):

		if self.is_showing:

			pygame.draw.rect(Globals.window, self.mb_border_color, [
				self.mb_x - self.mb_border_w, 
				self.mb_y - self.mb_border_w, 
				self.mb_w + 2 *self.mb_border_w, 
				self.mb_h + 2 *self.mb_border_w
			])

			pygame.draw.rect(Globals.window, self.mb_box_color, [
				self.mb_x,
				self.mb_y,
				self.mb_w,
				self.mb_h
			])

			#Prints Title

			x = (Globals.window.get_size()[0] - self.mb_title_font.size(self.mb_title)[0])/2
			y = self.mb_y + 20

			while self.mb_title_font.size(self.mb_title)[0] > self.mb_w:
				h = self.mb_title.font.get_height()

				if self.mb_title.get_height() > 20:
					self.mb_title_font = pygame.font.Font(pygame.font.Font("assets/fonts/Minecraftia-Regular.ttf", h - 1))
				else:
					raise Exception("Title text '%s' is too long." % self.mb_title)

			ren = self.mb_title_font.render(self.mb_title, False, self.mb_border_color)
			Globals.window.blit(ren, (x, y))


			#Prints MEssage

			line_indent = 0

			x = self.mb_x + 5
			y = self.mb_y + self.mb_title_font.size(self.mb_title)[1] + 5

			for line in self.text_lines:

				ren = self.mb_message_font.render(line, False, self.mb_border_color)

				Globals.window.blit(ren, (x, y + 16*line_indent))

				line_indent += 1

	def message_box(self, title, message):

			self.is_showing = True

			line_index = 0

			self.mb_title = title

			word_index = 1

			words = message.split(" ")

			self.text_lines[0] = words[0]

			needs_to_loop = True

			while needs_to_loop:

				needs_to_loop = False

				while  len(words) - 1 >= word_index and self.mb_message_font.size(self.text_lines[line_index] + words[word_index])[0] < (self.mb_w - 10):

					needs_to_loop = True

					self.text_lines[line_index] += "  %s" % words[word_index]

					word_index += 1

			#Adds a new line

				try:
					self.text_lines[line_index + 1]
				except IndexError:
					self.text_lines.append("")

				line_index += 1

	def on_input (self, keys):
		pass