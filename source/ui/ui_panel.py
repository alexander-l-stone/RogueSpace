import tcod

class UIPanel:
    def __init__(self, x:int, y:int, panel_height:int, panel_width:int, border_char:str = '#'):
        self.x:int = x
        self.y:int = y
        self.panel_height:int = panel_height
        self.panel_width:int = panel_width
        self.border_char:str = border_char

    def draw(self, root_console):
        """
        Draw this UIPanel
        """
        #Make a Rectangle
        for x in range(self.x, self.x + self.panel_width):
            root_console.draw_rect(x, self.y, 1, 1, ord(self.border_char))
            root_console.draw_rect(x, self.y + self.panel_height-1, 1, 1, ord(self.border_char))
        for y in range(self.y, self.y + self.panel_height):
            root_console.draw_rect(self.x, y, 1, 1, ord(self.border_char))
            root_console.draw_rect(self.x + self.panel_width-1, y + self.panel_height-1, 1, 1, ord(self.border_char))
    
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
