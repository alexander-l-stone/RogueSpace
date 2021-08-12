import tcod
import time
import sys

from source.draw.entity.newtonian_entity import NewtonianEntity
from source.galaxy.galaxy import Galaxy
from source.handlers.input_handler import InputHandler
from source.system.system import System
from source.ui.menu.generate_menu import generate_dev_command_menu, generate_spawn_entity_menu
from source.ui.menu.menu import Menu
from source.ui.menu.menu_item import MenuItem
from source.ui.ui_bar import UIBar
from source.ui.ui_message import UIMessage
from source.ui.ui_panel import UIPanel

#TODO Rework entire render framework
"""
    Should have a list of things to render and just render those. Game Window should be a ui element that can be rendered/not rendered.
    The Menu/Current menu should be replaced by the abo
"""
class RenderEngine:
    def __init__(self, tileset, screen_height, screen_width, game):
        self.tileset = tileset
        self.SCREEN_HEIGHT = screen_height
        self.SCREEN_WIDTH = screen_width
        self.game = game
        self.InputHandler = InputHandler()

        STATUS_LABEL_WIDTH = 8
        STATUS_BAR_WIDTH = 10
        STATUS_WIDTH = STATUS_LABEL_WIDTH + STATUS_BAR_WIDTH
        panel = UIPanel(0, self.SCREEN_HEIGHT - 8, 8, self.SCREEN_WIDTH, (20, 20, 20))
        panel.elements['label_health'] = UIMessage(panel, 1, 1, 'Health', (255,255,255))
        panel.elements['bar_health'] = UIBar(panel, STATUS_LABEL_WIDTH, 1, STATUS_BAR_WIDTH, 1, (0, 255, 0), (0, 120, 0), (0, 0, 0), 45, 100)
        panel.elements['label_heat'] = UIMessage(panel, 1, 2, 'Heat', (255,255,255))
        panel.elements['bar_heat'] = UIBar(panel, STATUS_LABEL_WIDTH, 2, STATUS_BAR_WIDTH, 1, (255, 0, 0), (120, 0, 0), (0, 0, 0), 33, 100)
        panel.elements['label_fuel'] = UIMessage(panel, 1, 3, 'Fuel', (255,255,255))
        panel.elements['bar_fuel'] = UIBar(panel, STATUS_LABEL_WIDTH, 3, STATUS_BAR_WIDTH, 1, (255, 255, 0), (120, 120, 0), (0, 0, 0), 77, 100)

        MESSAGE_CENTER = (screen_width - STATUS_WIDTH) / 2 + STATUS_WIDTH
        MESSAGE_LEFT = int(MESSAGE_CENTER - 3)
        panel.elements['coordinates'] = UIMessage(panel, MESSAGE_LEFT, 2, '(0, 0)', (255, 255, 255))
        panel.elements['vector'] = UIMessage(panel, MESSAGE_LEFT, 3, '(0, 0)', (255, 255, 255))

        self.ui = {'hud': panel}
        self.tick_count = 0
    
    def generate_dev_panel(self):
        dev_panel = UIPanel(0, 0, self.SCREEN_HEIGHT - 8, 15, (0, 0, 50))
        dev_menu = generate_dev_command_menu(0, 1)
        spawn_entity_menu = generate_spawn_entity_menu(0, 1)
        spawn_entity_menu.hidden = True
        dev_panel.elements['command_menu'] = dev_menu
        dev_panel.elements['spawn_entity'] = spawn_entity_menu
        self.ui['dev'] = dev_panel
        self.ui['dev'].hidden = True

    #TODO: Change the center of the screen that the player character knows to be the center of the visible area not taken up by ui.
    # Probably make a seprate UI element that is the game panel?
    def render(self, root_console) -> None:
        self.tick_count += 1
        if self.tick_count == sys.maxsize:
            self.tick_count = 0
        if self.game.game_state != 'game' and self.game.game_state.split('_')[-1] != 'render':
            self.game.current_menu.draw(root_console)
        else:
            self.update_hud()
            self.game.current_area.draw(root_console, self.game.player.current_entity.x, self.game.player.current_entity.y, self.tick_count, self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
            for panel in self.ui.values():
                # draw all panels
                panel.draw(root_console)

    def update_hud(self) -> None:
        hud = self.ui['hud']
        # TODO if the player becomes not a ship, make this a switch
        hud.elements['bar_health'].curr_value = self.game.player.current_ship.health
        hud.elements['bar_health'].max_value = self.game.player.current_ship.max_health
        hud.elements['bar_heat'].curr_value = self.game.player.current_ship.heat
        hud.elements['bar_heat'].max_value = self.game.player.current_ship.max_heat
        hud.elements['bar_fuel'].curr_value = self.game.player.current_ship.fuel
        hud.elements['bar_fuel'].max_value = self.game.player.current_ship.max_fuel

        hud.elements['coordinates'].message = f"({self.game.player.current_entity.x}, {self.game.player.current_entity.y})"
        hud.elements['vector'].message = f"({self.game.player.current_entity.vector.x}, {self.game.player.current_entity.vector.y})"

    def game_loop(self):
        with tcod.context.new_terminal(self.SCREEN_HEIGHT, self.SCREEN_WIDTH, tileset=self.tileset, title="Rogue Expedition", vsync=True) as context:
            root_console = tcod.Console(self.SCREEN_HEIGHT, self.SCREEN_WIDTH, order='F')
            while True:
                context.present(root_console)
                if (self.game.game_state == 'game'):
                    self.event_loop(root_console)
                elif (self.game.game_state == 'main_menu'):
                    self.menu_loop(root_console, self.game.main_menu)
                elif (self.game.game_state == 'game_menu'):
                    self.menu_loop(root_console, self.game.game_menu)
                elif (self.game.game_state == 'menu_command_menu_render'):
                    self.menu_loop(root_console, self.game.render_engine.ui['dev'].elements['command_menu'])
                elif (self.game.game_state == 'menu_spawn_entity_render'):
                    self.menu_loop(root_console, self.game.render_engine.ui['dev'].elements['spawn_entity'])
                self.render_console(root_console)
    
    def render_console(self, root_console) -> None:
        root_console.clear()
        self.render(root_console)

    def event_loop(self, root_console) -> None:
        if self.game.event_engine.global_queue.player_actions_count > 0:
            self.game.event_engine.resolve_actions()
            if type(self.game.player.current_entity) is NewtonianEntity:
                self.game.player.current_entity.generate_vector_path()
            self.game.event_engine.global_time += 1
        else:
            for event in tcod.event.get():
                if event.type == "KEYDOWN":
                    result = self.InputHandler.handle_keypress(event)
                    self.game.event_engine.resolve_keyboard_input(result)
                if event.type == "QUIT":
                    raise SystemExit()


    def menu_loop(self, root_console, menu):
        for event in tcod.event.get():
            if event.type == "KEYDOWN":
                result = menu.handle_key_presses(event)
                self.game.event_engine.resolve_menu_kb_input(result)
            if event.type == "QUIT":
                raise SystemExit()
        root_console.clear()

