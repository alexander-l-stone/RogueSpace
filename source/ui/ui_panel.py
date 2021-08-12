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
        self.elements = {}
        self.hidden = False

    def draw(self, root_console) -> None:
        if self.hidden:
            return
        self.draw_background(root_console)
        for elem in self.elements.values():
            elem.draw(root_console)

    def draw_background(self, root_console):
        """
        Draw this UIPanel
        """
        root_console.draw_frame(self.x, self.y, self.panel_width, self.panel_height, clear=True, fg=(255,255,255), bg=self.panel_color, decoration=self.decoration_tuple)

