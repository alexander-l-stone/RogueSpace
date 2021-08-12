#This will contain that generates any/all menu's in the game
from source.ui.menu.menu import Menu
from source.ui.menu.menu_item import MenuItem

def generate_main_menu(x, y):
    main_menu = Menu(x, y)
    new_game = MenuItem('New Game', select=lambda: {'type': 'game', 'value': 'new'})
    load_game = MenuItem('Load Game', select=lambda: {'type': 'game', 'value': 'load'})
    exit_game = MenuItem('Exit', select=lambda: {'type': 'exit'})
    main_menu.menu_items.extend([new_game, load_game, exit_game])
    return main_menu

def generate_dev_menu(x, y):
    dev_menu = Menu(x, y)
    dev_mode = MenuItem('Start Dev Mode', select=lambda: {'type': 'game', 'value': 'dev'})
    exit_game = MenuItem('Exit', select=lambda: {'type': 'exit'})
    dev_menu.menu_items.extend([dev_mode, exit_game])
    return dev_menu

def generate_game_menu(x, y):
    game_menu = Menu(x, y)
    close_menu = MenuItem('Close Menu', select=lambda: {'type': 'close'})
    save_game = MenuItem('Save Game', select=lambda: {'type': 'save'})
    load_game = MenuItem('Load Game', select=lambda: {'type': 'game', 'value': 'load'})
    exit_game = MenuItem('Exit', select=lambda: {'type': 'exit'})
    game_menu.menu_items.extend([close_menu, save_game, load_game, exit_game])
    return game_menu

def generate_dev_command_menu(x, y):
    dev_menu = Menu(x, y)
    close_menu = MenuItem('Close Menu', select=lambda: {'type': "close"})
    spawn_entity = MenuItem('Spawn Entity', select=lambda: {'type': "open", "value": "spawn_entity"})
    dev_menu.menu_items.extend([close_menu, spawn_entity])
    return dev_menu

def generate_spawn_entity_menu(x, y):
    spawn_entity_menu = Menu(x, y)
    go_back = MenuItem('Go Back', select=lambda: {'type': "open", "value": "command_menu"})
    adjust_character = MenuItem('Character: @', disabled=True, select=lambda: {'type': 'string-input', 'value': 'spawn-entity-char', 'max-length': 1})
    adjust_red = MenuItem('Red: 255', disabled=True, select=lambda: {'type': 'numeric-input', 'value': 'red', 'min-value': 0, 'max-value': 255})
    adjust_green = MenuItem('Green: 255', disabled=True, select=lambda: {'type': 'numeric-input', 'value': 'green', 'min-value': 0, 'max-value': 255})
    adjust_blue = MenuItem('Blue: 255', disabled=True, select=lambda: {'type': 'numeric-input', 'value': 'blue', 'min-value': 0, 'max-value': 255})
    spawn_entity = MenuItem('Spawn Entity', disabled=True, select=lambda: {'type': "open", "value": "spawn-entity"})
    #TODO Show example entity at button
    #TODO Allow adjust background color as well as foreground
    #TODO Allow adjusting of coordinates that it is spawned at?
    #TODO Allow spanning of multiple entities
    spawn_entity_menu.menu_items.extend([go_back, adjust_character, adjust_red, adjust_green, adjust_blue, spawn_entity])
    return spawn_entity_menu