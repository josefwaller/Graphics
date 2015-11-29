from assets.files.utilities.globals import Globals

import pygame

class MainMenu ():

	logo = None

	logo_x = 0
	logo_y = 0

	blue = (0, 0, 255)

	def __init__(self):
		
		self.logo = pygame.image.load("assets/images/menu/logo.png").convert_alpha()

		w = Globals.window.get_size()

		#Rounds logo width closest to one thirds as wide of the screen
		pixel_size = Globals.block_size / Globals.pixels_per_block
		approx_logo_w = w[0] / 3
		logo_w_in_pixels = self.logo.get_size()[0] * pixel_size
		logo_w = int(approx_logo_w / logo_w_in_pixels * logo_w_in_pixels)
		logo_h = int(self.logo.get_size()[1] * (self.logo.get_size()[0] / self.logo.get_size()[1]))

		self.logo = pygame.transform.scale(self.logo, (logo_w, logo_h))

		self.logo_x = (w[0] - logo_w) / 2
		self.logo_y = 200

	def update(self):

		self.render()

	def render (self):
		
		pygame.draw.rect(Globals.window, (255, 255, 255), [
			20,
			20,
			200,
			200
		])

		Globals.window.blit(self.logo, (self.logo_x, self.logo_y))


