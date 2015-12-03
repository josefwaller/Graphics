import pygame

from level_editor_assets.lvl_edtr_globals import LEGlobals

class BaseItem ():

	x = 0
	y = 0
	s = 0

	offset_x = 0

	image = 0

	attributes = None

	def __init__ (self, x, y, image, attributes, offset):

		self.x, self.y = x, y
		self.s = LEGlobals.block_size
		self.image = image

		self.attributes = attributes.copy()
		if not self.attributes['editable'] == None:
			self.attributes['editable'] = attributes['editable'].copy()

		#Accounts for the menu
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

		elif self.attributes['type'] == 'walker':

			dis = (self.attributes['editable']['rounds'] + self.attributes['editable']['offset'])

			to_save['turn1'] = (self.x / LEGlobals.block_size) + ((self.s / 2) / LEGlobals.block_size) - (dis / 2)
			to_save['turn2'] = (self.x / LEGlobals.block_size) + ((self.s / 2) / LEGlobals.block_size) + (dis / 2)

		elif self.attributes['type'] == 'checkpoint':
			to_save['y'] += 1
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
		elif self.attributes['type'] == 'trigger':

			x = self.x + LEGlobals.x_offset * LEGlobals.block_size + self.offset_x
			y = self.y + LEGlobals.y_offset * LEGlobals.block_size
			w = self.attributes['editable']['w'] * LEGlobals.block_size
			h = self.attributes['editable']['h'] * LEGlobals.block_size

			pink = (255, 0, 255)

			pygame.draw.rect(LEGlobals.window, pink, [x, y, w, h], 10)

		else:

			if self.attributes['type'] == 'walker':

				black = (0, 0, 0)

				rounds = self.attributes['editable']['rounds'] * LEGlobals.block_size
				offset = self.attributes['editable']['offset'] * LEGlobals.block_size

				x = self.x - int((rounds - offset - self.s) / 2) + LEGlobals.x_offset * LEGlobals.block_size + self.offset_x
				y = self.y + int(self.s / 2) + LEGlobals.y_offset * LEGlobals.block_size
				w = rounds
				h = 0

				print("X:%s, player's x: %s" % (x, self.x))

				length = 4

				pygame.draw.rect(LEGlobals.window, black, [x, y, w, h], length)

			LEGlobals.window.blit(self.image, (
				self.x + LEGlobals.x_offset * LEGlobals.block_size + self.offset_x, 
				self.y + LEGlobals.y_offset * LEGlobals.block_size
			))