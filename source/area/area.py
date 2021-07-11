import tcod

from typing import List, Dict
from source.entity.entity import Entity

class Area:
    def __init__(self, bg=(0,0,0), **kwargs):
        self.entity_dict: Dict = {}
        self.background_color = bg
        self.kwargs = kwargs

    def add_entity(self, new_entity) -> None:
        if (new_entity.x, new_entity.y) in self.entity_dict:
            self.entity_dict[(new_entity.x, new_entity.y)].append(new_entity)
        else:
            self.entity_dict[(new_entity.x, new_entity.y)] = [new_entity]
        new_entity.curr_area = self

    def add_entity_at_coordinates(self, x, y, new_entity) -> None:
        if (x,y) in self.entity_dict:
            self.entity_dict[(x,y)].append(new_entity)
        else:
            self.entity_dict[(x, y)] = [new_entity]
        new_entity.x = x
        new_entity.y = y
        new_entity.curr_area = self

    #TODO: make an actual delete at coordinates but also a generic delete entity maybe?
    def delete_entity_at_coordinates(self, entity, x, y) -> Entity:
        if (x,y) in self.entity_dict:
            self.entity_dict[(x,y)].remove(entity)
            entity.curr_area = None
        return entity
    
    def transfer_entity_between_coordinates(self, entity, x1, y1, x2, y2) -> None:
        """Moves the entity at x1, y1 to x2, y2

        Args:
            x1 ([integer]): The X coordinate the entity is starting at
            y1 ([integer]): The Y coordinate the entity is starting at
            x2 ([integer]): The X coordinate the entity will end up at
            y2 ([integer]): The Y coordinate the entity will end up at
        """
        transfering_entity = self.delete_entity_at_coordinates(entity, x1, y1)
        self.add_entity_at_coordinates(x2, y2, transfering_entity)

    def get_entities_at_coordinates(self, x, y) -> Entity:
        if (x, y) in self.entity_dict:
            return self.entity_dict[(x, y)]
        else:
            return []
    
    def draw(self, playerx, playery, screen_width, screen_height, **config) -> None:
        corner_x = playerx - screen_width//2
        corner_y = playery - screen_height//2
        tcod.console_set_default_background(0, self.background_color)
        for drawx in range(playerx - screen_width//2, playerx + screen_width//2):
            for drawy in range(playery - screen_height//2, playery + screen_height//2):
                entities_at_point = self.get_entities_at_coordinates(drawx, drawy)
                if entities_at_point is not None and len(entities_at_point) > 0:
                    entities_at_point[-1].draw(corner_x, corner_y, self.background_color)