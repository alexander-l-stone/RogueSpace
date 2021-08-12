import tcod

#TODO: Maybe mark this as in system?
class GameWindow:
    def __init__(self, x, y, height, width, area, game, hidden=False, **flags):
    #Note that when increasing x or y, you must decrease height and width respectively by the same amount to keep it square
        self.x:int = x
        self.y:int = y
        self.height:int = height
        self.width:int = width
        self.area = area
        self.hidden = hidden
        self.game = game
        self.flags = flags
    
    def draw(self, root_console, tick_count, **flags):
        #TODO:Allow better adjustment of where this window actually is
        if self.hidden:
            return
        if 'center_x' not in flags:
            center_x = self.game.player.current_entity.x
        else:
            center_x = flags['center_x']
        if 'center_y' not in flags:
            center_y = self.game.player.current_entity.y
        else:
            center_y = flags['center_y']
        self.area.draw(root_console, center_x, center_y, tick_count, self.width, self.height, corner_l_x=self.x, corner_b_y=self.y)

