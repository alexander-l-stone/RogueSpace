import tcod.event
from typing import Dict

#TODO: Figure out a good way of doing input handling.

class MenuHandler:
    def __init__(self):
        pass
    
    def handle_keypress(self, event) -> Dict[str,str]:
        if(event.sym == tcod.event.K_UP or event.sym == tcod.event.K_w or event.sym == tcod.event.K_KP_8):
            return {"type": "up"}
        elif(event.sym == tcod.event.K_DOWN or event.sym == tcod.event.K_s or event.sym == tcod.event.K_KP_2):
            return {"type": "down"}
        elif(event.sym == tcod.event.K_KP_ENTER):
            return {"type": "select"}
        else:
            return {"type": "none"}