import tcod

from source.handlers.menu_handler import MenuHandler

class Menu:
    def __init__(self):
        self.menu_items:list = []
        self.active_item:int = 0
        self.menu_title:str = ''
        self.MenuHandler:MenuHandler = MenuHandler()
    
    def render(self, sh, sw, console):
        """Render this menu. Only works if there is more than 0 menu items.

        Args:
            sh (int): Screen Height
            sw (int): Screen Width
        """
        try:
            start_height = int(sh//2 + len(self.menu_items)//2)
            start_width = int(sw//2 - len(self.menu_items[0].message)//2)
            for index in range(len(self.menu_items)):
                for char_index in range(len(self.menu_items[index].message)):
                    if self.menu_items[index].disabled:
                        tcod.console_set_default_foreground(0, self.menu_items[index].disabled_color)
                    else:
                        if index == self.active_item:
                            tcod.console_set_default_foreground(0, self.menu_items[index].active_color)
                        else:
                            tcod.console_set_default_foreground(0, self.menu_items[index].default_color)
                    tcod.console_put_char(console, start_width + char_index, start_height + index, self.menu_items[index].message[char_index])
            tcod.console_flush()
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
