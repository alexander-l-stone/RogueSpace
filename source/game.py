import pickle
import tcod
import tcod.event
from typing import Dict

from source.action.action import Action
from source.action.action_queue import ActionQueue
from source.area.area import Area
from source.helper_functions.circle_conversions import *
from source.entity.entity import Entity
from source.galaxy.galaxy import Galaxy
from source.handlers.input_handler import InputHandler
from source.action.jump_action import JumpAction
from source.menu.menu import Menu
from source.menu.menu_item import MenuItem
from source.action.move_action import MoveAction
from source.planet.planet import Planet
from source.player.player import Player
from source.helper_functions.colliders import stop_collision
from source.helper_functions.circle_conversions import *
from source.system.system import System
from source.ui.ui_panel import UIPanel

class Game:
    def __init__(self, config:Dict={}):
        self.config = config
        #set up font
        tcod.console_set_custom_font("terminal12x12_gs_ro.png", tcod.FONT_LAYOUT_ASCII_INROW | tcod.FONT_TYPE_GREYSCALE,)
        self.SCREEN_WIDTH:int = 50
        self.SCREEN_HEIGHT:int = 50
        self.global_time:int = 0
        self.global_queue = ActionQueue()
        self.InputHandler:InputHandler = InputHandler()
        self.bot_ui = UIPanel(0, self.SCREEN_HEIGHT - 8, 8, self.SCREEN_WIDTH)
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
        player_entity = Entity(1, 1, '@', (255,255,255), flags={'is_player': True})
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

    def render(self) -> None:
        self.current_area.draw(self.player.current_entity.x, self.player.current_entity.y, self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        self.bot_ui.draw()
        self.bot_ui.print_string(self.SCREEN_WIDTH//2 - len(f"{self.player.current_entity.x}, {-self.player.current_entity.y}")//2, 1, f"{self.player.current_entity.x}, {-self.player.current_entity.y}")
        if not isinstance(self.current_location, Galaxy):
            self.bot_ui.print_string(self.SCREEN_WIDTH//2 - len(self.current_location.name)//2, 2, self.current_location.name, )
        if isinstance(self.current_location, Planet):
            self.bot_ui.print_string(self.SCREEN_WIDTH//2 - len(f"Planetary Radius: {self.current_location.planetary_radius}")//2, 3, f"Planetary Radius: {self.current_location.planetary_radius}", (0, 255, 0))
            self.bot_ui.print_string(self.SCREEN_WIDTH//2 - len(f"Moons: {len(self.current_location.moons)}")//2, 4, f"Moons: {len(self.current_location.moons)}")
        elif isinstance(self.current_location, System):
            self.bot_ui.print_string(self.SCREEN_WIDTH//2 - len(f"Hyperlimit: {self.current_location.hyperlimit}")//2, 3, f"Hyperlimit: {self.current_location.hyperlimit}", (255, 0, 0))
            self.bot_ui.print_string(self.SCREEN_WIDTH//2 - len(f"Planets: {len(self.current_location.planet_list)}")//2, 4, f"Planets: {len(self.current_location.planet_list)}")
        tcod.console_flush()

    def resolve_actions(self):
        results = self.global_queue.resolve_actions(self.global_time)
        for result in results:
            if result["type"] == "enter":
                self.resolve_enter(result)
            elif result["type"] == "jump":
                self.resolve_jump(result)
            elif result["type"] == "move" and isinstance(self.current_location, Galaxy):
                for key, value in self.current_location.check_explored_corners(self.player.current_entity.x, self.player.current_entity.y, self.SCREEN_WIDTH, self.SCREEN_HEIGHT).items():
                    if (value == False):
                        self.current_location.generate_new_sector(key[0], key[1])
                if (
                self.player.current_entity.x <= self.current_area.kwargs['center_x'] - self.SCREEN_WIDTH//2
                or
                self.player.current_entity.x >= self.current_area.kwargs['center_x'] + self.SCREEN_WIDTH//2
                or
                self.player.current_entity.y <= self.current_area.kwargs['center_y'] - self.SCREEN_HEIGHT//2
                or
                self.player.current_entity.y >= self.current_area.kwargs['center_y'] - self.SCREEN_HEIGHT//2
                ):
                    self.current_area = self.current_location.generate_local_area(self.player.current_entity.x, self.player.current_entity.y)
                    self.current_area.add_entity(self.player.current_entity)
        if(isinstance(self.current_location, Planet)):
            for result in self.current_location.test_for_exit_planetary_area(self.current_area):
                if result["type"] == 'exit':
                    self.resolve_exit(result)

    def resolve_enter(self, result):
    #TODO: figure out what to do for non-player entities
        if (result['entering_entity'].flags['is_player']) is True:
            self.current_location = result['target_entity']
            dx, dy = result['entering_entity'].x - result['target_entity'].x, result['entering_entity'].y - result['target_entity'].y
            theta = convert_delta_to_theta(dx, dy)
            self.current_location.entity_list.append(result['entering_entity'])
            if (isinstance(self.current_location, Planet)):
                result['entering_entity'].x, result['entering_entity'].y = int(self.current_location.planetary_radius*math.cos(theta)), int(self.current_location.planetary_radius*math.sin(theta))
            elif (isinstance(self.current_location, System)):
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
            if(isinstance(self.current_location, Planet)):
                self.current_location = self.current_location.system
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
                for key, value in self.current_location.check_explored_corners(self.player.current_entity.x, self.player.current_entity.y, self.SCREEN_WIDTH, self.SCREEN_HEIGHT).items():
                        if (value == False):
                            self.current_location.generate_new_sector(key[0], key[1])
                self.current_area = self.current_location.generate_local_area(self.player.current_entity.x, self.player.current_entity.y)
                self.current_area.add_entity(self.player.current_entity)
                return True
            else:
                return False

    def resolve_keyboard_input(self, result):
        print(f"result: {result}")
        if(result["type"] == "move"):
            self.global_queue.push(MoveAction(self.player.current_entity, self.global_time+1, result["value"][0], result["value"][1], self.current_area, is_player=True))
        elif(result["type"] == "jump"):
            self.global_queue.push(JumpAction(self.player.current_entity, self.global_time+1, self.player.current_entity.x, self.player.current_entity.y, self.current_area, is_player=True))
        elif(result["type"] == "wait"):
            self.global_queue.push(Action(self.player.current_entity, self.global_time+1, lambda: [], is_player=True))
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

    def menu_loop(self, root_console, menu):
            for event in tcod.event.wait():
                if event.type == "KEYDOWN":
                    result = menu.handle_key_presses(event)
                    self.resolve_menu_kb_input(result)
                if event.type == "QUIT":
                    raise SystemExit()
            root_console.clear()
            menu.render(self.SCREEN_HEIGHT, self.SCREEN_WIDTH, root_console)


    def console_loop(self) -> None:
        with tcod.console_init_root(self.SCREEN_HEIGHT, self.SCREEN_WIDTH, order='F', vsync=False) as root_console:
            while not tcod.console_is_window_closed():
                root_console.clear()
                if (self.game_state == 'game'):
                    self.game_loop(root_console)
                elif (self.game_state == 'main_menu'):
                    self.menu_loop(root_console, self.main_menu)
                elif (self.game_state == 'game_menu'):
                    self.menu_loop(root_console, self.game_menu)

    def game_loop(self, root_console) -> None:
            self.render()
            if self.global_queue.player_actions_count > 0:
                self.resolve_actions()
                self.global_time += 1
            else:
                for event in tcod.event.wait():
                    if event.type == "KEYDOWN":
                        result = self.InputHandler.handle_keypress(event)
                        self.resolve_keyboard_input(result)
                    if event.type == "QUIT":
                        raise SystemExit()
            root_console.clear()
            self.render()