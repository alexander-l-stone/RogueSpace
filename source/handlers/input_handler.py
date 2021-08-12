import tcod.event
from typing import Dict

#TODO: Figure out a good way of doing input handling.
#TODO: Add Import/Export of key commands to/from a config file. Probably json for now.

class InputHandler:
    def __init__(self):
        self.key_command_dict = {
            tcod.event.K_UP: {"type": "thrust", "value": (0, -1)},
            tcod.event.K_w: {"type": "thrust", "value": (0, -1)},
            tcod.event.K_KP_8: {"type": "thrust", "value": (0, -1)},
            tcod.event.K_DOWN: {"type": "thrust", "value": (0, 1)},
            tcod.event.K_s: {"type": "thrust", "value": (0, 1)},
            tcod.event.K_KP_2: {"type": "thrust", "value": (0, 1)},
            tcod.event.K_LEFT: {"type": "thrust", "value": (-1, 0)},
            tcod.event.K_a: {"type": "thrust", "value": (-1, 0)},
            tcod.event.K_KP_4: {"type": "thrust", "value": (-1, 0)},
            tcod.event.K_RIGHT: {"type": "thrust", "value": (1, 0)},
            tcod.event.K_d: {"type": "thrust", "value": (1, 0)},
            tcod.event.K_KP_6: {"type": "thrust", "value": (1, 0)},
            tcod.event.K_KP_9: {"type": "thrust", "value": (1, -1)},
            tcod.event.K_KP_7: {"type": "thrust", "value": (-1, -1)},
            tcod.event.K_KP_1: {"type": "thrust", "value": (-1, 1)},
            tcod.event.K_KP_3: {"type": "thrust", "value": (1, 1)},
            tcod.event.K_KP_5: {"type": "wait"},
            53: {"type": "wait"}, #The number 5
            tcod.event.K_j: {"type": "jump"},
            tcod.event.K_f: {"type": "cheat-fuel"},
            tcod.event.K_ESCAPE: {"type": "menu", "value": "open"},
        }
    
    def handle_keypress(self, event) -> Dict[str,str]:
        if event.sym in self.key_command_dict:
            return self.key_command_dict[event.sym]
        else:
            return {'type': "none"}