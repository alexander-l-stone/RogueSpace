import math
from source.stellar_objects.planet import Planet
from source.stellar_objects.moon import Moon
from source.helper_functions.colliders import stop_collision
from source.stellar_objects.ring import Ring
from source.stellar_objects.belt import Belt
from source.system.system import System
from source.stellar_objects.cloud import Cloud
from random import seed, randint, random
from grammar.grammar import read_grammar

#TODO: Turn a lot of this into reading out of a grammar
class GalaxyGenerator:
    def __init__(self):
        self.generator_queue = []
        self.angleplusminus = 50
        self.system_scalar = 3
        self.planet_generation_function_dict = {
            'mercurial': self.generate_mercurial,
            'venusian': self.generate_venusian,
            'hot_belt': self.generate_hot_belt,
            'temperate': self.generate_temperate,
            'jungle': self.generate_jungle,
            'ocean': self.generate_ocean,
            'arid': self.generate_arid,
            'primordial': self.generate_primordial,
            'ast_belt': self.generate_ast_belt,
            'gas': self.generate_gas,
            'frozen': self.generate_frozen,
            'liquid': self.generate_liquid,
            'frozen_belt': self.generate_frozen_belt,
            'martian': self.generate_martian,
        }
        self.grammar = read_grammar("resources/grammars/system_grammar.json")
    
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
        #TODO: figure out if this needs to be fixed when wormholes allow a sector to be generated not adjacent to an explored area. Suspect no
        rounded_x = int(x/galaxy.sector_size)
        if (x < 0):
            rounded_x = rounded_x - 1
        adjusted_x = rounded_x * galaxy.sector_size
        rounded_y = int(y/galaxy.sector_size)
        if (y < 0):
            rounded_y = rounded_y - 1
        adjusted_y = rounded_y * galaxy.sector_size
        num_clusters = randint(0, galaxy.sector_size//25)
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
        num_system_to_generate = randint(1, max(2,cluster_area//120))
        for i in range(0, num_system_to_generate):
            randtheta = randint(0,360)*math.pi/180
            randradius = randint(0, radius)
            randx = int(randradius*math.cos(randtheta)) + x
            randy = int(randradius*math.sin(randtheta)) + y
            if ((randx, randy not in galaxy.system_dict)):
                galaxy.system_dict[(randx, randy)] = self.generate_solar_system(randx, randy)

    def generate_solar_system(self, x, y):

        gal_str = self.grammar.generate()

        part = gal_str.split(' ')
        i = 0
        # star data
        star_type = part[i]
        i += 1
        character = chr(int(part[i], 0))
        i += 1
        hyperlimit = randint(int(part[i]), int(part[i+1]))
        i += 2
        color = (randint(int(part[i]), int(part[i+1])), randint(int(part[i+2]), int(part[i+3])), randint(int(part[i+4]), int(part[i+5])))
        i += 6

        # zones
        hot_zone = randint(0, int(part[i]))
        i += 1
        bio_zone = randint(hot_zone, hot_zone + int(part[i]))
        i += 1
        cold_zone = randint(bio_zone, bio_zone + int(part[i]))
        i += 1
        gas_zone = randint(cold_zone, cold_zone + int(part[i]))
        i += 1
        frozen_zone = randint(gas_zone, gas_zone + int(part[i]))

        return System(x, y, character, color, f"{star_type}: {x}, {y}", star_type, hyperlimit * self.system_scalar, hot_zone, bio_zone, cold_zone, gas_zone, frozen_zone)
    
    def generate_planets(self, system):
        if system.system_type == ("giant-red" or "giant-blue"):
            return False
        num_planets = randint(2, 10)
        p1 = 8 + randint(1, 8)
        p2 = p1 + 2 + randint(1, 5)
        current_angle = 0
        planet_array = []
        for i in range(1, num_planets + 1):
            current_angle = current_angle + 120
            if i == 1:
                planet_radius = p1 * self.system_scalar
            elif i == 2:
                planet_radius = p2 * self.system_scalar
            else:
                planet_radius = self.titus_bode(p1, p2, i) * self.system_scalar
            if planet_radius < (system.hot_zone * self.system_scalar):
                planet = self.grammar.generate('planet<hot>')
            elif planet_radius < (system.bio_zone * self.system_scalar):
                planet = self.grammar.generate('planet<bio>')
            elif planet_radius < (system.cold_zone * self.system_scalar):
                planet = self.grammar.generate('planet<cold>')
            elif planet_radius < (system.gas_zone * self.system_scalar):
                planet = self.grammar.generate('planet<gas>')
            elif planet_radius < (system.frozen_zone * self.system_scalar):
                planet = self.grammar.generate('planet<frozen>')
            else:
                planet = 'frozen_belt'
            planet_array.append({'radius': planet_radius, 'angle': current_angle, 'planet': planet})
        for planet in planet_array:
            system.add_planet(self.planet_generation_function_dict[planet['planet']](system, planet['radius'], planet['angle']))

        if len(system.planet_list) > 0:
            try:
                system.hyperlimit += int((system.planet_list[-1].x**2 + system.planet_list[-1].y**2)**(1/2))
            except AttributeError:
                system.hyperlimit += system.planet_list[-1].radius
        #Make Clouds
        num_clouds = randint(int(math.pi*system.hyperlimit**2)//1200, int(math.pi*system.hyperlimit**2)//800)
        for i in range(num_clouds):
            randradius = randint(11, system.hyperlimit)
            xy = self.get_random_point_on_circle(randradius)
            cloudradius = randint(1, 6)
            overlap = False
            for planet in system.planet_list:
                planet_datatype = type(planet)
                if not planet_datatype is Ring and not planet_datatype is Belt:
                    if abs(planet.x - xy['x'])**2 + abs(planet.y - xy['y'])**2 <= (planet.radius + cloudradius)**2:
                        overlap = True
            for entity in system.entity_list:
                if type(entity) is Cloud:
                    if abs(entity.x - xy['x'])**2 + abs(entity.y - xy['y'])**2 <= (entity.radius + cloudradius)**2:
                        overlap = True
            if not overlap:
                d15 = randint(1, 15)
                if d15 < 4:
                    system.entity_list.append(Cloud(xy['x'], xy['y'], ' ', (128, 0, 128), cloudradius, randint(0, cloudradius + abs(xy['x']) + abs(xy['y'])), 'purple-gas', thin_color=(88, 0, 88)))
                elif d15 < 7:
                    system.entity_list.append(Cloud(xy['x'], xy['y'], ' ', (0, 150, 0), cloudradius, randint(0, cloudradius + abs(xy['x']) + abs(xy['y'])), 'green-gas', thin_color=(0, 100, 0)))
                elif d15 < 9:
                    system.entity_list.append(Cloud(xy['x'], xy['y'], ' ', (0, 150, 150), cloudradius, randint(0, cloudradius + abs(xy['x']) + abs(xy['y'])), 'cyan-gas', thin_color=(0, 100, 100)))
                elif d15 < 12:
                    system.entity_list.append(Cloud(xy['x'], xy['y'], ' ', (150, 0, 0), cloudradius, randint(0, cloudradius + abs(xy['x']) + abs(xy['y'])), 'red-gas', thin_color=(60, 0, 0)))
                else:
                    system.entity_list.append(Cloud(xy['x'], xy['y'], ' ', (160, 99, 0), cloudradius, randint(0, cloudradius + abs(xy['x']) + abs(xy['y'])), 'gold-dust', thin_color=(80, 45, 0)))
        return True
    
    def generate_mercurial(self, system, orbital_radius, current_angle):
        xy = self.get_random_point_within_angle(orbital_radius, current_angle - self.angleplusminus, current_angle + self.angleplusminus)
        return Planet(xy['x'], xy['y'], 'o', (randint(120,180),randint(120,180),randint(120,180)), f"Mercurial {orbital_radius}", "mercurial", system, randint(5,8))

    def generate_venusian(self, system, orbital_radius, current_angle):
        xy = self.get_random_point_within_angle(orbital_radius, current_angle - self.angleplusminus, current_angle + self.angleplusminus)
        new_planet = Planet(xy['x'], xy['y'], 'o', (randint(125, 175),randint(190,220),randint(40,60)), f"Venusian {orbital_radius}", "venusian", system, randint(5,10))
        num_moons = randint(-5, 2)
        prev_radius = 2
        if num_moons > 0:
            for i in range(0, num_moons):
                new_moon_radius = randint(prev_radius+1, prev_radius+4)
                prev_radius = new_moon_radius
                self.generate_hot_zone_moons(new_planet, new_moon_radius)
        return new_planet

    def generate_hot_belt(self, system, orbital_radius, current_angle):
        return Belt(orbital_radius, '*', 3, (randint(210, 230), randint(170, 190), randint(130, 140)), randint(0, orbital_radius))

    def generate_hot_zone_moons(self, planet:Planet, radius:int):
        xy = self.get_random_point_on_circle(radius)
        planet.planetary_radius = radius + randint(3,5)
        planet.moons.append(Moon(xy['x'], xy['y'], 'o', (randint(150, 200), randint(150, 200), randint(150, 200)), 'hot', f"{planet.name} {radius}", planet, flags={'on_collide': stop_collision}))

    def generate_temperate(self, system, orbital_radius, current_angle):
        xy = self.get_random_point_within_angle(orbital_radius, current_angle - self.angleplusminus, current_angle + self.angleplusminus)
        new_planet = Planet(xy['x'], xy['y'], 'o', (randint(20, 60),randint(100,200),randint(20, 150)), f"Temperate {orbital_radius}", "temperate", system, randint(5,10))
        num_moons = randint(-1, 2)
        prev_radius = 2
        if num_moons > 0:
            for i in range(0, num_moons):
                new_moon_radius = randint(prev_radius+1, prev_radius+4)
                prev_radius = new_moon_radius
                self.generate_bio_zone_moons(new_planet, new_moon_radius)
        return new_planet
    
    def generate_ocean(self, system, orbital_radius, current_angle):
        xy = self.get_random_point_within_angle(orbital_radius, current_angle - self.angleplusminus, current_angle + self.angleplusminus)
        new_planet = Planet(xy['x'], xy['y'], 'o', (randint(0, 10),randint(0, 40),randint(150, 255)), f"Ocean {orbital_radius}", "ocean", system, randint(5,10))
        num_moons = randint(-1, 2)
        prev_radius = 2
        if num_moons > 0:
            for i in range(0, num_moons):
                new_moon_radius = randint(prev_radius+1, prev_radius+4)
                prev_radius = new_moon_radius
                self.generate_bio_zone_moons(new_planet, new_moon_radius)
        return new_planet

    def generate_jungle(self, system, orbital_radius, current_angle):
        xy = self.get_random_point_within_angle(orbital_radius, current_angle - self.angleplusminus, current_angle + self.angleplusminus)
        new_planet = Planet(xy['x'], xy['y'], 'o', (randint(20, 60),randint(200,250),randint(20, 60)), f"Jungle {orbital_radius}", "jungle", system, randint(5,10))
        num_moons = randint(-1, 2)
        prev_radius = 2
        if num_moons > 0:
            for i in range(0, num_moons):
                new_moon_radius = randint(prev_radius+1, prev_radius+4)
                prev_radius = new_moon_radius
                self.generate_bio_zone_moons(new_planet, new_moon_radius)
        return new_planet

    def generate_arid(self, system, orbital_radius, current_angle):
        xy = self.get_random_point_within_angle(orbital_radius, current_angle - self.angleplusminus, current_angle + self.angleplusminus)
        new_planet = Planet(xy['x'], xy['y'], 'o', (randint(170, 180),randint(160, 170),randint(130, 140)), f"Arid {orbital_radius}", "arid", system, randint(5,10))
        num_moons = randint(-1, 2)
        prev_radius = 2
        if num_moons > 0:
            for i in range(0, num_moons):
                new_moon_radius = randint(prev_radius+1, prev_radius+4)
                prev_radius = new_moon_radius
                self.generate_bio_zone_moons(new_planet, new_moon_radius)
        return new_planet
    
    def generate_primordial(self, system, orbital_radius, current_angle):
        xy = self.get_random_point_within_angle(orbital_radius, current_angle - self.angleplusminus, current_angle + self.angleplusminus)
        new_planet = Planet(xy['x'], xy['y'], 'o', (randint(220, 255),randint(140,180),0), f"Primordial {orbital_radius}", "primordial", system, randint(5,10))
        num_moons = randint(-1, 2)
        prev_radius = 2
        if num_moons > 0:
            for i in range(0, num_moons):
                new_moon_radius = randint(prev_radius+1, prev_radius+4)
                prev_radius = new_moon_radius
                self.generate_bio_zone_moons(new_planet, new_moon_radius)
        return new_planet
    
    def generate_ast_belt(self, system, orbital_radius, current_angle):
        return Belt(orbital_radius, '*', 5, (randint(80, 120), randint(80, 100), randint(80, 90)), randint(0, orbital_radius))

    def generate_bio_zone_moons(self, planet:Planet, radius:int):
        xy = self.get_random_point_on_circle(radius)
        planet.planetary_radius = radius + randint(3,5)
        d10 = randint(1, 10)
        if d10 <= 2:
            planet.moons.append(Moon(xy['x'], xy['y'], 'o', (0, randint(50, 255), randint(50, 255)), 'terran', f"{planet.name} {radius}", planet, flags={'on_collide': stop_collision}))
        elif d10 <= 5:
            planet.moons.append(Moon(xy['x'], xy['y'], 'o', (randint(80, 90),randint(80, 90),randint(80, 90)), 'barren', f"{planet.name} {radius}", planet, flags={'on_collide': stop_collision}))
        else:
            planet.moons.append(Moon(xy['x'], xy['y'], '*', (randint(80, 120), randint(80, 100), randint(80, 90)), 'asteroid', f"{planet.name} {radius}", planet, flags={'on_collide': stop_collision}))

    def generate_martian(self, system, orbital_radius, current_angle):
        xy = self.get_random_point_within_angle(orbital_radius, current_angle - self.angleplusminus, current_angle + self.angleplusminus)
        new_planet = Planet(xy['x'], xy['y'], 'o', (randint(170,190),randint(35,45),randint(45,55)), f"Martian {orbital_radius}", "martian", system, randint(5,8))
        num_moons = randint(-2, 3)
        prev_radius = 2
        if num_moons > 0:
            for i in range(0, num_moons):
                new_moon_radius = randint(prev_radius+1, prev_radius+4)
                prev_radius = new_moon_radius
                self.generate_bio_zone_moons(new_planet, new_moon_radius)
        return new_planet

    def generate_cold_zone_moons(self, planet:Planet, radius:int):
        #TODO: Add more cold zone moon types
        xy = self.get_random_point_on_circle(radius)
        planet.planetary_radius = radius + randint(3,5)
        d10 = randint(1, 10)
        if d10 <= 5:
            planet.moons.append(Moon(xy['x'], xy['y'], 'o', (randint(80, 90),randint(80, 90),randint(80, 90)), 'barren', f"{planet.name} {radius}", planet, flags={'on_collide': stop_collision}))
        else:
            planet.moons.append(Moon(xy['x'], xy['y'], '*', (randint(80, 120), randint(80, 100), randint(80, 90)), 'asteroid', f"{planet.name} {radius}", planet, flags={'on_collide': stop_collision}))

    def generate_gas(self, system, orbital_radius, current_angle):
        xy = self.get_random_point_within_angle(orbital_radius, current_angle - self.angleplusminus, current_angle + self.angleplusminus)
        new_planet = Planet(xy['x'], xy['y'], 'O', (randint(100, 255),randint(50, 150),randint(0, 100)), f"Gas {orbital_radius}", "gas", system, randint(10,15))
        num_moons = randint(0, 5)
        prev_radius = 4
        if num_moons > 0:
            for i in range(0, num_moons):
                new_moon_radius = randint(prev_radius+1, prev_radius+3)
                prev_radius = new_moon_radius
                self.generate_gas_zone_moons(new_planet, new_moon_radius)
        return new_planet

    def generate_gas_zone_moons(self, planet:Planet, radius:int):
        #TODO: Add more gas zone moon types
        #TODO: Figure out a way to put the asteroids on the outside maybe ???
        xy = self.get_random_point_on_circle(radius)
        planet.planetary_radius = radius + randint(5,10)
        if len(planet.moons) == 0 and len(planet.entity_list) == 0:
            d10 = randint(1, 10)
            if d10 < 8:
                planet.entity_list.append(Ring(radius, '*', (randint(80, 120), randint(80, 100), randint(80, 90))))
                return
        d10 = randint(1, 10)
        if d10 <= 1:
            planet.moons.append(Moon(xy['x'], xy['y'], 'o', (randint(80, 90),randint(80, 90),randint(80, 90)), 'barren', f"{planet.name} {radius}", planet, flags={'on_collide': stop_collision}))
        elif d10 <= 4:
            planet.moons.append(Moon(xy['x'], xy['y'], '*', (randint(80, 120), randint(80, 100), randint(80, 90)), 'asteroid', f"{planet.name} {radius}", planet, flags={'on_collide': stop_collision}))
        elif d10 <= 7:
            planet.moons.append(Moon(xy['x'], xy['y'], 'o', (randint(230, 255), randint(200, 210), 0), 'methane', f"{planet.name} {radius}", planet, flags={'on_collide': stop_collision}))
        elif d10 <= 9:
            planet.moons.append(Moon(xy['x'], xy['y'], 'o', (randint(230, 255), randint(230, 255), randint(120, 170)), 'volcanic', f"{planet.name} {radius}", planet, flags={'on_collide': stop_collision}))

    def generate_frozen(self, system, orbital_radius, current_angle):
        xy = self.get_random_point_within_angle(orbital_radius, current_angle - self.angleplusminus, current_angle + self.angleplusminus)
        new_planet = Planet(xy['x'], xy['y'], 'o', (randint(150, 170), randint(230, 255), randint(230, 255)), f"Frozen {orbital_radius}", "frozen", system, randint(2,3))
        num_moons = randint(-4, 1)
        prev_radius = 2
        if num_moons > 0:
            for i in range(0, num_moons):
                new_moon_radius = randint(prev_radius+1, prev_radius+4)
                prev_radius = new_moon_radius
                self.generate_frozen_zone_moons(new_planet, new_moon_radius)
        return new_planet
    
    def generate_liquid(self, system, orbital_radius, current_angle):
        xy = self.get_random_point_within_angle(orbital_radius, current_angle - self.angleplusminus, current_angle + self.angleplusminus)
        new_planet = Planet(xy['x'], xy['y'], 'O', (0,randint(50, 255),randint(150, 255)), f"Liquid {orbital_radius}", "liquid", system, randint(10,15))
        num_moons = randint(0, 8)
        prev_radius = 3
        if num_moons > 0:
            for i in range(0, num_moons):
                new_moon_radius = randint(prev_radius+1, prev_radius+4)
                prev_radius = new_moon_radius
                self.generate_frozen_zone_moons(new_planet, new_moon_radius)
        return new_planet
    
    def generate_frozen_belt(self, system, orbital_radius, current_angle):
        return Belt(orbital_radius, '*', 3, (randint(150, 170), randint(230, 255), randint(230, 255)), randint(0, orbital_radius))

    def generate_frozen_zone_moons(self, planet:Planet, radius:int):
        #TODO: Add more frozen zone moon types
        xy = self.get_random_point_on_circle(radius)
        planet.planetary_radius = radius + randint(4,8)
        d10 = randint(1, 10)
        if len(planet.moons) == 0 and len(planet.entity_list) == 0:
            d10 = randint(1, 10)
            if d10 < 8:
                planet.entity_list.append(Ring(radius, '*', (randint(150, 170), randint(230, 255), randint(230, 255))))
                return
        if d10 <= 7:
            planet.moons.append(Moon(xy['x'], xy['y'], 'o', (randint(150, 170), randint(230, 255), randint(230, 255)), 'frozen', f"{planet.name} {radius}", planet, flags={'on_collide': stop_collision}))
        else:
            planet.moons.append(Moon(xy['x'], xy['y'], '*', (randint(150, 170), randint(230, 255), randint(230, 255)), 'frozen-asteroid', f"{planet.name} {radius}", planet, flags={'on_collide': stop_collision}))

    def generate_oort_cloud_planet(self, system:System, orbital_radius:int, current_angle:int):
        system.add_planet(self.generate_frozen_belt(system, orbital_radius, current_angle))

    def get_random_point_on_circle(self, radius):
        randTheta = randint(0, 360) * math.pi/180
        return {'x': int(radius * math.cos(randTheta)), 'y': int(radius * math.sin(randTheta))}
    
    def get_random_point_within_angle(self, radius, min_angle, max_angle):
        randTheta = randint(min_angle, max_angle) * math.pi/180
        return {'x': int(radius * math.cos(randTheta)), 'y': int(radius * math.sin(randTheta))}

    def titus_bode(self, a, b, n):
        return int(a + ((b - a) * 2 * (n-2)))