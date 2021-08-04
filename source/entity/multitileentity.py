from source.entity.entity import Entity

class MultiTileEntity:
    def __init__(self, x, y, char, color, radius, **flags):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.radius = radius
        self.flags = flags
    
    def point_inside(self, x, y):
        dx = abs(x - self.x)
        dy = abs(y - self.y)
        tempradius = self.radius + 0.5
        if self.radius <= 2:
            return dx**2 + dy**2 <= tempradius**2
        else:
            return dx**2 + dy**2 < tempradius**2

    def draw(self, root_console, topx, topy, bgcolor, **kwargs) -> None:
        """Draw this entity onto the screen.

        Args:
            topx (int): The left most x coordinate of the screen.
            topy (int): The bottom most(tcod counts y up from the bottom) of the y coordinate of the screen.
            bgcolor (tuple): the background color to set if the entity does not have a background color
        """
        #find the offset coordinates and draw on that point
        if ('bgcolor' in self.flags):
            root_console.tiles_rgb[self.x-topx, self.y-topy] = self.flags['bgcolor']
        else:
            root_console.tiles_rgb[self.x-topx, self.y-topy] = bgcolor
        root_console.print(self.x-topx, self.y-topy, self.char,fg=self.color)
    
    def offset_draw(self, root_console, topx, topy, drawx, drawy, bgcolor, **kwargs) -> None:
        """Draw this entity onto the screen.

        Args:
            topx (int): The left most x coordinate of the screen.
            topy (int): The bottom most(tcod counts y up from the bottom) of the y coordinate of the screen.
            bgcolor (tuple): the background color to set if the entity does not have a background color
        """
        #find the offset coordinates and draw on that point
        if ('bgcolor' in self.flags):
            root_console.tiles_rgb[drawx-topx, drawy-topy] = self.flags['bgcolor']
        else:
            root_console.tiles_rgb[drawx-topx, drawy-topy] = bgcolor
        root_console.print(drawx-topx, drawy-topy, self.char, fg=self.color)