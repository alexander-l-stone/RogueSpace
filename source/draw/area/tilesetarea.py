import tcod
import numpy

from typing import Dict
from source.draw.area.area import Area
from source.draw.entity.entity import Entity
from source.tileset.tileset import Tileset

class TilesetArea(Area):
    def __init__(self, tileset, height, width, bg=(0,0,0), **flags):
        Area.__init__(self, bg, **flags)
        self.tileset = Tileset(tileset)
        self.height = height
        self.width = width
        self.entity_array = numpy.array([])
        self.explored_array = numpy.array([])
        #TODO figure out if we want an array of walkable tiles
        #TODO Figure out if we want an array of vision blocking tiles
    
    def init_area(self, key=0):
        self.entity_array = numpy.array([[key for y in range(self.height)] for x in range(self.width)])
        self.explored_array = numpy.array([[False for y in range(self.height)] for x in range(self.width)])
    

    def draw(self, root_console, centerx, centery, tick_count, screen_width, screen_height, corner_l_x=0, corner_b_y=0, **config) -> None:
        """Draw everything in the visible area

        Args:
            centerx (int): The x coordinate the player is at
            centery (int): The y coordinate the player is at
            screen_width (int): [description]
            screen_height (int): [description]
            corner_d_x (int): The x coordinate of the corner(leftmost) this draws from
            corner_d_y (int): The y coordinate of the cornery(bottomost) this draws from
            config(dict): On occasion there could be configuration flags passed through here
        """
        animation_frame = tick_count//50
        root_console.default_bg = self.background_color
        for drawx in range(centerx - screen_width//2, centerx + screen_width//2):
            for drawy in range(centery - screen_height//2, centery + screen_height//2):
                entities_at_point = self.get_entities_at_coordinates(drawx, drawy).copy()
                #TODO: Do the below in a way that doesn't suck
                if entities_at_point is not None and len(entities_at_point) > 0:
                    i = animation_frame % len(entities_at_point)
                    if len(entities_at_point) > 1:
                        priority_entity = False
                        for entity in entities_at_point[::-1]:
                            if 'priority_draw' in entity.flags:
                                priority_entity = entity
                                break
                        if priority_entity:
                            entities_at_point.remove(priority_entity)
                            priority_entity.draw(root_console, centerx - screen_width//2 - corner_l_x, centery - screen_height//2 - corner_b_y, self.background_color, animation_frame, other_entities=entities_at_point)
                        else:
                            drawn_entity = entities_at_point[-i]
                            entities_at_point.remove(drawn_entity)
                            drawn_entity.draw(root_console, centerx - screen_width//2 - corner_l_x, centery - screen_height//2 - corner_b_y, self.background_color, animation_frame, other_entities=entities_at_point, debug=True)
                    else:
                        entities_at_point[-1].draw(root_console, centerx - screen_width//2 - corner_l_x, centery - screen_height//2 - corner_b_y, self.background_color, animation_frame)
                else:
                    #TODO Check if tile is visible. If not draw some shitty explored but out of vision version
                    if drawx in self.entity_array:
                        if drawy in self.entity_array[drawx]:
                            #grab the tile and set its coordinates to the proper coordinats
                            #This assumes tile is an Entity
                            tile = self.tileset.tiles[self.entity_array[drawx][drawy]]
                            tile.parent = self.tileset
                            tile.x = drawx
                            tile.y = drawy
                            tile.x_offset = drawx
                            tile.y_offset = drawy
                            self.tileset.tiles[self.entity_array[drawx][drawy]].draw(root_console, centerx - screen_width//2 - corner_l_x, centery - screen_height//2 - corner_b_y, self.background_color, animation_frame)
