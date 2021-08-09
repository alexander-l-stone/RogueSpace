import tcod
class Entity:
    def __init__(self, x:int, y:int, char, color, parent, **flags:dict):
        self.x:int = x
        self.y:int = y
        if type(char) is str:
            self.char = [char]
        else:
            self.char = char
        if type(color) is tuple:
            self.color = [color]
        else:
            self.color = color
        self.parent = parent
        self.curr_area = None
        self.flags:dict = flags
    
    def __str__(self):
        return f"[{self.parent} ({self.x}, {self.y})]"
    
    def __repr__(self) -> str:
        return f"[{self.parent} ({self.x}, {self.y})]"
    
    def draw(self, root_console, topx, topy, bgcolor, animation_frame, **flags) -> None:
        """Draw this entity onto the screen.

        Args:
            topx (int): The left most x coordinate of the screen.
            topy (int): The bottom most(tcod counts y up from the bottom) of the y coordinate of the screen.
            bgcolor (tuple): the background color to set if the entity does not have a background color
            override_color (tuple, optional): [description]. Defaults to None. This will override the entities base color. Used only for debugging purposes with fov.
        """
        #find the offset coordinates and draw on that point
        animation_char_frame = animation_frame % len(self.char)
        animation_color_frame = animation_frame % len(self.color)

        #Step 1 Find BG Color
        background_color = None
        if 'bg_color' in self.flags and self.flags['bg_color'] != bgcolor:
            background_color = self.flags['bg_color']
        elif 'other_entities' in flags and flags['other_entities'] is not None:
            for entity in flags['other_entities']:
                if 'bg_color' in entity.flags:
                    background_color = entity.flags['bg_color']
                    break
        if background_color is None:
            background_color = bgcolor
        #Step 2 find Entity and FG Color
        print_char = self.char[animation_char_frame]
        fg_color = self.color[animation_color_frame]
        if print_char == ' ':
            if 'other_entities' in flags and flags['other_entities'] is not None:
                for entity in flags['other_entities']:
                    if entity.char[animation_char_frame] != ' ':
                        print_char = entity.char[animation_char_frame]
                        fg_color = entity.color[animation_color_frame]
        #Step 3 Print
        root_console.print(self.x-topx, self.y-topy, print_char, fg=fg_color, bg=background_color)