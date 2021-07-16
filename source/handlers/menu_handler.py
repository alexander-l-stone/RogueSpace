import tcod.event
from typing import Dict

#TODO: Figure out a good way of doing input handling.

class MenuHandler:
    def __init__(self):
        pass
    
    #TODO: figure out if these need to be dicts or if they can be strings
    def handle_keypress(self, event) -> Dict[str, str]:
        if(event.sym == tcod.event.K_UP or event.sym == tcod.event.K_w or event.sym == tcod.event.K_KP_8):
            return {"type": "up"}
        elif(event.sym == tcod.event.K_DOWN or event.sym == tcod.event.K_s or event.sym == tcod.event.K_KP_2):
            return {"type": "down"}
        #TODO: figure out the actual tcod.event enums for these numbers, they appear to be space and enter
        elif(event.sym == 32 or event.sym == 13):
            return {"type": "select"}
        else:
            return {"type": "none"}