import pygame

class KeyHandler ():

	keys_down = []

	def __init__(self):

		self.keys_down = []

	def new_event (self, event):

		if event.type == pygame.KEYDOWN:

			if event.key not in self.keys_down:

				self.keys_down.append(event.key)

		elif event.type == pygame.KEYUP:

			if event.key in self.keys_down:

				self.keys_down.remove(event.key)
		
		return self.keys_down