from source.draw.area.area import Area
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
    
    def check_explored_corners(self, x, y, screen_width, screen_height):
        top_x = x + screen_width//2
        bot_x = x - screen_width//2
        top_y = y + screen_height//2
        bot_y = y - screen_height//2
        return {
            (top_x, top_y): self.check_if_coordinate_is_explored(top_x, top_y),
            (top_x, bot_y): self.check_if_coordinate_is_explored(top_x, bot_y),
            (bot_x, top_y): self.check_if_coordinate_is_explored(bot_x, top_y),
            (bot_x, bot_y): self.check_if_coordinate_is_explored(bot_x, bot_y)
            }
    
    def generate_local_area(self, x, y):
        new_area = Area(bg=(30,0,0), center_x= x, center_y= y)
        for drawx in range(x - self.sector_size//2, x + self.sector_size//2):
            for drawy in range(y - self.sector_size//2, y + self.sector_size//2):
                if (drawx, drawy) in self.system_dict:
                    new_area.add_entity(self.system_dict[(drawx, drawy)].generate_star_entity())
        return new_area
    
    def generate_new_sector(self, x, y):
        self.explored_dict[self.galaxy_generator.generate_sector(self, x, y)] = True