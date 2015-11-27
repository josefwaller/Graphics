import pygame
import json

from level_editor_assets.lvl_edtr_base_item import BaseItem
from level_editor_assets.lvl_edtr_globals import LEGlobals

class LevelEditor ():

	menu_width = 150
	attr_menu_width = 150

	window = None

	items = None
	item_selected = None

	entities = None
	entity_selected = None
	block_size = None

	buttons = []

	mouse = None

	offset_x = 0
	offset_y = 0

	compass_buttons = []

	def __init__ (self):

		windowSize = width, height = 800, 600
		LEGlobals.window = pygame.display.set_mode(windowSize)

		self.mouse = [[0,0], 0]

		self.items = [
			{
				"image": self.load_img("assets/images/blocks/temp_block.png"),
				"type": "delete",
				"selected": False,
				"editable" : None

			},
			{
				"image": self.load_img("assets/images/player/run_2.png"),
				"type": "player",
				"selected": False,
				"editable" : None
			},
			{
				"image": self.load_img("assets/images/blocks/snow.png"),
				"type": "platform",
				"selected": False,
				"editable": 
					{
						"w" : 1,
						"h" : 1
					}
			},
			{
				"image" : self.load_img("assets/images/enemies/wizard/front_1.png"),
				"type": "wizard",
				"selected": False,
				"editable" : None
			},
			{
				"image": self.load_img("assets/images/enemies/walker/run_2.png"),
				"type": "walker",
				"selected": False,
				"editable": {
					"rounds": 5,
					"offset": 0
				}
			},
			{
				"image": self.load_img("assets/images/enemies/archer/archer_1.png"),
				"type": "archer",
				"selected": False,
				"editable": None
			},
			{
				"image": self.load_img("assets/images/enemies/jumper/jumper_land.png"),
				"type": "jumper",
				"selected": False,
				"editable": None
			},
			{
				"image": self.load_img("assets/images/tools/bar.png"),
				"type": "bar",
				"selected": False,
				"editable": None
			},
			{
				"image": self.load_img("assets/images/tools/staff.png"),
				"type": "staff",
				"selected": False,
				"editable": None
			},
			{
				"image": self.load_img("assets/images/tools/sword.png"),
				"type": "sword",
				"selected": False,
				"editable": None
			},
			{
				"image": self.load_img("assets/images/blocks/up_graphics_16.png"),
				"type": "endblock",
				"selected": False,
				"editable": None
			}

		]

		c = []

		for i in range(int(len(self.items) / 4) + 1):

			c.append([])


		for i in range(len(self.items)):

			i_rounded = int(i/4)

			c[i_rounded].append(self.items[i])

		self.items = c.copy()



		compass_size = 90
		#   _ _ _
		#  |_|_|_|
		#  |_|_|_|
		#  |_|_|_|

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
				1
			],
			[
				0,
				int(LEGlobals.window.get_size()[1] - compass_size * (2/3)),
				int(compass_size * (1/3)),
				int(compass_size * (1/3)),
				-1,
				0
			]
		]

		self.save_button = [

			LEGlobals.window.get_size()[0] - 100,
			LEGlobals.window.get_size()[1] - 100,
			100
		]

		LEGlobals.block_size = int(LEGlobals.window.get_size()[1] / 15)
		self.item_selected = {
			"type": None
		}
		self.entities = []

		while len(self.entities) < 20:
			self.entities.append([])

		for i in range(len(self.entities)):
			while len(self.entities[i]) < int(LEGlobals.window.get_size()[1] / LEGlobals.block_size):
				self.entities[i].append(None)


		self.run_editor()

	def run_editor (self):
		
		while True:

			self.mouse[1] = False

			for event in pygame.event.get():

				if event.type == pygame.MOUSEBUTTONDOWN:

					self.mouse[1] = True

			self.mouse[0] = pygame.mouse.get_pos()

			if not self.check_for_compass_movement():


				if self.mouse[0][0] < self.menu_width:
					self.check_for_menu_selection()

				elif self.mouse[0][0] > self.menu_width and self.mouse[0][0] < LEGlobals.window.get_size()[0] - self.attr_menu_width:
					
					if not self.check_for_entity_selection():

						self.check_for_item_placement()

				elif self.mouse[0][0] > LEGlobals.window.get_size()[0] - self.attr_menu_width:
					self.check_for_attribute_changes()

			self.check_for_save()

			self.render()

	def check_for_save (self):

		p = self.save_button

		if self.mouse[1]:
			if self.mouse[0][0] > p[0]:
				if self.mouse[0][0] < p[0] + p[2]:
					if self.mouse[0][1] > p[1]:
						if self.mouse[0][1] < p[1] + p[2]:
							self.save_to_file("current_level.json")

	def check_for_compass_movement (self):

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

	def check_for_menu_selection (self):

		item_row = int(self.mouse[0][1] / (self.menu_width / 4))

		item_index = int(self.mouse[0][0] / (self.menu_width / 4))

		try:

			if self.mouse[1] == True:

				self.item_selected = self.items[item_row][item_index]

		except IndexError:

			#No button was there
			self.item_selected = None

	def  check_for_item_placement (self):

		if not self.item_selected == None and self.mouse[1] == True:

			x = int(self.mouse[0][0] / LEGlobals.block_size) - LEGlobals.x_offset
			y = int(self.mouse[0][1] / LEGlobals.block_size) - LEGlobals.y_offset

			if self.item_selected['type'] == 'delete':
				self.entities[x][y] = None

			else:

				self.entities[x][y] = BaseItem(
					x= int((self.mouse[0][0] - self.menu_width) / LEGlobals.block_size) * LEGlobals.block_size - LEGlobals.x_offset, 
					y= y * LEGlobals.block_size,
					image=pygame.transform.scale(self.item_selected['image'], (LEGlobals.block_size, LEGlobals.block_size)), 
					attributes=self.item_selected.copy(),
					offset=self.menu_width
				)



	def check_for_attribute_changes (self):
		
		for b in self.buttons:

			if self.mouse[1]:

				if self.mouse[0][0] < b['x'] + b['s']:
					if self.mouse[0][0] > b['x']:
						if self.mouse[0][1] < b['y'] + b['s']:
							if self.mouse[0][1] > b['y']:

								b['ent'][b['attr']] += b['inc']

								print(b['ent'])

	def save_to_file(self, file_name):

		to_save = []

		most_x = 0
		most_y = 0

		for x in range(len(self.entities)):

			for y in range(len(self.entities[x])):

				if not self.entities[x][y] == None:

					e = self.entities[x][y]

					to_save.append(e.get_save())

					if e.x + e.w > most_x:
						most_x = e.x + e.w
					if e.y + e.h > most_y:
						most_y = e.y + e.h

		to_save.append({
			"type": "level_settings",
			"width": int(most_x / LEGlobals.block_size),
			"height": int(most_y / LEGlobals.block_size)
		})

		f = open("assets/levels/%s" % file_name, "w")
		f.write(json.dumps(to_save))

	def render (self):

		#Draws sky

		sky = pygame.image.load("assets/images/props/sky.png").convert_alpha()

		sky = pygame.transform.scale(sky, (LEGlobals.window.get_size()[0] - self.menu_width - self.attr_menu_width, LEGlobals.window.get_size()[1]))

		LEGlobals.window.blit(sky, (self.menu_width, 0))

		grey = (128, 128, 128)

		#Draws Grid

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

		#Draws things

		for e_x in range(len(self.entities)):
			for e_y in range(len(self.entities[e_x])):

				if not self.entity_selected == None:
					if e_x == self.entity_selected[0]:
						if e_y == self.entity_selected[1]:
							red = (255, 0, 0)

							s = LEGlobals.block_size
							pygame.draw.rect(LEGlobals.window, red, [e_x * s, e_y * s, s, s])

				e = self.entities[e_x][e_y]
				if not e == None:
					e.render()

		#Draws compass

		for b in self.compass_buttons:

			new_grey = (80, 80, 80)

			pygame.draw.rect(LEGlobals.window, new_grey, (self.menu_width + b[0], b[1], b[2], b[3]))


		#Draws item menu

		pygame.draw.rect(LEGlobals.window,grey, [0, 0, self.menu_width, LEGlobals.window.get_size()[1]])

		x = 0
		y = 0
		s = int(self.menu_width / 4)

		for item_row in self.items:

			for item in item_row:

				if not self.item_selected == None and self.item_selected['type'] == item['type']:
					red = (255, 0, 0)
					pygame.draw.rect(LEGlobals.window, red, [x, y, s, s])

				image = pygame.transform.scale(item['image'], (s, s))

				LEGlobals.window.blit(image, (x, y))

				x += s

			y += s
			x = 0

		#Draws Attribute Menu
		pygame.draw.rect(LEGlobals.window, grey, [
			LEGlobals.window.get_size()[0] - self.attr_menu_width,
			0,
			self.attr_menu_width,
			LEGlobals.window.get_size()[1]
		])
		if not self.entity_selected == None:

				grey = (200, 200, 200)

				text_grey = (80, 80, 80)

				pygame.font.init()

				f = pygame.font.Font("assets/fonts/Minecraftia-Regular.ttf", s)

				for b in self.buttons:

					pygame.draw.rect(LEGlobals.window, grey, [b['x'], b['y'], b['s'], b['s']])

					if not b['text'] == None:

						r = f.render(b['text'], False, text_grey)

						LEGlobals.window.blit(r, (b['x'] + b['s'] + 10, b['y'] + int(b['s'] / 2)))

		#Draws exit button

		purple = (180, 000, 255)

		p = self.save_button

		pygame.draw.rect(LEGlobals.window, purple, [p[0], p[1], p[2], p[2]])

		pygame.display.flip()

	def check_for_entity_selection (self):

		if not self.item_selected['type'] == 'delete':

			if self.mouse[1] == True:

				x = int(self.mouse[0][0] / LEGlobals.block_size) - LEGlobals.x_offset
				y = int(self.mouse[0][1] / LEGlobals.block_size) - LEGlobals.y_offset

				if not self.entities[x][y] == None:

					self.entity_selected = [x, y]

					#Creates buttons

					e = self.entities[x][y]

					if not e.attributes['editable'] == None:

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

	def load_img (self, img):

		img = pygame.image.load(img).convert_alpha()

		return img