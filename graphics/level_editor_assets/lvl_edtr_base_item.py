import pygame

from level_editor_assets.lvl_edtr_globals import LEGlobals

class BaseItem ():

	x = 0
	y = 0
	w = 0
	h = 0

	oiffset_x = 0

	image = 0

	attributes = None

	def __init__ (self, x, y, image, attributes, offset):

		self.x, self.y = x, y
		self.s = LEGlobals.block_size
		self.image = image

		self.attributes = attributes.copy()
		if not self.attributes['editable'] == None:
			self.attributes['editable'] = attributes['editable'].copy()
		self.offset_x = offset

		print(self.x / LEGlobals.block_size)

	def load_image(self, img):

		image = pygame.image.load(img).convert_alpha()

		self.image = pygame.transform.scale(image, (self.s, self.s))

	def get_save (self):

		to_save = {}

		to_save = self.attributes.copy()

		to_save['x'] = int(self.x / LEGlobals.block_size)
		to_save['y'] = int(self.y / LEGlobals.block_size)
		if self.attributes['type'] == "platform":
			to_save['w'] = self.attributes['editable']['w']
			to_save['h'] = self.attributes['editable']['h']

		to_save.pop('image')

		return to_save


	def render (self):

		if self.attributes['type'] == 'platform':

			x = self.x + LEGlobals.x_offset * LEGlobals.block_size + self.offset_x
			y = self.y + LEGlobals.y_offset * LEGlobals.block_size

			for i in range(self.attributes['editable']['w']):

				for z in range(self.attributes['editable']['h']):

					LEGlobals.window.blit(self.image, (
						x + i * self.s,
						y + z * self.s
					))
		else:
			LEGlobals.window.blit(self.image, (
				self.x + LEGlobals.x_offset * LEGlobals.block_size + self.offset_x, 
				self.y + LEGlobals.y_offset * LEGlobals.block_size
			))