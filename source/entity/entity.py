import tcod

#TODO: Change flags to a **kwargs field
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
    
    def __str__(self):
        return f"[Char: {self.char} | {self.x}, {self.y}]"
    
    def __repr__(self) -> str:
        return f"[Char: {self.char} | {self.x}, {self.y}]"
    
    def draw(self, topx, topy, bgcolor, override_color=None,) -> None:
        """Draw this entity onto the screen.

        Args:
            topx (int): The left most x coordinate of the screen.
            topy (int): The bottom most(tcod counts y up from the bottom) of the y coordinate of the screen.
            bgcolor (tuple): the background color to set if the entity does not have a background color
            override_color (tuple, optional): [description]. Defaults to None. This will override the entities base color. Used only for debugging purposes with fov.
        """
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
        tcod.console_set_default_background(0, bgcolor)