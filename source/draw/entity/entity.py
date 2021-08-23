import tcod
class Entity:
    def __init__(self, x_offset:int, y_offset:int, char, color, parent, **flags:dict):
        self.parent = parent
        self.x_offset:int = x_offset
        self.y_offset:int = y_offset

        """
        World position of this entity is tracked as relative position from parent, using xoffset and yoffset.

        x and y track this entity's position in the area dictionary. 
        As an invariant, should match world position
        Used primarily to update the entity's position after a move.
        """
        self.x = self.get_abs_x()
        self.y = self.get_abs_y()

        if type(char) is str:
            self.char = [char]
        else:
            self.char = char
        if type(color) is tuple:
            self.color = [color]
        else:
            self.color = color

        if('curr_area' in flags):
            self.curr_area = flags['curr_area']
            flags.pop('curr_area')
            self.curr_area.add_entity(self)
        else:
            self.curr_area = None
        self.flags:dict = flags

    def __str__(self):
        return f"[{self.parent} ({self.parent.x + self.x_offset}, {self.parent.y + self.y_offset})]"
    
    def __repr__(self) -> str:
        return f"[{self.parent} ({self.parent.x + self.x_offset}, {self.parent.y + self.y_offset})]"

    def get_abs_x(self):
        return round(self.parent.x) + self.x_offset

    def get_abs_y(self):
        return round(self.parent.y) + self.y_offset
        
    def update_area_position(self):
        """
            update_entity.... will adjust this entity's position in the area dictionary to it's absolute position
            then, we update self.x and self.y accordingly
        """
        self.curr_area.update_coords_for_entity(self, self.x, self.y)
        self.x = self.get_abs_x()
        self.y = self.get_abs_y()

    

    def move_entity_to_coordinates(self, x, y) -> None:
        """Moves the entity to x, y by changing it's offset.

        Args:
            x ([integer]): The X coordinate the entity will end up at
            y ([integer]): The Y coordinate the entity will end up at
        """
        self.x_offset = x - self.parent.x
        self.y_offset = y - self.parent.y
        self.update_area_position()

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
        root_console.print(self.get_abs_x() - topx, self.get_abs_y() - topy, print_char, fg=fg_color, bg=background_color)