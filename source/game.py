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
from source.action.move_action import MoveAction
from source.planet.planet import Planet
from source.player.player import Player
from source.ring.ring import Ring
from source.helper_functions.colliders import stop_collision
from source.helper_functions.circle_conversions import *
from source.system.system import System

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
        
        #Code to generate player
        player_entity = Entity(1, 1, '@', (255,255,255), flags={'is_player': True})
        self.player = Player(player_entity)
        
        #Code to generate initial system
        self.galaxy = Galaxy()
        self.current_location = self.galaxy.galaxy_generator.generate_solar_system(50, 50)
        self.galaxy.system_dict[(self.current_location.x, self.current_location.y)] = self.current_location
        self.current_area:Area = None
        self.generate_current_area()
        self.current_area.add_entity(player_entity)

    def generate_current_area(self):
        self.current_area = self.current_location.generate_area()

    #TODO: Figure out why entities exiting planets(and presumably systems) don't appear until they move
    def render(self) -> None:
        self.current_area.draw(self.player.current_entity.x, self.player.current_entity.y, self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
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
        if(result["type"] == "move"):
            self.global_queue.push(MoveAction(self.player.current_entity, self.global_time+1, result["value"][0], result["value"][1], self.current_area))
        elif(result["type"] == "jump"):
            self.global_queue.push(JumpAction(self.player.current_entity, self.global_time+1, self.player.current_entity.x, self.player.current_entity.y, self.current_area))
    
    def game_loop(self) -> None:
        with tcod.console_init_root(self.SCREEN_HEIGHT, self.SCREEN_WIDTH, order='F', vsync=False) as root_console:
            root_console.clear()
            self.render()
            while not tcod.console_is_window_closed():
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