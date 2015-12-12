import pygame
import json

from level_editor_assets.lvl_edtr_base_item import BaseItem
from level_editor_assets.lvl_edtr_globals import LEGlobals


class LevelEditor:

	menu_width = 150
	attr_menu_width = 150

	window = None

	items = None
	item_selected = {
		"type": None
	}

	entities = None
	entity_selected = None
	block_size = None

	level_file = None
	to_save_to = "test.json"

	level_dimensions = None

	buttons = []

	mouse = None

	offset_x = 0
	offset_y = 0

	compass_buttons = []

	def __init__(self, level_to_load=None, level_to_save=None, dimension_x=40, dimension_y=40):

		pygame.init()

		window_size = 800, 600
		LEGlobals.window = pygame.display.set_mode(window_size)

		self.to_save_to = level_to_save

		self.level_dimensions = [int(dimension_x), int(dimension_y)]

		self.mouse = [[0, 0], 0]

		# Reads items
		item_file = open("level_editor_assets/lvl_edtr_items.json", "r")
		self.base_items = json.loads(item_file.read())
		item_file.close()
		for item in self.base_items:
			item['image'] = self.load_img(item['image'])

		# Stuff in the menu
		c = []

		for i in range(int(len(self.base_items) / 4) + 1):

			c.append([])

		for i in range(len(self.base_items)):

			# Rounds to 4 a row
			i_rounded = int(i/4)

			c[i_rounded].append(self.base_items[i])

		self.items = c.copy()

		self.set_compass_proportions(90)

		self.save_button = [

			LEGlobals.window.get_size()[0] - 100,
			LEGlobals.window.get_size()[1] - 100,
			100
		]

		LEGlobals.block_size = int(LEGlobals.window.get_size()[1] / 30)

		self.item_selected = {
			"type": None
		}
		self.entities = []

		self.scale_to_dimension()

		if level_to_load is not None:

			file = open("assets/levels/%s" % level_to_load, "r")
			level = json.loads(file.read())

			self.level_dimensions = [
				level['level_settings']['width'],
				level['level_settings']['height']
			]
			self.scale_to_dimension()

			for thing in level['entities']:

				for item in self.base_items:

					attributes = item.copy()
					if item['editable'] is not None:
						attributes['editable'] = item['editable'].copy()

					if item['type'] == thing['type']:

						if item['editable'] is not None:

							for i in item['editable']:
								try:
									attributes['editable'][i] = thing['editable'][i]
								except:
									print("Type %s has no %s" % (thing['type'], i))

						y = thing['y']

						if thing['type'] == 'checkpoint':
							y -= 1

						self.entities[thing['x']][thing['y']] = BaseItem(
							x=thing['x'] * LEGlobals.block_size,
							y=y * LEGlobals.block_size,
							image=pygame.transform.scale(item['image'], (LEGlobals.block_size, LEGlobals.block_size)),
							attributes=attributes,
							offset=self.menu_width
						)
						break

		# Runs editor loop
		self.run_editor()

	def scale_to_dimension(self):

		while len(self.entities) < self.level_dimensions[0]:
			self.entities.append([])

		for i in range(len(self.entities)):
			while len(self.entities[i]) < self.level_dimensions[1]:
				self.entities[i].append(None)

	def run_editor(self):
		
		while True:

			self.mouse[1] = False

			for event in pygame.event.get():

				if event.type == pygame.MOUSEBUTTONDOWN:

					self.mouse[1] = True

			self.mouse[0] = pygame.mouse.get_pos()

			if self.item_selected is None:
				self.item_selected = {
					"type": None
				}

			if not self.check_for_compass_movement():

				if self.mouse[0][0] < self.menu_width:
					self.check_for_menu_selection()

				elif self.mouse[0][0] > self.menu_width and self.mouse[0][0] < LEGlobals.window.get_size()[0] - self.attr_menu_width:

					if not self.check_for_entity_selection() and self.item_selected['type'] is not None:

						self.check_for_item_placement()

				elif self.mouse[0][0] > LEGlobals.window.get_size()[0] - self.attr_menu_width:
					self.check_for_attribute_changes()

			self.check_for_save()

			self.render()

	def check_for_save(self):

		p = self.save_button

		if self.mouse[1]:
			if self.mouse[0][0] > p[0]:
				if self.mouse[0][0] < p[0] + p[2]:
					if self.mouse[0][1] > p[1]:
						if self.mouse[0][1] < p[1] + p[2]:
							self.save_to_file(self.to_save_to)

	def check_for_compass_movement(self):

		for b in self.compass_buttons:

			if self.mouse[1] == True:

				if self.mouse[0][0] > b[0] + self.menu_width:
					if self.mouse[0][0] < b[0] + b[2] + self.menu_width:
						if self.mouse[0][1] > b[1]:
							if self.mouse[0][1] < b[1] + b[3]:

								LEGlobals.x_offset += b[4]
								LEGlobals.y_offset += b[5]

								return True
		return False

	def check_for_menu_selection(self):

		item_row = int(self.mouse[0][1] / (self.menu_width / 4))

		item_index = int(self.mouse[0][0] / (self.menu_width / 4))

		try:

			if self.mouse[1] is True:

				if self.items[item_row][item_index] is None:
					self.item_selected = {
						"type": None
					}
				else:
					self.item_selected = self.items[item_row][item_index]

		except IndexError:

			# No button was there
			self.item_selected = None

	def check_for_item_placement(self):

		if self.item_selected is not None and self.mouse[1] is True:

			# Gets the indexes
			x = int(self.mouse[0][0] / LEGlobals.block_size) - LEGlobals.x_offset
			y = int(self.mouse[0][1] / LEGlobals.block_size) - LEGlobals.y_offset

			if self.item_selected['type'] == 'delete':
				self.entities[x][y] = None

			else:

				self.entities[x][y] = BaseItem(
					x=int((self.mouse[0][0] - self.menu_width) / LEGlobals.block_size) * LEGlobals.block_size - (LEGlobals.x_offset * LEGlobals.block_size),
					y=y * LEGlobals.block_size,
					image=pygame.transform.scale(self.item_selected['image'], (LEGlobals.block_size, LEGlobals.block_size)), 
					attributes=self.item_selected.copy(),
					offset=self.menu_width
				)

	def check_for_attribute_changes(self):
		
		for b in self.buttons:

			if self.mouse[1]:

				if self.mouse[0][0] < b['x'] + b['s']:
					if self.mouse[0][0] > b['x']:
						if self.mouse[0][1] < b['y'] + b['s']:
							if self.mouse[0][1] > b['y']:

								b['ent'][b['attr']] += b['inc']

	def save_to_file(self, file_name):

		to_save = []

		most_x = 0
		most_y = 0

		for x in range(len(self.entities)):

			for y in range(len(self.entities[x])):

				if not self.entities[x][y] == None:

					e = self.entities[x][y]

					to_save.append(e.get_save())

					if e.x + e.s > most_x:
						most_x = e.x + e.s
					if e.y + e.s > most_y:
						most_y = e.y + e.s

		level_settings = ({
			"type": "level_settings",
			"width": int(most_x / LEGlobals.block_size),
			"height": int(most_y / LEGlobals.block_size)
		})
		final_to_save = {
			"level_settings": level_settings,
			"entities": to_save
		}
		f = open("assets/levels/%s" % file_name, "w")
		f.write(json.dumps(final_to_save))

	def render(self):

		# Draws sky

		sky = pygame.image.load("assets/images/props/8_sky.png").convert_alpha()

		sky = pygame.transform.scale(sky, (LEGlobals.window.get_size()[0] - self.menu_width - self.attr_menu_width, LEGlobals.window.get_size()[1]))

		LEGlobals.window.blit(sky, (self.menu_width, 0))

		grey = (128, 128, 128)

		# Draws Grid

		x = 0
		y = 0

		add_x = self.menu_width + self.attr_menu_width  

		while x * LEGlobals.block_size + add_x < LEGlobals.window.get_size()[0]:
			while y * LEGlobals.block_size < LEGlobals.window.get_size()[1]:

				black = (0,0,0)

				pygame.draw.rect(LEGlobals.window, black, [x * LEGlobals.block_size + self.menu_width, y * LEGlobals.block_size, LEGlobals.block_size, LEGlobals.block_size], 2)

				y += 1
			x += 1
			y = 0

		# Draws things

		for e_x in range(len(self.entities)):
			for e_y in range(len(self.entities[e_x])):

				e = self.entities[e_x][e_y]

				if e is not None:
					e.render()

					if self.entity_selected is not None:
						if e_x == self.entity_selected[0]:
							if e_y == self.entity_selected[1]:
								red = (255, 0, 0)

								s = LEGlobals.block_size
								pygame.draw.rect(LEGlobals.window, red, [
									e.x + LEGlobals.x_offset * s + self.menu_width,
									e.y + LEGlobals.y_offset * s,
									s,
									s], 1)

		# Draws level boundaries

			pink = (255, 0, 255)
			pygame.draw.rect(LEGlobals.window, pink, [
				LEGlobals.x_offset * LEGlobals.block_size + self.menu_width,
				LEGlobals.y_offset * LEGlobals.block_size,
				LEGlobals.block_size * self.level_dimensions[0],
				LEGlobals.block_size * self.level_dimensions[1]
			], 4)

		# Draws compass

		for b in self.compass_buttons:

			new_grey = (80, 80, 80)

			pygame.draw.rect(LEGlobals.window, new_grey, (self.menu_width + b[0], b[1], b[2], b[3]))


		# Draws item menu

		pygame.draw.rect(LEGlobals.window,grey, [0, 0, self.menu_width, LEGlobals.window.get_size()[1]])

		x = 0
		y = 0
		s = int(self.menu_width / 4)

		for item_row in self.items:

			for item in item_row:

				image = pygame.transform.scale(item['image'], (s, s))

				LEGlobals.window.blit(image, (x, y))

				if self.item_selected is not None and self.item_selected['type'] == item['type']:
					red = (255, 0, 0)
					pygame.draw.rect(LEGlobals.window, red, [x, y, s, s], 4)

				x += s

			y += s
			x = 0

		# Draws Attribute Menu
		pygame.draw.rect(LEGlobals.window, grey, [
			LEGlobals.window.get_size()[0] - self.attr_menu_width,
			0,
			self.attr_menu_width,
			LEGlobals.window.get_size()[1]
		])
		if self.entity_selected is not None:

				# Draws attribute menu attributes

				grey = (200, 200, 200)

				text_grey = (80, 80, 80)

				pygame.font.init()

				f = pygame.font.Font("assets/fonts/Minecraftia-Regular.ttf", s)

				for b in self.buttons:

					pygame.draw.rect(LEGlobals.window, grey, [b['x'], b['y'], b['s'], b['s']])

					if b['text'] is not None:

						r = f.render(b['text'], False, text_grey)

						LEGlobals.window.blit(r, (b['x'] + b['s'] + 10, b['y'] + int(b['s'] / 2)))

		#Draws exit button

		purple = (180, 000, 255)

		p = self.save_button

		pygame.draw.rect(LEGlobals.window, purple, [p[0], p[1], p[2], p[2]])

		pygame.display.flip()

	def check_for_entity_selection(self):

		if self.item_selected is not None and not self.item_selected['type'] == 'delete':

			if self.mouse[1] is True:

				nothing_selected = True

				for e_x in range(len(self.entities)):
					for e_y in range(len(self.entities[e_x])):
						if self.entities[e_x][e_y] is not None:
							if self.entities[e_x][e_y].check_selection(self.mouse[0]):
								self.entity_selected = [e_x, e_y]
								nothing_selected = False
								break
				if nothing_selected:
					return False

				# Creates buttons

				if self.entity_selected is not None:
					x, y = self.entity_selected[0], self.entity_selected[1]

					e = self.entities[x][y]

					if e.attributes['editable'] is not None:

						self.buttons = []

						button_s = 30

						x = LEGlobals.window.get_size()[0] - self.attr_menu_width
						y = 5

						for attr in e.attributes['editable']:

							self.buttons.append({
								"x": x,
								"y": y,
								"s": button_s,
								"ent": e.attributes['editable'],
								"attr": attr,
								"inc": 1,
								"text": attr
							})

							self.buttons.append({
								"x": x,
								"y": y + button_s + 5,
								"s": button_s,
								"ent": e.attributes['editable'],
								"attr": attr,
								"inc": -1,
								"text": None
							})

							y += 2 * button_s + 20

					return True

		return False

	def load_img(self, img):

		img = pygame.image.load(img).convert_alpha()

		return img

	def set_compass_proportions(self, compass_size):

		self.compass_buttons = [

			[
				int(compass_size * (1/3)),
				int(LEGlobals.window.get_size()[1] - compass_size),
				int(compass_size * (1/3)),
				int(compass_size * (1/3)),
				0,
				1
			],
			[
				int(compass_size * (2/3)),
				int(LEGlobals.window.get_size()[1] - compass_size * (2/3)),
				int(compass_size * (1/3)),
				int(compass_size * (1/3)),
				-1,
				0
			],
			[
				int(compass_size * (1/3)),
				int(LEGlobals.window.get_size()[1] - compass_size * (1/3)),
				int(compass_size * (1/3)),
				int(compass_size * (1/3)),
				0,
				-1
			],
			[
				0,
				int(LEGlobals.window.get_size()[1] - compass_size * (2/3)),
				int(compass_size * (1/3)),
				int(compass_size * (1/3)),
				1,
				0
			]
		]
