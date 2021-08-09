import tcod

from typing import Dict
from source.entity.entity import Entity

class Area:
    def __init__(self, bg=(0,0,0), **flags):
        self.entity_dict: dict = {}
        self.background_color = bg
        self.flags = flags
    
    def __str__(self):
        return f"[Area | flags: {self.flags}]"
    
    def __repr__(self) -> str:
        return f"[Area | flags: {self.flags}]"

    def add_entity(self, new_entity) -> None:
        """Adds an entity to the area at the entities x, y coordinates. Make sure they are set correctly.

        Args:
            new_entity (Entity): The entity to be added.
        """
        if (new_entity.x, new_entity.y) in self.entity_dict:
            self.entity_dict[(new_entity.x, new_entity.y)].append(new_entity)
        else:
            self.entity_dict[(new_entity.x, new_entity.y)] = [new_entity]
        new_entity.curr_area = self

    def add_entity_at_coordinates(self, x, y, new_entity) -> None:
        """Add a new entity to an area at the provided coordinates.

        Args:
            x (int): x coordinate to add the entity too
            y (int): y coordinate to add the entity too
            new_entity (Entity): The Entity to add to the area.
        """
        if (x,y) in self.entity_dict:
            self.entity_dict[(x,y)].append(new_entity)
        else:
            self.entity_dict[(x, y)] = [new_entity]
        new_entity.x = x
        new_entity.y = y
        new_entity.curr_area = self

    #TODO: make an actual delete at coordinates but also a generic delete entity maybe?
    def delete_entity_at_coordinates(self, entity, x, y) -> Entity:
        """[summary]

        Args:
            entity ([type]): [description]
            x ([type]): [description]
            y ([type]): [description]

        Returns:
            Entity: [description]
        """,
        try:
            if (x,y) in self.entity_dict:
                self.entity_dict[(x,y)].remove(entity)
                entity.curr_area = None
            return entity
        except ValueError:
            return None
    
    #TODO: Add transfer and delete multi tile entity
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

    def get_entities_at_coordinates(self, x, y) -> list:
        """Get a list of entities at the given coordinates

        Args:
            x (int): x coordinate to grab list of entities from
            y (int): y coordinate to grab list of entities from

        Returns:
            list: The list of entities at the given coordinates.
        """
        if (x, y) in self.entity_dict:
            return self.entity_dict[(x, y)]
        else:
            return []
    
    def draw(self, root_console, playerx, playery, tick_count, screen_width, screen_height, **config) -> None:
        """Draw everything in the visible area

        Args:
            playerx (int): The x coordinate the player is at
            playery (int): The y coordinate the player is at
            screen_width (int): [description]
            screen_height (int): [description]
            config(dict): On occasion there could be configuration flags passed through here
        """
        animation_frame = tick_count//50
        corner_x = playerx - screen_width//2
        corner_y = playery - screen_height//2
        root_console.default_bg = self.background_color
        for drawx in range(playerx - screen_width//2, playerx + screen_width//2):
            for drawy in range(playery - screen_height//2, playery + screen_height//2):
                entities_at_point = self.get_entities_at_coordinates(drawx, drawy)
                 #TODO: Do the below in a way that doesn't suck
                if entities_at_point is not None and len(entities_at_point) > 0:
                    i = animation_frame % len(entities_at_point)
                    if len(entities_at_point) > 1:
                        if 'priority_draw' in entities_at_point[-1].flags:
                            entities_at_point[-1].draw(root_console, corner_x, corner_y, self.background_color, animation_frame, other_entities=entities_at_point[0::-1])
                        else:
                            entities_at_point[-i].draw(root_console, corner_x, corner_y, self.background_color, animation_frame, other_entities=entities_at_point[0::-1])
                    else:
                        entities_at_point[-1].draw(root_console, corner_x, corner_y, self.background_color, animation_frame)
               