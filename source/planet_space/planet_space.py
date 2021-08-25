from source.draw.entity.entity import Entity
from source.draw.area.tilsetarea import TilesetArea
from source.tileset.tileset import Tileset

class PlanetSpace:
    def __init__(self, planet_type, space_type, height, width, seed, **flags):
        self.planet_type = planet_type
        self.space_type = space_type
        self.seed = seed
        self.height = height
        self.width = width
        #TODO: Figure out how tilesets are generated
        self.tileset = Tileset(
            {0: Entity(0, 0, '~', (0, 0, 255), None)},
            {1: Entity(0, 0, '.', (0, 255, 0), None)},
            {2: Entity(0, 0, '^', (80, 80, 80), None)},
            )
        self.flags = flags
    
    def generate_area(self) -> TilesetArea:
        new_area = TilesetArea(self.tileset, self.height, self.width, **self.flags)
        #TODO: Actuall generate the area
        return new_area