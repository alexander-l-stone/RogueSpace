import tcod.event
from typing import Dict

#TODO: Figure out a good way of doing input handling.

class InputHandler:
    def __init__(self):
        pass
    
    def handle_keypress(self, event) -> Dict[str,str]:
        if(event.sym == tcod.event.K_UP or event.sym == tcod.event.K_w or event.sym == tcod.event.K_KP_8):
            return {"type": "move", "value": (0, -1)}
        elif(event.sym == tcod.event.K_DOWN or event.sym == tcod.event.K_s or event.sym == tcod.event.K_KP_2):
            return {"type": "move", "value": (0, 1)}
        elif(event.sym == tcod.event.K_LEFT or event.sym == tcod.event.K_a or event.sym == tcod.event.K_KP_4):
            return {"type": "move", "value": (-1, 0)}
        elif(event.sym == tcod.event.K_RIGHT or event.sym == tcod.event.K_d or event.sym == tcod.event.K_KP_6):
            return {"type": "move", "value": (1, 0)}
        elif(event.sym == tcod.event.K_KP_9):
            return {"type": "move", "value": (1, -1)}
        elif(event.sym == tcod.event.K_KP_7):
            return {"type": "move", "value": (-1, -1)}
        elif(event.sym == tcod.event.K_KP_1):
            return {"type": "move", "value": (-1, 1)}
        elif(event.sym == tcod.event.K_KP_3):
            return {"type": "move", "value": (1, 1)}
        elif(event.sym == tcod.event.K_j):
            return {"type": "jump"}
        else:
            return {"type": "none"}