from source.draw.entity.entity import Entity
from source.draw.area.tilesetarea import TilesetArea
from source.tileset.tileset import Tileset

class PlanetSpace:
    def __init__(self, planet_type, space_type, height, width, seed, **flags):
        self.planet_type = planet_type
        self.space_type = space_type
        self.seed = seed
        self.height = height
        self.width = width
        self.explored = False
        self.x = 0
        self.y = 0
        #TODO: Figure out how tilesets are generated
        self.tileset = {
            0: Entity(0, 0, '~', (0, 0, 255), self),
            1: Entity(0, 0, '.', (0, 255, 0), self),
            2: Entity(0, 0, '^', (80, 80, 80), self),
            }
        self.flags = flags

    def generate_area(self) -> TilesetArea:
        import tcod
        #This is code to fill the tileset area with random entities
        new_area = TilesetArea(self.tileset, self.height, self.width, **self.flags)
        new_area.init_area()
        noise = tcod.noise.Noise(dimensions = 2)
        samples = noise[tcod.noise.grid(shape=(new_area.width, new_area.height), scale=0.25, origin=(new_area.width//2, new_area.height//2))]
        samples = (samples + 1) * 256
        for x in range(new_area.width):
            for y in range(new_area.height):
                area_value = samples[x][y]
                if area_value < 96:
                    val = 0
                elif area_value < 164:
                    val = 1
                else:
                    val = 2
                new_area.entity_array[x][y] = val
        #TODO: Actuall generate the area
        return new_area