from assets.files.utilities.globals import Globals

import pygame

class HeadsUpDisplay ():

	def __init__(self):
		pass


	def show_message (self, mess):
		pass

	def render (self):
		yellow = (255, 234, 000)
		x, y = Globals.window.get_size()[0], Globals.window.get_size()[1]

		# s = pygame.Surface((x, y))
		# s.set_alpha(12 * (255/100))
		# s.fill(yellow)
		# Globals.window.blit(s, [0, 0])

	def on_input (self, keys):
		pass