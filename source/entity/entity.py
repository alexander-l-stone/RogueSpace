import tcod

#TODO: Change flags to a **kwargs field
class Entity:
    def __init__(self, x:int, y:int, char:str, color:tuple, parent, **flags:dict):
        self.x:int = x
        self.y:int = y
        self.char:str = char
        self.color:tuple = color
        self.parent = parent
        self.curr_area = None
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
        if ('bgcolor' in self.flags):
            root_console.tiles_rgb[self.x-topx, self.y-topy] = self.flags['bgcolor']
        else:
            root_console.tiles_rgb[self.x-topx, self.y-topy] = bgcolor
        root_console.print(self.x-topx, self.y-topy, self.char,fg=self.color)