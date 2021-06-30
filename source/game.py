import tcod
import tcod.event
from typing import Dict

from source.action.action import Action
from source.action.move_action import MoveAction
from source.action.action_queue import ActionQueue
from source.area.area import Area
from source.entity.entity import Entity
from source.handlers.input_handler import InputHandler
from source.helper_functions.colliders import stop_collision
from source.player.player import Player
class Game:
    def __init__(self, config:Dict={}):
        self.config = config
        #set up font
        tcod.console_set_custom_font("terminal8x12_gs_ro.png", tcod.FONT_LAYOUT_ASCII_INROW | tcod.FONT_TYPE_GREYSCALE,)
        self.SCREEN_WIDTH:int = 50
        self.SCREEN_HEIGHT:int = 50
        self.global_time = 0
        self.global_queue = ActionQueue()
        self.InputHandler:InputHandler = InputHandler()
        player_entity = Entity(0, 0, '@', (255,255,255), flags={'is_player': True})
        new_entity = Entity(1,1, '#', (255,0,0), flags={'on_collide': stop_collision})
        self.player = Player(player_entity)
        self.current_area = Area()
        self.current_area.add_entity(player_entity)
        self.current_area.add_entity(new_entity)

    def render(self) -> None:
        self.current_area.draw(self.player.current_entity.x, self.player.current_entity.y, self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        tcod.console_flush()
    
    def game_loop(self) -> None:
        with tcod.console_init_root(self.SCREEN_HEIGHT, self.SCREEN_WIDTH, order='F', vsync=False) as root_console:
            root_console.clear()
            self.render()
            while not tcod.console_is_window_closed():
                if self.global_queue.player_actions_count > 0:
                    self.global_queue.resolve_actions(self.global_time)
                    self.global_time += 1
                    root_console.clear()
                    self.render()
                else:
                    for event in tcod.event.wait():
                        if event.type == "KEYDOWN":
                            result = self.InputHandler.handle_keypress(event)
                            if(result["type"] == "move"):
                               self.global_queue.push(MoveAction(self.player.current_entity, self.global_time+1, result["value"][0], result["value"][1], self.current_area))
                        if event.type == "QUIT":
                            raise SystemExit()