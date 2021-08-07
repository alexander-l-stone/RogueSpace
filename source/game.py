import pickle
import tcod
import tcod.event
from typing import Dict

from source.action.action import Action
from source.action.resolution_functions import *
from source.action.action_queue import ActionQueue
from source.area.area import Area
from source.entity.newtonian_entity import NewtonianEntity
from source.galaxy.galaxy import Galaxy
from source.handlers.input_handler import InputHandler
from source.menu.menu import Menu
from source.menu.menu_item import MenuItem
from source.planet.planet import Planet
from source.player.player import Player
from source.engine.renderengine import RenderEngine
from source.helper_functions.circle_conversions import *
from source.system.system import System
from source.ui.ui_panel import UIPanel

class Game:
    def __init__(self, config:Dict={}):
        self.config = config
        #set up font
        self.render_engine = RenderEngine(
            tcod.tileset.load_tilesheet("terminal12x12_gs_ro.png", 16, 16, tcod.tileset.CHARMAP_CP437),
            50,
            50,
            self)
        self.tileset = tcod.tileset.load_tilesheet("terminal12x12_gs_ro.png", 16, 16, tcod.tileset.CHARMAP_CP437)
        self.global_time:int = 0
        self.global_queue = ActionQueue()
        self.InputHandler:InputHandler = InputHandler()
        self.game_state = 'main_menu'

        #generate main menu
        self.main_menu = Menu()
        new_game = MenuItem('New Game', select=lambda: {'type': 'game', 'value': 'new'})
        load_game = MenuItem('Load Game', select=lambda: {'type': 'game', 'value': 'load'})
        exit = MenuItem('Exit', select=lambda: {'type': 'exit'})
        self.main_menu.menu_items.extend([new_game, load_game, exit])

        #generate game menu
        self.game_menu = Menu()
        save_game = MenuItem('Save Game', select=lambda: {'type': 'save'})
        close_menu = MenuItem('Close', select=lambda: {'type': 'close'})
        self.game_menu.menu_items.extend([save_game, load_game, exit, close_menu])

    def start_new_game(self):
        #Code to generate player
        # None,{'x': 1, 'y': 1}
        player_entity = NewtonianEntity(7, 7, '@', (255,255,255), None, {'x': 1, 'y': 1}, is_player=True)
        # player_entity = Entity(1, 1, '@', (255,255,255), flags={'is_player': True})
        self.player = Player(player_entity)
        
        #Code to generate initial system
        self.galaxy = Galaxy()
        self.current_location = self.galaxy.galaxy_generator.generate_solar_system(50, 50)
        self.galaxy.galaxy_generator.generate_planets(self.current_location)
        self.current_location.explored = True
        self.galaxy.system_dict[(self.current_location.x, self.current_location.y)] = self.current_location
        self.current_area:Area = None
        self.generate_current_area()
        self.current_area.add_entity(player_entity)
        self.player.current_entity.generate_vector_path()

    def save_game(self):
        save_dict = {
            'galaxy': self.galaxy,
            'global_time': self.global_time,
            'global_queue': self.global_queue,
            'player': self.player,
            'current_location': self.current_location,
            'current_area': self.current_area,
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
        except FileNotFoundError:
            pass

    def generate_current_area(self):
        self.current_area = self.current_location.generate_area()

    def resolve_actions(self):
        results = self.global_queue.resolve_actions(self.global_time)
        for result in results:
            if result["type"] == "enter":
                self.resolve_enter(result)
            elif result["type"] == "jump":
                self.resolve_jump(result)
            elif result["type"] == "move" and isinstance(self.current_location, Galaxy):
                for key, value in self.current_location.check_explored_corners(self.player.current_entity.x, self.player.current_entity.y, self.render_engine.SCREEN_WIDTH, self.render_engine.SCREEN_HEIGHT).items():
                    if (value == False):
                        self.current_location.generate_new_sector(key[0], key[1])
                if (
                self.player.current_entity.x <= self.current_area.flags['center_x'] - self.render_engine.SCREEN_WIDTH//2
                or
                self.player.current_entity.x >= self.current_area.flags['center_x'] + self.render_engine.SCREEN_WIDTH//2
                or
                self.player.current_entity.y <= self.current_area.flags['center_y'] - self.render_engine.SCREEN_HEIGHT//2
                or
                self.player.current_entity.y >= self.current_area.flags['center_y'] - self.render_engine.SCREEN_HEIGHT//2
                ):
                    self.current_area = self.current_location.generate_local_area(self.player.current_entity.x, self.player.current_entity.y)
                    self.current_area.add_entity(self.player.current_entity)

    def resolve_enter(self, result):
    #TODO: figure out what to do for non-player entities
        if (result['entering_entity'].flags['is_player']) is True:
            self.current_location = result['target_entity']
            dx, dy = result['entering_entity'].x - result['target_entity'].x, result['entering_entity'].y - result['target_entity'].y
            theta = convert_delta_to_theta(dx, dy)
            self.current_location.entity_list.append(result['entering_entity'])
            if (isinstance(self.current_location, System)):
                if(self.current_location.explored == False):
                    self.galaxy.galaxy_generator.generate_planets(self.current_location)
                    self.current_location.explored = True
                result['entering_entity'].x, result['entering_entity'].y = int(self.current_location.hyperlimit*math.cos(theta)), int(self.current_location.hyperlimit*math.sin(theta))
            self.generate_current_area()
            self.current_area.add_entity(self.player.current_entity)

    def resolve_exit(self, result):
        if ('is_player' in result['exiting_entity'].flags and result['exiting_entity'].flags['is_player'] is True):
            theta = convert_delta_to_theta(result['exiting_entity'].x, result['exiting_entity'].y)
            delta = convert_theta_to_delta(theta)
            result['exiting_entity'].x, result['exiting_entity'].y = self.current_location.x + delta[0], self.current_location.y + delta[1]
            self.current_location.entity_list.append(result['exiting_entity'])
            self.generate_current_area()
            self.current_area.add_entity(self.player.current_entity)
        
    def resolve_jump(self, result):
        if(not isinstance(self.current_location, System) ==True):
            return False
        else:
            if (((self.player.current_entity.x**2) + (self.player.current_entity.y**2))**(1/2)) > self.current_location.hyperlimit:
                delta = convert_theta_to_delta(convert_delta_to_theta(result['x'], result['y']))
                new_x = self.current_location.x + delta[0]
                new_y = self.current_location.y + delta[1]
                self.current_location = self.galaxy
                self.player.current_entity.x = new_x
                self.player.current_entity.y = new_y
                for key, value in self.current_location.check_explored_corners(self.player.current_entity.x, self.player.current_entity.y, self.render_engine.SCREEN_WIDTH, self.render_engine.SCREEN_HEIGHT).items():
                        if (value == False):
                            self.current_location.generate_new_sector(key[0], key[1])
                self.current_area = self.current_location.generate_local_area(self.player.current_entity.x, self.player.current_entity.y)
                self.current_area.add_entity(self.player.current_entity)
                return True
            else:
                return False

    def resolve_keyboard_input(self, result):
        if(result["type"] == "move"):
            self.global_queue.push(Action(self.player.current_entity, self.global_time+1, resolve_move_action, dx=result["value"][0], dy=result["value"][1], area=self.current_area, is_player=True))
        elif(result["type"] == "jump"):
            self.global_queue.push(Action(self.player.current_entity, self.global_time+1, resolve_jump_action, y=self.player.current_entity.x, x=self.player.current_entity.y, area=self.current_area, is_player=True))
        elif(result["type"] == "wait"):
            actions = self.player.current_entity.generate_move_actions(self.global_time+1)
            for action in actions:
                self.global_queue.push(action)
            self.global_queue.push(Action(self.player.current_entity, self.global_time+1, resolve_wait_action, is_player=True))
        elif(result["type"] == "thrust"):
            self.player.current_entity.thrust(result["value"][0], result["value"][1])
            actions = self.player.current_entity.generate_move_actions(self.global_time+1)
            for action in actions:
                self.global_queue.push(action)
        elif(result["type"] == "menu"):
            self.game_state = "game_menu"

    def resolve_menu_kb_input(self, result):
        if result['type'] == 'exit':
            raise SystemExit()
        elif result['type'] == 'game':
            if result['value'] == 'new':
                self.start_new_game()
            elif result['value'] == 'load':
                self.load_game()
            self.game_state = 'game'
        elif result['type'] == 'close':
            self.game_state = 'game'
        elif(result["type"] == "save"):
            self.save_game()
            self.game_state = "game"