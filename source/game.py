from source.action.action import Action
import tcod
import tcod.event
from typing import Dict

from source.action.action_queue import ActionQueue
from source.handlers.input_handler import InputHandler

class Game:
    def __init__(self, config:Dict={}):
        self.config = config
        #set up font
        tcod.console_set_custom_font("terminal8x12_gs_ro.png", tcod.FONT_LAYOUT_ASCII_INROW | tcod.FONT_TYPE_GREYSCALE,)
        self.SCREEN_WIDTH:int = 50
        self.SCREEN_HEIGHT:int = 50
        self.global_time = 0
        self.global_queue = ActionQueue()

    def render(self) -> None:
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
                            #if(result["type"] == "move"):
                            #   self.player.move_action(result["value"][0], result["value"][1], result["value"][2], self.curr_area, self.global_queue)
                        if event.type == "QUIT":
                            raise SystemExit()