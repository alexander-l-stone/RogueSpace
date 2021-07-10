import math
from source.system.system import System
from random import seed, randint

class GalaxyGenerator:
    def __init__(self):
        self.generator_queue = []
    
    #TODO: Remove generator queue
    def resolve_generator_queue(self, galaxy):
        """This function should never be called
        """
        for item in self.generator_queue:
            if item['type'] == 'solar_system':
                if ((item['x'], item['y']) not in galaxy.system_dict):
                    galaxy.system_dict[(item['x'], item['y'])] = self.generate_solar_system(item['x'], item['y'])
            if item['type'] == 'cluster':
                self.generate_cluster(item['x'], item['y'], item['radius'])

    def generate_sector(self, galaxy, x, y):
        """Generate a sector from the new coordinates x and y. These coordinates will be rounded and modded by the galaxies sector size to
        find the nearest unexplored x, y corner. This coordinate pair will always be adjacent to an explored sector. Sector counting starts at 0,0 and
        goes up/down by the galaxies sector_size.

        Args:
            galaxy (Galaxy): A galaxy object that contains the exploration dict and system dict.
            x (int): an integer. Either this or y(or both) must adjacent to an explored sector.
            y (int): an integer. Either this or x(or both) must adjacent to an explored sector.
        """
        #TODO: figure out if this needs to be fixed when wormholes allow a sector to be generated not adjacent to an explored area
        rounded_x = int(x/galaxy.sector_size)
        if (x < 0):
            rounded_x = rounded_x - 1
        rounded_x = rounded_x * galaxy.sector_size
        rounded_y = int(y/galaxy.sector_size)
        if (y < 0):
            rounded_y = rounded_y - 1
        rounded_y = rounded_y * galaxy.sector_size
        num_clusters = randint(0, galaxy.sector_size//5)
        num_additional_systems = randint(0, galaxy.sector_size//25)
        for cluster in range(0, num_clusters):
            cluster_radius = randint(3, 20)
            cluster_x = randint(rounded_x + cluster_radius + 1, rounded_x + galaxy.sector_size - cluster_radius - 1)
            cluster_y = randint(rounded_y + cluster_radius + 1, rounded_y + galaxy.sector_size - cluster_radius - 1)
            self.generate_cluster(galaxy, cluster_x, cluster_y, cluster_radius)
        for system in range(0, num_additional_systems):
            system_x = randint(rounded_x, rounded_x + galaxy.sector_size)
            system_y = randint(rounded_y, rounded_y + galaxy.sector_size)
            galaxy.system_dict[(system_x, system_y)] = self.generate_solar_system(system_x, system_y)

    def generate_cluster(self, galaxy, x, y, radius):
        cluster_area = int(math.pi*radius**2)
        num_system_to_generate = randint(1, cluster_area//4)
        for i in range(0, num_system_to_generate):
            randx = randint(x - radius, x + radius)
            randy = randint(y - radius, y + radius)
            galaxy.system_dict[(randx, randy)] = self.generate_solar_system(randx, randy)

    def generate_solar_system(self, x, y):
        return System(x, y, 'O', (0, 0, 255), f"Placeholder: {x}, {y}", "placeholder", 10)