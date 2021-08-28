import tcod.event
from typing import Dict

#TODO: Figure out a good way of doing input handling.
#TODO: Add Import/Export of key commands to/from a config file. Probably json for now.

class InputHandler:
    def __init__(self):
        self.galaxy_command_dict = {
            tcod.event.K_UP: {"type": "navigate", "value": (0, -1), "time":1},
            tcod.event.K_w: {"type": "navigate", "value": (0, -1), "time":1},
            tcod.event.K_KP_8: {"type": "navigate", "value": (0, -1), "time":1},
            tcod.event.K_DOWN: {"type": "navigate", "value": (0, 1), "time":1},
            tcod.event.K_s: {"type": "navigate", "value": (0, 1), "time":1},
            tcod.event.K_KP_2: {"type": "navigate", "value": (0, 1), "time":1},
            tcod.event.K_LEFT: {"type": "navigate", "value": (-1, 0), "time":1},
            tcod.event.K_a: {"type": "navigate", "value": (-1, 0), "time":1},
            tcod.event.K_KP_4: {"type": "navigate", "value": (-1, 0), "time":1},
            tcod.event.K_RIGHT: {"type": "navigate", "value": (1, 0), "time":1},
            tcod.event.K_d: {"type": "navigate", "value": (1, 0), "time":1},
            tcod.event.K_KP_6: {"type": "navigate", "value": (1, 0), "time":1},
            tcod.event.K_KP_9: {"type": "navigate", "value": (1, -1), "time":1},
            tcod.event.K_KP_7: {"type": "navigate", "value": (-1, -1), "time":1},
            tcod.event.K_KP_1: {"type": "navigate", "value": (-1, 1), "time":1},
            tcod.event.K_KP_3: {"type": "navigate", "value": (1, 1), "time":1},
        }

        self.system_command_dict = {
            tcod.event.K_UP: {"type": "thrust", "value": (0, -1), "time":1},
            tcod.event.K_w: {"type": "thrust", "value": (0, -1), "time":1},
            tcod.event.K_KP_8: {"type": "thrust", "value": (0, -1), "time":1},
            tcod.event.K_DOWN: {"type": "thrust", "value": (0, 1), "time":1},
            tcod.event.K_s: {"type": "thrust", "value": (0, 1), "time":1},
            tcod.event.K_KP_2: {"type": "thrust", "value": (0, 1), "time":1},
            tcod.event.K_LEFT: {"type": "thrust", "value": (-1, 0), "time":1},
            tcod.event.K_a: {"type": "thrust", "value": (-1, 0), "time":1},
            tcod.event.K_KP_4: {"type": "thrust", "value": (-1, 0), "time":1},
            tcod.event.K_RIGHT: {"type": "thrust", "value": (1, 0), "time":1},
            tcod.event.K_d: {"type": "thrust", "value": (1, 0), "time":1},
            tcod.event.K_KP_6: {"type": "thrust", "value": (1, 0), "time":1},
            tcod.event.K_KP_9: {"type": "thrust", "value": (1, -1), "time":1},
            tcod.event.K_KP_7: {"type": "thrust", "value": (-1, -1), "time":1},
            tcod.event.K_KP_1: {"type": "thrust", "value": (-1, 1), "time":1},
            tcod.event.K_KP_3: {"type": "thrust", "value": (1, 1), "time":1},
            tcod.event.K_KP_5: {"type": "wait", "time":1},
            53: {"type": "wait", "time":1}, #The number 5
            tcod.event.K_j: {"type": "jump", "time":1},
            tcod.event.K_f: {"type": "cheat-fuel", "time":1},
            tcod.event.K_ESCAPE: {"type": "menu", "value": "game", "time":1},
        }
    
    def handle_keypress(self, event) -> Dict[str,str]:
        if event.sym in self.system_command_dict:
            return self.system_command_dict[event.sym]
        else:
            return {'type': "none"}