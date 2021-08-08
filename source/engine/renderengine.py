import tcod

from source.handlers.input_handler import InputHandler
from source.ui.ui_panel import UIPanel
from source.galaxy.galaxy import Galaxy
from source.system.system import System
from source.entity.newtonian_entity import NewtonianEntity

class RenderEngine:
    def __init__(self, tileset, screen_height, screen_width, game):
        self.tileset = tileset
        self.SCREEN_HEIGHT = screen_height
        self.SCREEN_WIDTH = screen_width
        self.game = game
        self.InputHandler = InputHandler()
        self.bot_ui = UIPanel(0, self.SCREEN_HEIGHT - 8, 8, self.SCREEN_WIDTH, (20, 20, 20))

    def render(self, root_console) -> None:
        if self.game.game_state != 'game':
            self.game.current_menu.render(self.SCREEN_HEIGHT, self.SCREEN_WIDTH, root_console)
        else:
            self.game.current_area.draw(root_console, self.game.player.current_entity.x, self.game.player.current_entity.y, self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
            self.bot_ui.draw(root_console)
            self.bot_ui.print_string(root_console, self.SCREEN_WIDTH//2 - len(f"{self.game.player.current_entity.x}, {-self.game.player.current_entity.y}")//2, 1, f"{self.game.player.current_entity.x}, {-self.game.player.current_entity.y}")
            if not isinstance(self.game.current_location, Galaxy):
                self.bot_ui.print_string(root_console, self.SCREEN_WIDTH//2 - len(self.game.current_location.name)//2, 2, self.game.current_location.name, )
            elif isinstance(self.game.current_location, System):
                self.bot_ui.print_string(root_console, self.SCREEN_WIDTH//2 - len(f"Hyperlimit: {self.game.current_location.hyperlimit}")//2, 3, f"Hyperlimit: {self.game.current_location.hyperlimit}", (255, 0, 0))
                self.bot_ui.print_string(root_console, self.SCREEN_WIDTH//2 - len(f"Planets: {len(self.game.current_location.planet_list)}")//2, 4, f"Planets: {len(self.game.current_location.planet_list)}")

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
            for event in tcod.event.wait():
                if event.type == "KEYDOWN":
                    result = self.InputHandler.handle_keypress(event)
                    self.game.event_engine.resolve_keyboard_input(result)
                if event.type == "QUIT":
                    raise SystemExit()


    def menu_loop(self, root_console, menu):
        for event in tcod.event.wait():
            if event.type == "KEYDOWN":
                result = menu.handle_key_presses(event)
                self.game.event_engine.resolve_menu_kb_input(result)
            if event.type == "QUIT":
                raise SystemExit()
        root_console.clear()

