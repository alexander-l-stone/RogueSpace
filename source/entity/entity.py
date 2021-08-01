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
    
    def draw(self, root_console, topx, topy, bgcolor, **kwargs) -> None:
        """Draw this entity onto the screen.

        Args:
            topx (int): The left most x coordinate of the screen.
            topy (int): The bottom most(tcod counts y up from the bottom) of the y coordinate of the screen.
            bgcolor (tuple): the background color to set if the entity does not have a background color
            override_color (tuple, optional): [description]. Defaults to None. This will override the entities base color. Used only for debugging purposes with fov.
        """
        #find the offset coordinates and draw on that point
        root_console.draw_rect(self.x-topx, self.y-topy, 1, 1, ord(self.char),fg=self.color, bg=bgcolor)