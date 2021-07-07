from source.area.area import Area
from source.galaxy_generator.galaxy_generator import GalaxyGenerator

class Galaxy:
    def __init__(self):
        self.explored_dict = {}
        self.system_dict = {}
        self.sector_size:int = 500
        self.galaxy_generator = GalaxyGenerator()
    
    def check_if_coordinate_is_explored(self, x, y) -> bool:
        rounded_x = int(x/self.sector_size)
        rounded_y = int(y/self.sector_size)
        if (x < 0):
            rounded_x = rounded_x - 1
        if (y < 0):
            rounded_y = rounded_y - 1
        return (rounded_x, rounded_y) in self.explored_dict
    
    def generate_local_area(self, x, y):
        new_area = Area()
        for drawx in range(x - self.sector_size//2, x + self.sector_size//2):
            for drawy in range(y - self.sector_size//2, y + self.sector_size//2):
                if (drawx, drawy) in self.system_dict:
                    new_area.add_entity(self.system_dict[(drawx, drawy)].generate_star_entity())
    
    def generate_new_sector(self, x, y):
        #round down to the nearest sector size
        rounded_x = int(x/self.sector_size)
        #reduce negatives by 1
        if (x < 0):
            rounded_x = rounded_x - 1
        rounded_y = int(y/self.sector_size)
        if (y < 0):
            rounded_y = rounded_y - 1
        self.explored_dict[(rounded_x, rounded_y)] = True
        