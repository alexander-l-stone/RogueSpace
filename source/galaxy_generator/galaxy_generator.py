import math
from source.planet.planet import Planet
from source.ring.ring import Ring
from source.system.system import System
from random import seed, randint, random

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
        adjusted_x = rounded_x * galaxy.sector_size
        rounded_y = int(y/galaxy.sector_size)
        if (y < 0):
            rounded_y = rounded_y - 1
        adjusted_y = rounded_y * galaxy.sector_size
        num_clusters = randint(0, galaxy.sector_size//50)
        num_additional_systems = randint(0, galaxy.sector_size)
        for cluster in range(0, num_clusters):
            cluster_radius = randint(3, galaxy.sector_size//14)
            cluster_x = randint(adjusted_x + cluster_radius + 1, adjusted_x + galaxy.sector_size - cluster_radius - 1)
            cluster_y = randint(adjusted_y + cluster_radius + 1, adjusted_y + galaxy.sector_size - cluster_radius - 1)
            self.generate_cluster(galaxy, cluster_x, cluster_y, cluster_radius)
        for system in range(0, num_additional_systems):
            system_x = randint(adjusted_x, adjusted_x + galaxy.sector_size)
            system_y = randint(adjusted_y, adjusted_y + galaxy.sector_size)
            if ((system_x, system_y not in galaxy.system_dict)):
                galaxy.system_dict[(system_x, system_y)] = self.generate_solar_system(system_x, system_y)
        return (rounded_x, rounded_y)

    def generate_cluster(self, galaxy, x, y, radius):
        cluster_area = int(math.pi*radius**2)
        num_system_to_generate = randint(1, max(2,cluster_area//20))
        for i in range(0, num_system_to_generate):
            randtheta = randint(0,360)*math.pi/180
            randradius = randint(0, radius)
            randx = int(randradius*math.cos(randtheta)) + x
            randy = int(randradius*math.sin(randtheta)) + y
            if ((randx, randy not in galaxy.system_dict)):
                galaxy.system_dict[(randx, randy)] = self.generate_solar_system(randx, randy)

    def generate_solar_system(self, x, y):
        dieroll = randint(0, 100)
        if dieroll < 60:
            #normal(white, yellow, orange, red)
            d4 = randint(1, 4)
            if d4 == 1:
                #white
                character = 'O'
                color = (randint(200, 255), randint(200, 255), randint(150, 200))
                star_type = "normal-white"
                hyperlimit = randint(90, 120)
            elif d4 == 2:
                #yellow
                character = 'O'
                color = (randint(200, 255), randint(200, 255), 0)
                star_type = "normal-yellow"
                hyperlimit = randint(90, 120)
            elif d4 == 3:
                #orange
                character = 'O'
                color = (randint(200, 255), randint(120, 165), 0)
                star_type = "normal-orange"
                hyperlimit = randint(90, 120)
            elif d4 == 4:
                #red
                character = 'O'
                color = (randint(130, 190), 0, 0)
                star_type = "normal-red"
                hyperlimit = randint(90, 120)
        elif dieroll < 80:
            #dwarf
            d6 = randint(1, 6)
            if d6 == 6:
                #white
                character = 'o'
                color = (randint(200, 255), randint(200, 255), randint(150, 200))
                star_type = "dwarf-white"
                hyperlimit = randint(60, 90)
            else:
                #red
                character = 'o'
                color = (randint(130, 190), 0, 0)
                star_type = "dwarf-red"
                hyperlimit = randint(60, 90)
        elif dieroll < 99:
            #supergiant
            d2 = randint(1, 2)
            if d2 == 1:
                #red
                character = 'O'
                color = (randint(200, 255), 0, 0)
                star_type = "giant-red"
                hyperlimit = randint(180, 250)
            else:
                #blue
                character = 'O'
                color = (0, 0, randint(200, 255))
                star_type = "giant-blue"
                hyperlimit = randint(180, 250)
        else:
            #anomaly(for now brown dwarf)
            character = 'o'
            color = (randint(120,145), randint(60, 70), randint(12, 18))
            star_type = "dwarf-brown"
            hyperlimit = randint(15, 25)
        return System(x, y, character, color, f"{star_type}: {x}, {y}", star_type, hyperlimit)
    
    def generate_planets(self, system):
        
        system.add_planet(Planet(3, 3, 'o', (0, 255, 0), 'test', 'placeholder', system, 5))
    
    def titus_bode(self, a, b, n):
        return int(a + ((b - a) * 2 * (n-2)))