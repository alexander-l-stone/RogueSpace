import tcod

from typing import List, Dict
from source.entity.entity import Entity

class Area:
    def __init__(self):
        self.entity_dict: Dict = {}

    def add_entity(self, new_entity) -> None:
        self.entity_dict[(new_entity.x, new_entity.y)] = new_entity
        new_entity.curr_area = self

    def add_entity_at_coordinates(self, x, y, new_entity) -> None:
        self.entity_dict[(x, y)] = new_entity
        new_entity.x = x
        new_entity.y = y
        new_entity.curr_area = self

    def delete_entity_at_coordinates(self, x, y) -> Entity:
        self.entity_dict[(x, y)].curr_area = None
        return self.entity_dict.pop((x, y))
    
    def transfer_entity_between_coordinates(self, x1, y1, x2, y2) -> None:
        """Moves the entity at x1, y1 to x2, y2

        Args:
            x1 ([integer]): The X coordinate the entity is starting at
            y1 ([integer]): The Y coordinate the entity is starting at
            x2 ([integer]): The X coordinate the entity will end up at
            y2 ([integer]): The Y coordinate the entity will end up at
        """
        transfering_entity = self.delete_entity_at_coordinates(x1, y1)
        self.add_entity_at_coordinates(x2, y2, transfering_entity)

    def get_entity_at_coordinates(self, x, y) -> Entity:
        if (x, y) in self.entity_dict:
            return self.entity_dict[(x, y)]
        else:
            return None
    
    def draw(self, playerx, playery, screen_width, screen_height, **config) -> None:
        corner_x = playerx - screen_width//2
        corner_y = playery - screen_height//2        
        for drawx in range(playerx - screen_width//2, playerx + screen_width//2):
            for drawy in range(playery - screen_height//2, playery + screen_height//2):
                entity_at_point = self.get_entity_at_coordinates(drawx, drawy)
                if entity_at_point is not None:
                    entity_at_point.draw(corner_x, corner_y)