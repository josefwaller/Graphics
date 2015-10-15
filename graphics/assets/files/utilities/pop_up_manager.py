from assets.files.utilities.globals import Globals

import pygame

class PopUpManager ():

	letters = {}

	end_statement = "Press Enter to continue"

	def __init__(self):
		
		letters = [
			"a",
			"b",
			"c",
			"d",
			"e",
			"f",
			"g",
			"h",
			"i",
			"j",
			"k",
			"l",
			"m",
			"n",
			"o",
			"p",
			"q",
			"r",
			"s",
			"t",
			"u",
			"v",
			"w",
			"x",
			"y",
			"z"
		]

		for l in letters:

			letter = pygame.image.load("assets/images/alphabet/%s.png" % l).convert_alpha()

			self.l_w = int(Globals.block_size / 16 * letter.get_size()[0])

			self.l_h = self.l_w

			self.letters[l] = pygame.transform.scale(letter, (self.l_w, self.l_h))

		self.message_box = {

			"x": Globals.window.get_size()[0] * (1 / 5),
			"y": Globals.window.get_size()[1] * (1 / 5),
			"w": Globals.window.get_size()[0] - (200),
			"h": Globals.window.get_size()[1] - (200),
			"message": "Hello",
			"should_show": False

		}



	def show_message (self, mess):

		self.message_box['message'] = mess
		self.message_box['should_show'] = True

	def render (self):

		white = (255, 255, 255)

		if self.message_box['should_show']:

				x = self.message_box['x']
				y = self.message_box['y']
				w = self.message_box['w']
				h = self.message_box['h']

				pygame.draw.rect(Globals.window, white, (x, y, w, h))

				words = (self.message_box['message']).split()

				for i in range(2 * len(words)):
					if not i % 2 == 0:

						x = len(words) - 1

						words.append("")

						while x >= i:

							words[x + 1] = words[x]

							x -= 1

						words[i] = " "

				l_x = self.message_box['x'] + (self.message_box['w'] / 20)
				l_y = self.message_box['y'] + (self.message_box['h'] / 20)

				for word in words:

					if l_x + self.l_w * len(word) >= self.message_box['x'] + self.message_box['w'] - 20:

						l_y += self.l_h
						l_x = self.message_box['x'] + (self.message_box['w'] / 20)

					for l in word:

						l = l.lower()

						try:

								Globals.window.blit(self.letters[l], (l_x, l_y))

						except:
							pass

						l_x += self.l_w

						if l_x + self.l_w >= self.message_box['x'] + self.message_box['w'] - 20:

							l_y += self.l_h

							l_x = self.message_box['x'] + self.message_box['w'] / 20

				l_x = int(self.message_box['x'] + self.message_box['w'] - ((len(self.end_statement)) * self.l_w) - 20)

				print(l_x)

				l_y = self.message_box['y'] + self.message_box['h'] - 20 - self.l_h

				print(l_y)

				for letter in self.end_statement:

					letter = letter.lower()

					if not letter == " ":

						Globals.window.blit(self.letters[letter], (l_x, l_y))

					l_x += self.l_w


	def on_input (self, keys):

		if Globals.is_paused:

			if pygame.K_RETURN in keys:

				Globals.is_paused = False

				self.message_box['should_show'] = False