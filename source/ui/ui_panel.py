import tcod

class UIPanel:
    def __init__(self, x:int, y:int, panel_height:int, panel_width:int, panel_color:tuple, border_char:str = ' ', **flags):
        self.x:int = x
        self.y:int = y
        self.panel_height:int = panel_height
        self.panel_width:int = panel_width
        self.panel_color:tuple = panel_color
        self.border_char:str = border_char
        self.flags = flags
        self.decoration_tuple:tuple = (ord(self.border_char), ord(self.border_char), ord(self.border_char), 
                                    ord(self.border_char), ord(' '), ord(self.border_char), 
                                    ord(self.border_char), ord(self.border_char), ord(self.border_char))

    def draw(self, root_console):
        """
        Draw this UIPanel
        """
        root_console.draw_frame(self.x, self.y, self.panel_width, self.panel_height, clear=True, fg=(255,255,255), bg=self.panel_color, decoration=self.decoration_tuple)

    def print_string(self, root_console, x:int, y:int, message:str, color:tuple = (255, 255, 255)):
        """
        Prints a string to the ui panel, offset from the panels upper right corner by x and y
        """
        i = 0
        y2 = 0
        while i < len(message):
            root_console.put_char(self.x + x + (i - y2*(self.panel_width-2)), self.y + y, ord(message[i]), tcod.BKGND_NONE)
            i += 1
            if (i - y2*(self.panel_width-2)) > self.panel_width-2:
                y2 += 1
