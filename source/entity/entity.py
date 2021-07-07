import tcod

class Entity:
    def __init__(self, x:int, y:int, char:str, color:tuple, flags:dict=None):
        self.x:int = x
        self.y:int = y
        self.char:str = char
        self.color:tuple = color
        self.curr_area = None
        if flags == None:
            self.flags:dict = {}
        else:
            self.flags:dict = flags
    
    def draw(self, topx, topy, bgcolor, override_color=None,) -> None:
        if ('bg_color' not in self.flags):
            tcod.console_set_default_background(0, bgcolor)
        else:
            tcod.console_set_default_background(0, self.flags['bg_color'])
        if(override_color is None):
            tcod.console_set_default_foreground(0, self.color)
        else:
            tcod.console_set_default_foreground(0, override_color)
        #find the offset coordinates and draw on that point
        tcod.console_put_char(0, self.x-topx, self.y-topy, self.char, tcod.BKGND_DEFAULT)