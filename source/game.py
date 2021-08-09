import pickle
import tcod
import tcod.event
from typing import Dict

from source.area.area import Area
from source.entity.newtonian_entity import NewtonianEntity
from source.galaxy.galaxy import Galaxy
from source.handlers.input_handler import InputHandler
from source.menu.menu import Menu
from source.menu.menu_item import MenuItem
from source.planet.planet import Planet
from source.player.player import Player
from source.engine.renderengine import RenderEngine
from source.engine.eventengine import EventEngine
from source.helper_functions.circle_conversions import *
from source.system.system import System
from source.ui.ui_panel import UIPanel
from source.ship.ship import Ship

class Game:
    def __init__(self, config:Dict={}):
        self.config = config
        #set up font
        self.render_engine = RenderEngine(
            tcod.tileset.load_tilesheet("terminal12x12_gs_ro.png", 16, 16, tcod.tileset.CHARMAP_CP437),
            50,
            50,
            self)
        self.event_engine = EventEngine(self)
        self.InputHandler:InputHandler = InputHandler()
        self.game_state = 'menu_main'

        #generate main menu
        self.main_menu = Menu()
        new_game = MenuItem('New Game', select=lambda: {'type': 'game', 'value': 'new'})
        load_game = MenuItem('Load Game', select=lambda: {'type': 'game', 'value': 'load'})
        exit_game = MenuItem('Exit', select=lambda: {'type': 'exit'})
        self.main_menu.menu_items.extend([new_game, load_game, exit_game])
        self.current_menu = self.main_menu

        #generate game menu
        self.game_menu = Menu()
        save_game = MenuItem('Save Game', select=lambda: {'type': 'save'})
        close_menu = MenuItem('Close Menu', select=lambda: {'type': 'close'})
        self.game_menu.menu_items.extend([close_menu, save_game, load_game, exit_game])

    def start_new_game(self):
        #Code to generate player
        # None,{'x': 1, 'y': 1}
        self.player = Player()
        player_ship = Ship('@', (255,255,255), is_player=True, priority_draw=True)
        self.player.assign_ship(player_ship)
        self.player.current_entity.vector.x = 1
        self.player.current_entity.vector.y = 1
        self.player.current_entity.x = 7
        self.player.current_entity.y = 7
        
        #Code to generate initial system
        self.galaxy = Galaxy()
        self.current_location = self.galaxy.galaxy_generator.generate_solar_system(50, 50)
        self.galaxy.galaxy_generator.generate_planets(self.current_location)
        self.current_location.explored = True
        self.galaxy.system_dict[(self.current_location.x, self.current_location.y)] = self.current_location
        self.current_area:Area = None
        self.generate_current_area()
        self.current_area.add_entity(self.player.current_entity)
        self.player.current_entity.generate_vector_path()
        self.game_state = 'game_system'

    def save_game(self):
        save_dict = {
            'galaxy': self.galaxy,
            'global_time': self.global_time,
            'global_queue': self.global_queue,
            'player': self.player,
            'current_location': self.current_location,
            'current_area': self.current_area,
            'game_state': self.game_state
        }
        try:
            with open('saves/save.p', 'wb+') as save_file:
                pickle.dump(save_dict, save_file, pickle.HIGHEST_PROTOCOL)
        except FileNotFoundError:
            with open('saves/save.p', 'ab+') as save_file:
                pickle.dump(save_dict, save_file, pickle.HIGHEST_PROTOCOL)

    def load_game(self):
        try:
            with open('saves/save.p', 'rb') as save_file:
                data = pickle.load(save_file)
                self.galaxy = data['galaxy']
                self.global_time = data['global_time']
                self.global_queue = data['global_queue']
                self.player = data['player']
                self.current_location = data['current_location']
                self.current_area = data['current_area']
                self.game_state = data['game_state']
        except FileNotFoundError:
            pass

    def generate_current_area(self):
        self.current_area = self.current_location.generate_area()

