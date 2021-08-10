from source.entity.entity import Entity

class Player:
    def __init__(self):
        self.current_entity = None
        self.current_ship = None
        #TODO: Add stuff here
    
    def assign_ship(self, ship) -> None:
        self.current_ship = ship
        self.current_entity = self.current_ship.entity_repr

    def draw(self, topx, topy, override_color=None) -> None:
        self.current_entity.draw(topx, topy, override_color)