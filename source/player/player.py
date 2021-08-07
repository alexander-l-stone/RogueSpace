from source.entity.entity import Entity

class Player:
    def __init__(self, entity):
        self.current_entity = entity
        self.current_entity.parent = self
        #TODO: Add stuff here
    
    def draw(self, topx, topy, override_color=None) -> None:
        self.current_entity.draw(topx, topy, override_color)