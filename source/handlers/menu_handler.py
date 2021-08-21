import tcod.event
from typing import Dict

#TODO: Figure out a good way of doing input handling.

class MenuHandler:
    def __init__(self):
        self.key_command_dict = {
            tcod.event.K_UP: {"type": "up"},
            tcod.event.K_w: {"type": "up"},
            tcod.event.K_KP_8: {"type": "up"},
            tcod.event.K_DOWN: {"type": "down"},
            tcod.event.K_s: {"type": "down"},
            tcod.event.K_KP_2: {"type": "down"},
            32: {"type": "select"}, #What key is this? Space I think
            13: {"type": "select"}, #What key is this? Enter I think
        }
    
    #TODO: figure out if these need to be dicts or if they can be strings
    def handle_keypress(self, event) -> Dict[str, str]:
        if event.sym in self.key_command_dict:
            return self.key_command_dict[event.sym]
        else:
            return {"type": "none"}