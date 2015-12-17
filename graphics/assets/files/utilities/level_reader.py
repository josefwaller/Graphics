from assets.files.entities.player import Player
from assets.files.entities.platform import Platform
from assets.files.entities.trigger import Trigger
from assets.files.entities.sky import Sky
from assets.files.entities.current_tool import CurrentTool
from assets.files.entities.prop import Prop

from assets.files.entities.tools.bow_and_arrow import BowAndArrow
from assets.files.entities.tools.sword import Sword
from assets.files.entities.tools.staff import Staff

from assets.files.entities.enemies.walker import Walker
from assets.files.entities.enemies.wizard import Wizard
from assets.files.entities.enemies.archer import Archer
from assets.files.entities.enemies.jumper import Jumper

from assets.files.entities.checkpoint import Checkpoint
from assets.files.entities.end_block import EndBlock

from assets.files.utilities.globals import Globals
from assets.files.utilities.heads_up_display import HeadsUpDisplay

import json


class LevelReader:

	def __init__(self):
		pass

	def read_level(self, level_str):

		if Globals.graphics_level == 0:
			Globals.pixels_per_block = 10
		elif Globals.graphics_level == 1:
			Globals.pixels_per_block = 16
		elif Globals.graphics_level == 2:
			Globals.pixels_per_block = 32
		else:
			raise Exception("Graphics level has improper value %s" % (Globals.graphics_level))

		level = json.loads(level_str)

		Globals.hud = HeadsUpDisplay()

		Globals.enemies = []
		Globals.platforms = []
		Globals.checkpoints = []
		Globals.tools = []
		Globals.props = []
		Globals.is_paused = False

		settings = level['level_settings']
		Globals.level_width = settings['width'] * Globals.block_size
		Globals.level_height = settings['height'] * Globals.block_size

		Globals.sky = Sky()

		for thing in level['entities']:
			if thing['type'] == 'platform':
				Globals.platforms.append(Platform(
					x=thing['x'], 
					y=thing['y'], 
					w=thing['w'],
					h=thing['h'],
				))

			elif thing['type'] == 'player':
				Globals.player = Player(x=thing['x'], y=thing['y'])
				Globals.player_tool_sprite = CurrentTool()

			elif thing['type'] == 'archer':
				Globals.enemies.append(Archer(x=thing['x'], y=thing['y'],))

			elif thing['type'] == 'walker':
				Globals.enemies.append(Walker(x=thing['x'], y=thing['y'], turn1=thing['turn1'], turn2=thing['turn2']))

			elif thing['type'] == 'wizard':
				Globals.enemies.append(Wizard(x=thing['x'], y=thing['y'] - 1))

			elif thing['type'] == 'jumper':
				Globals.enemies.append(Jumper(x=thing['x'], y=thing['y']))

			elif thing['type'] == 'bar':
				Globals.tools.append(BowAndArrow(x=thing['x'], y=thing['y']))

			elif thing['type'] == 'sword':
				Globals.tools.append(Sword(x=thing['x'], y=thing['y']))

			elif thing['type'] == "staff":
				Globals.tools.append(Staff(x=thing['x'], y=thing['y']))

			elif thing['type'] == 'checkpoint':
				c = Checkpoint(x=thing['x'], y=thing['y'])
				Globals.checkpoints.append(c)

				try:
					if thing['is_starter']:
						Globals.player.checkpoint = c
						c.flag_rising = True
				except KeyError:
					pass

			elif thing['type'] == 'endblock':
				Globals.endblock = EndBlock(x=thing['x'], y=thing['y'])

			elif thing['type'] == 'prop':
				Globals.props.append(Prop(x=thing['x'], y=thing['y'], images=thing['image']))

			elif thing['type'] == 'trigger':
				x = thing['x']
				y = thing['y']
				w = thing['w']
				h = thing['h']

				if thing['on_enter']['type'] == 'message_box':
					file_name = "assets/dialog/%s" % thing['on_enter']['file']
					file = open(file_name)
					file_content = json.loads(file.read())

					title = file_content['title']
					text = file_content['text']
					param = [title, text]
					func = Globals.hud.message_box

				elif thing['on_enter']['type'] == 'dialog_box':
					file = open("assets/dialog/%s" % thing['on_enter']['file'])
					dialog = json.loads(file.read())
					dialogs = dialog['dialogs']
					images = dialog['images']
					param = [dialogs, images]
					func = Globals.hud.dialog_box

				elif thing['on_enter']['type'] == 'player_die':
					func = "player_die"
					param = []
				else:
					print("Trigger Entity has improper on_enter attribute: %s" % thing['on_enter']['type'])
					return

				Globals.props.append(
					Trigger(x=x, y=y, w=w, h=h, on_enter=func, parameters=param)
				)
