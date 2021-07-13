import tcod

class UIPanel:
    def __init__(self, x:int, y:int, panel_height:int, panel_width:int, border_char:str = '#'):
        self.x:int = x
        self.y:int = y
        self.panel_height:int = panel_height
        self.panel_width:int = panel_width
        self.border_char:str = border_char

    def draw(self):
        """
        Draw this UIPanel
        """
        #Make a Rectangle
        tcod.console_set_default_foreground(0, tcod.gray)
        for x in range(self.x, self.x + self.panel_width):
            tcod.console_put_char(0, x, self.y, self.border_char, tcod.BKGND_NONE)
            tcod.console_put_char(0, x, self.y + self.panel_height-1, self.border_char, tcod.BKGND_NONE)
        for y in range(self.y, self.y + self.panel_height):
            tcod.console_put_char(0, self.x, y, self.border_char, tcod.BKGND_NONE)
            tcod.console_put_char(0, self.x + self.panel_width-1, y, self.border_char, tcod.BKGND_NONE)
    
    def print_string(self, x:int, y:int, message:str, color:tuple = (255, 255, 255)):
        """
        Prints a string to the ui panel, offset from the panels upper right corner by x and y
        """
        i = 0
        y2 = 0
        while i < len(message):
            tcod.console_set_default_foreground(0, color)
            tcod.console_put_char(0, self.x + x + (i - y2*(self.panel_width-2)), self.y + y, message[i], tcod.BKGND_NONE)
            i += 1
            if (i - y2*(self.panel_width-2)) > self.panel_width-2:
                y2 += 1
