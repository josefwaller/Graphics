import pygame

from level_editor_assets.lvl_edtr_globals import LEGlobals


class BaseItem:

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
		if self.attributes['editable'] is not None:
			self.attributes['editable'] = attributes['editable'].copy()

		# Accounts for the menu
		self.offset_x = offset

	def load_image(self, img):

		image = pygame.image.load(img).convert_alpha()

		self.image = pygame.transform.scale(image, (self.s, self.s))

	def get_save(self):

		to_save = self.attributes.copy()

		to_save['x'] = int(self.x / LEGlobals.block_size)
		to_save['y'] = int(self.y / LEGlobals.block_size)

		if self.attributes['type'] == "platform" or self.attributes['type'] == 'trigger':
			to_save['w'] = self.attributes['editable']['w']
			to_save['h'] = self.attributes['editable']['h']

			if self.attributes['type'] == 'trigger':
				n = self.attributes['editable']['type']
				trigger_type = None
				file = None

				if n == 0:
					trigger_type = 'player_die'
				elif n == 1:
					trigger_type = 'dialog_box'
					file = "dialog_%s.json" % self.attributes['editable']['file_num']
				elif n == 2:
					trigger_type = "message_box"
					file = "mb_%s.json" % self.attributes['editable']['file_num']

				to_save['on_enter'] = {
					"type": trigger_type,
					"file": file
				}

		elif self.attributes['type'] == 'walker':
			dis = (self.attributes['editable']['rounds'] + self.attributes['editable']['offset'])

			to_save['turn1'] = (self.x / LEGlobals.block_size) + ((self.s / 2) / LEGlobals.block_size) - (dis / 2)
			to_save['turn2'] = (self.x / LEGlobals.block_size) + ((self.s / 2) / LEGlobals.block_size) + (dis / 2)

		elif self.attributes['type'] == 'checkpoint':
			to_save['y'] += 1
		to_save.pop('image')

		return to_save

	def render(self):

		if self.attributes['type'] == 'platform':

			x = self.x + LEGlobals.x_offset * LEGlobals.block_size + self.offset_x
			y = self.y + LEGlobals.y_offset * LEGlobals.block_size

			for i in range(self.attributes['editable']['w']):

				for z in range(self.attributes['editable']['h']):

					LEGlobals.window.blit(self.image, (
						x + i * self.s,
						y + z * self.s
					))

			color = (0, 255, 0)
			w = self.attributes['editable']['w']
			h = self.attributes['editable']['h']
			pygame.draw.rect(LEGlobals.window, color, [x, y, self.s * w, self.s * h], 1)

		elif self.attributes['type'] == 'trigger':

			x = self.x + LEGlobals.x_offset * LEGlobals.block_size + self.offset_x
			y = self.y + LEGlobals.y_offset * LEGlobals.block_size
			w = self.attributes['editable']['w'] * LEGlobals.block_size
			h = self.attributes['editable']['h'] * LEGlobals.block_size

			pink = (255, 0, 255)
			black = (0, 0, 0)
			orange = (255, 165, 0)
			green = (0, 255, 0)

			if self.attributes['editable']['type'] == 0:
				color = black

			elif self.attributes['editable']['type'] == 1:
				color = orange

			elif self.attributes['editable']['type'] == 2:
				color = pink

			else:
				color = green

			pygame.draw.rect(LEGlobals.window, color, [x, y, w, h], 10)
			font = pygame.font.Font("assets/fonts/Minecraftia-Regular.ttf", 16)
			text = str(self.attributes['editable']['file_num'])
			font_x = x + (w - font.size(text)[0]) / 2
			font_y = y + (h - font.get_height()) / 2
			r = font.render(text, False, (255, 255, 255))
			LEGlobals.window.blit(r, (font_x, font_y))

		else:

			if self.attributes['type'] == 'walker':

				black = (0, 0, 0)

				rounds = self.attributes['editable']['rounds'] * LEGlobals.block_size
				offset = self.attributes['editable']['offset'] * LEGlobals.block_size

				x = self.x - int((rounds - offset - self.s) / 2) + LEGlobals.x_offset * LEGlobals.block_size + self.offset_x
				y = self.y + int(self.s / 2) + LEGlobals.y_offset * LEGlobals.block_size
				w = rounds
				h = 0

				length = 4

				pygame.draw.rect(LEGlobals.window, black, [x, y, w, h], length)

			LEGlobals.window.blit(self.image, (
				self.x + LEGlobals.x_offset * LEGlobals.block_size + self.offset_x, 
				self.y + LEGlobals.y_offset * LEGlobals.block_size
			))

	def check_selection(self, m):

		x = self.x + LEGlobals.x_offset * LEGlobals.block_size + self.offset_x
		y = self.y + LEGlobals.y_offset * LEGlobals.block_size
		w = 0
		h = 0

		if self.attributes['type'] == 'platform' or self.attributes['type'] == 'trigger':
			w = self.attributes['editable']['w'] * LEGlobals.block_size
			h = self.attributes['editable']['h'] * LEGlobals.block_size

		else:
			w = LEGlobals.block_size
			h = LEGlobals.block_size

		if m[0] < x + w:
			if m[0] > x:
				if m[1] < y + h:
					if m[1] > y:
						return True

		return False
