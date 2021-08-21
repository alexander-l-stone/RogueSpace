class Menu:
    def __init__(self, x, y):
        self.menu_items:list = []
        self.active_item:int = 0
        self.menu_title:str = ''
        self.x = x
        self.y = y
        self.visible = True
        self.priority = 2

    def __str__(self) -> str:
        return_string = ''
        for item in self.menu_items:
            return_string = f"{return_string}\n{item}"
        return return_string

    def __repr__(self) -> str:
        return_string = ''
        for item in self.menu_items:
            return_string = f"{return_string}\n{item}"
        return return_string

    
    def draw(self, root_console, tick_count):
        if not self.visible:
            return
        try:
            start_height = self.y
            start_width = self.x
            for index in range(len(self.menu_items)):
                #TODO: Print entire string not by char index
                for char_index in range(len(self.menu_items[index].message)):
                    if self.menu_items[index].disabled:
                        root_console.print(start_width + char_index, start_height + index, self.menu_items[index].message[char_index],fg=self.menu_items[index].disabled_color)
                    else:
                        if index == self.active_item:
                            root_console.print(start_width + char_index, start_height + index, self.menu_items[index].message[char_index],fg=self.menu_items[index].active_color)
                        else:
                            root_console.print(start_width + char_index, start_height + index, self.menu_items[index].message[char_index],fg=self.menu_items[index].default_color)
        except IndexError:
            raise IndexError