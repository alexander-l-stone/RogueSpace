import pickle
import tcod
import tcod.event
from typing import Dict

from source.draw.area.area import Area
from source.ship.ship_components.newtonian_mover import NewtonianMover
from source.galaxy.galaxy import Galaxy
from source.handlers.input_handler import InputHandler
from source.ui.menu.generate_menu import generate_main_menu, generate_dev_menu, generate_game_menu, generate_dev_command_menu, generate_spawn_entity_menu
from source.stellar_objects.planet import Planet
from source.player.player import Player
from source.engine.renderengine import RenderEngine
from source.engine.eventengine import EventEngine
from source.helper_functions.circle_conversions import *
from source.system.system import System
from source.ui.game_window import GameWindow
from source.ui.ui_panel import UIPanel
from source.ship.ship import Ship

class Game:
    def __init__(self, config=None):
        self.config = config
        #set up font
        self.render_engine = RenderEngine(
            tcod.tileset.load_tilesheet("terminal12x12_gs_ro.png", 16, 16, tcod.tileset.CHARMAP_CP437),
            50,
            50,
            self)
        self.event_engine = EventEngine(self)
        self.InputHandler:InputHandler = InputHandler()
        self.game_state = 'main_menu'
        if config is not None:
            self.state_flags = config
        else:
            self.state_flags = {}

        #generate main menu
        if 'debug' in self.state_flags and self.state_flags['debug']:
            self.main_menu = generate_dev_menu(self.render_engine.SCREEN_WIDTH//3, self.render_engine.SCREEN_HEIGHT//3)
        else:
            self.main_menu = generate_main_menu(self.render_engine.SCREEN_WIDTH//3, self.render_engine.SCREEN_HEIGHT//3)
        self.current_menu = self.main_menu
        self.render_engine.add_element_to_ui('main_menu', self.main_menu)

        #generate game menu
        self.game_menu = generate_game_menu(self.render_engine.SCREEN_WIDTH//3, self.render_engine.SCREEN_HEIGHT//3)
        self.render_engine.add_element_to_ui('game_menu', self.game_menu)
        self.game_menu.visible = False

    def start_new_game(self):
        
        #Code to generate initial system
        self.galaxy = Galaxy()
        self.current_location = self.galaxy.galaxy_generator.generate_solar_system(50, 50)
        self.galaxy.galaxy_generator.generate_planets(self.current_location)
        self.current_location.explored = True
        self.galaxy.system_dict[(self.current_location.x, self.current_location.y)] = self.current_location
        self.current_area:Area = None
        self.generate_current_area()
        main_game_window = GameWindow(0, 0, self.render_engine.SCREEN_HEIGHT - 8, self.render_engine.SCREEN_WIDTH, self.current_area, self)
        self.render_engine.add_element_to_ui('game_window', main_game_window)
        self.render_engine.ui['main_menu'].visible = False
        self.render_engine.ui['hud'].visible = True

        #Code to generate player
        # None,{'x': 1, 'y': 1}
        self.player = Player()
        player_ship = Ship('@', (255,255,255), is_player=True, priority_draw=True, curr_area = self.current_area)
        self.player.assign_ship(player_ship)
        self.player.current_ship.engine.vector.x = 1
        self.player.current_ship.engine.vector.y = 1
        self.player.current_ship.relocate(7.0, 7.0)

    def start_dev(self):
        self.player = Player()
        player_ship = Ship('@', (255,255,255), is_player=True, priority_draw=True)
        self.player.assign_ship(player_ship)
        self.player.current_ship.engine.vector.x = 1
        self.player.current_ship.engine.vector.y = 1
        self.player.current_ship.x = 7.0
        self.player.current_ship.y = 7.0
        
        #Code to generate dev system
        self.galaxy = Galaxy()
        self.current_location = System(0, 0, 'O', (0, 255, 0), 'DevStar', 'dev-system', 30)
        self.current_location.explored = True
        self.galaxy.system_dict[(self.current_location.x, self.current_location.y)] = self.current_location
        self.current_area:Area = None
        self.generate_current_area()
        self.current_area.add_entity(self.player.current_entity)
        self.player.current_ship.engine.generate_vector_path()
        self.generate_dev_panel()
        self.render_engine.InputHandler.key_command_dict[tcod.event.K_F10] = {"type": "menu", "value": "dev"}
        main_game_window = GameWindow(0, 0, self.render_engine.SCREEN_HEIGHT - 8, self.render_engine.SCREEN_WIDTH, self.current_area, self)
        self.state_flags['no-jump'] = True
        self.render_engine.add_element_to_ui('game_window', main_game_window)
        self.render_engine.ui['main_menu'].visible = False
        self.render_engine.ui['hud'].visible = True

    def generate_dev_panel(self):
        dev_panel = UIPanel(0, 0, self.render_engine.SCREEN_HEIGHT - 8, 15, (0, 0, 50))
        dev_menu = generate_dev_command_menu(0, 1)
        spawn_entity_menu = generate_spawn_entity_menu(0, 1)
        spawn_entity_menu.visible = False
        dev_panel.elements['command_menu'] = dev_menu
        dev_panel.elements['spawn_entity'] = spawn_entity_menu
        self.render_engine.add_element_to_ui('dev', dev_panel)
        self.render_engine.ui['dev'].visible = False

    #TODO: Look at save load after core game structure is more settled.
    def save_game(self):
        save_dict = {
            'galaxy': self.galaxy,
            'global_time': self.event_engine.global_time,
            'global_queue': self.event_engine.global_queue,
            'player': self.player,
            'current_location': self.current_location,
            'current_area': self.current_area,
            'state_flags': self.state_flags
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
                self.event_engine.global_time = data['global_time']
                self.event_engine.global_queue = data['global_queue']
                self.player = data['player']
                self.current_location = data['current_location']
                self.current_area = data['current_area']
                self.state_flags = data['state_flags']
        except FileNotFoundError:
            pass

    def generate_current_area(self):
        self.current_area = self.current_location.generate_area()

