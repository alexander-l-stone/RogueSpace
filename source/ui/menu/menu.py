import tcod

from source.handlers.menu_handler import MenuHandler

class Menu:
    def __init__(self, x, y):
        self.menu_items:list = []
        self.active_item:int = 0
        self.menu_title:str = ''
        self.MenuHandler:MenuHandler = MenuHandler()
        self.x = x
        self.y = y
        self.hidden = False

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

    
    def draw(self, root_console):
        """Render this menu. Only works if there is more than 0 menu items.

        Args:
            sh (int): Screen Height
            sw (int): Screen Width
        """
        if self.hidden:
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
    
    def handle_key_presses(self, event) -> dict:
        if event.type == 'KEYDOWN':
            result = self.MenuHandler.handle_keypress(event)
            key_result = {'type': 'none'}
            if result['type'] == 'select':
                key_result = self.menu_items[self.active_item].kwargs['select']()
            elif result['type'] == 'up':
                if self.active_item > 0:
                    self.active_item -= 1
                key_result = {'type': 'move', 'value': 'up'}
            elif result['type'] == 'down':
                if self.active_item < len(self.menu_items) - 1:
                    self.active_item += 1
                key_result = {'type': 'move', 'value': 'down'}
            return key_result
        else:
            return {'type': 'none'}
