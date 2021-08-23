import math

from source.action.action_queue import ActionQueue
from source.action.action import Action
from source.action.resolution_functions import *
from source.helper_functions.circle_conversions import *
from source.galaxy.galaxy import Galaxy
from source.system.system import System

class EventEngine:
    def __init__(self, game):
        self.global_time = 0
        self.global_queue = ActionQueue()
        self.game = game
    
    def resolve_actions(self):
        results = self.global_queue.resolve_actions(self.global_time)
        for result in results:
            if result["type"] == "enter":
                self.resolve_enter(result)
            elif result["type"] == "jump":
                if ('no-jump' in self.game.state_flags):
                    return
                self.resolve_jump(result)
            elif result["type"] == "move" and isinstance(self.game.current_location, Galaxy):
                for key, value in self.game.current_location.check_explored_corners(self.game.player.current_ship.get_x(), self.game.player.current_ship.get_y(), self.game.render_engine.SCREEN_WIDTH, self.game.render_engine.SCREEN_HEIGHT).items():
                    if (value == False):
                        self.game.current_location.generate_new_sector(key[0], key[1])
                if (
                self.game.player.current_ship.get_x() <= self.game.current_area.flags['center_x'] - self.game.render_engine.SCREEN_WIDTH//2
                or
                self.game.player.current_ship.get_x() >= self.game.current_area.flags['center_x'] + self.game.render_engine.SCREEN_WIDTH//2
                or
                self.game.player.current_ship.get_y() <= self.game.current_area.flags['center_y'] - self.game.render_engine.SCREEN_HEIGHT//2
                or
                self.game.player.current_ship.get_y() >= self.game.current_area.flags['center_y'] - self.game.render_engine.SCREEN_HEIGHT//2
                ):
                    self.game.current_area = self.game.current_location.generate_local_area(self.game.player.current_ship.get_x(), self.game.player.current_ship.get_y())
                    self.game.current_area.add_entity(self.game.player.current_entity)
                    self.game.render_engine.ui['game_window'].area = self.game.current_area
    
    def resolve_enter(self, result):
    #TODO: figure out what to do for non-player entities
        if (result['entering_entity'].flags['is_player']) is True:
            self.game.current_location = result['target_entity']
            dx, dy = result['entering_entity'].x - result['target_entity'].x, result['entering_entity'].y - result['target_entity'].y
            theta = convert_delta_to_theta(dx, dy)
            self.game.current_location.entity_list.append(result['entering_entity'])
            if (isinstance(self.game.current_location, System)):
                if(self.game.current_location.explored == False):
                    self.game.galaxy.galaxy_generator.generate_planets(self.game.current_location)
                    self.game.current_location.explored = True
                result['entering_entity'].x, result['entering_entity'].y = int(self.game.current_location.hyperlimit*math.cos(theta)), int(self.game.current_location.hyperlimit*math.sin(theta))
            self.game.generate_current_area()
            self.game.current_area.add_entity(self.game.player.current_entity)
            self.game.render_engine.ui['game_window'].area = self.game.current_area
    
    def resolve_exit(self, result):
        if ('is_player' in result['exiting_entity'].flags and result['exiting_entity'].flags['is_player'] is True):
            theta = convert_delta_to_theta(result['exiting_entity'].x, result['exiting_entity'].y)
            delta = convert_theta_to_delta(theta)
            result['exiting_entity'].x, result['exiting_entity'].y = self.current_location.x + delta[0], self.game.current_location.y + delta[1]
            self.game.current_location.entity_list.append(result['exiting_entity'])
            self.game.generate_current_area()
            self.game.current_area.add_entity(self.game.player.current_entity)
    
    def resolve_jump(self, result):
        if(not isinstance(self.game.current_location, System) ==True):
            return False
        else:
            if (((self.game.player.current_ship.get_x()**2) + (self.game.player.current_ship.get_y()**2))**(1/2)) > self.game.current_location.hyperlimit:
                delta = convert_theta_to_delta(convert_delta_to_theta(result['x'], result['y']))
                new_x = self.game.current_location.x + delta[0]
                new_y = self.game.current_location.y + delta[1]
                self.game.current_location = self.game.galaxy
                self.game.player.current_ship.x = new_x
                self.game.player.current_ship.y = new_y
                for key, value in self.game.current_location.check_explored_corners(self.game.player.current_ship.get_x(), self.game.player.current_ship.get_y(), self.game.render_engine.SCREEN_WIDTH, self.game.render_engine.SCREEN_HEIGHT).items():
                        if (value == False):
                            self.game.current_location.generate_new_sector(key[0], key[1])
                self.game.current_area = self.game.current_location.generate_local_area(self.game.player.current_ship.get_x(), self.game.player.current_ship.get_y())
                self.game.current_area.add_entity(self.game.player.current_entity)
                self.game.render_engine.ui['game_window'].area = self.game.current_area
                return True
            else:
                return False



    def resolve_keyboard_input(self, result):
        if(result["type"] == "move"):
            self.global_queue.push(Action(self.game.player.current_ship, self.global_time+1, resolve_move_action, dx=result["value"][0], dy=result["value"][1], area=self.game.current_area, is_player=True))
        elif(result["type"] == "jump"):
            self.global_queue.push(Action(self.game.player.current_ship, self.global_time+1, resolve_jump_action, y=self.game.player.current_ship.get_x(), x=self.game.player.current_ship.get_y(), area=self.game.current_area, is_player=True))
        elif(result["type"] == "wait"):
            actions = self.game.player.current_ship.engine.generate_move_actions(self.global_time, 1)
            for action in actions:
                self.global_queue.push(action)
            self.global_queue.push(Action(self.game.player.current_ship, self.global_time+1, resolve_wait_action, is_player=True))
        elif(result["type"] == "thrust"):
            self.game.player.current_ship.thrust(result["value"][0], result["value"][1])
            actions = self.game.player.current_ship.engine.generate_move_actions(self.global_time,1)
            for action in actions:
                self.global_queue.push(action)
        elif(result["type"] == "cheat-fuel"):
            self.game.player.current_ship.fuel += 10
        elif(result["type"] == "menu"):
            if result["value"] == 'game':
                self.game.game_state = "game_menu"
                self.game.current_menu = self.game.game_menu
                self.game.render_engine.ui['game_menu'].visible = True
                self.game.render_engine.ui['game_window'].visible = False
                self.game.render_engine.ui['hud'].visible = False
            elif result["value"] == 'dev-system':
                self.game.game_state = "menu_command_menu_render"
                self.game.current_menu = self.game.render_engine.ui["dev"].elements["command_menu"]
                self.game.render_engine.ui["dev"].visible = True
            elif result["value"] == "dev-tileset":
                



    def handle_menu_key_presses(self, result) -> dict:
        key_result = {'type': 'none'}
        if result['type'] == 'select':
            key_result = self.game.current_menu.menu_items[self.game.current_menu.active_item].kwargs['select']()
        elif result['type'] == 'up':
            if self.game.current_menu.active_item > 0:
                self.game.current_menu.active_item -= 1
            key_result = {'type': 'move', 'value': 'up'}
        elif result['type'] == 'down':
            if self.game.current_menu.active_item < len(self.game.current_menu.menu_items) - 1:
                self.game.current_menu.active_item += 1
            key_result = {'type': 'move', 'value': 'down'}
        return key_result

    def resolve_menu_kb_input(self, result):
        if result['type'] == 'exit':
            raise SystemExit()
        elif result['type'] == 'game':
            if result['value'] == 'new':
                self.game.start_new_game()
            elif result['value'] == 'load':
                self.game.load_game()
            elif result['value'] == 'dev':
                self.game.start_dev()
            self.game.game_state = 'game'
        elif result['type'] == 'close':
            self.game.game_state = 'game'
            if 'debug' in self.game.state_flags and self.game.state_flags['debug']:
                self.game.render_engine.ui['dev'].visible = False
            self.game.render_engine.ui['game_menu'].visible = False
            self.game.render_engine.ui['game_window'].visible = True
            self.game.render_engine.ui['hud'].visible = True
        elif result['type'] == 'open':
            if result["value"] == 'spawn_entity':
                self.game.current_menu = self.game.render_engine.ui['dev'].elements['spawn_entity']
                self.game.game_state = 'menu_spawn_entity_render'
                self.game.render_engine.ui['dev'].elements['command_menu'].visible = False
                self.game.render_engine.ui['dev'].elements['spawn_entity'].visible = True
            elif result["value"] == 'command_menu':
                self.game.current_menu = self.game.render_engine.ui['dev'].elements['command_menu']
                self.game.game_state = 'menu_command_menu_render'
                self.game.render_engine.ui['dev'].elements['command_menu'].visible = True
                self.game.render_engine.ui['dev'].elements['spawn_entity'].visible = False
        elif(result["type"] == "save"):
            self.game.save_game()
            self.game.game_state = "game"