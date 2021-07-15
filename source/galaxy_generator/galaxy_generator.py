import math
from source.planet.planet import Planet
from source.planet.moon import Moon
from source.helper_functions.colliders import stop_collision
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
        dieroll = randint(1, 100)
        if dieroll < 60:
            #normal(white, yellow, orange, red)
            d4 = randint(1, 4)
            if d4 == 1:
                #white
                character = 'O'
                color = (randint(200, 255), randint(200, 255), randint(150, 200))
                star_type = "normal-white"
                hyperlimit = randint(10, 20)
            elif d4 == 2:
                #yellow
                character = 'O'
                color = (randint(200, 255), randint(200, 255), 0)
                star_type = "normal-yellow"
                hyperlimit = randint(10, 20)
            elif d4 == 3:
                #orange
                character = 'O'
                color = (randint(200, 255), randint(120, 165), 0)
                star_type = "normal-orange"
                hyperlimit = randint(10, 20)
            elif d4 == 4:
                #red
                character = 'O'
                color = (randint(130, 190), 0, 0)
                star_type = "normal-red"
                hyperlimit = randint(10, 20)
        elif dieroll < 80:
            #dwarf
            d6 = randint(1, 6)
            if d6 == 6:
                #white
                character = chr(7)
                color = (randint(200, 255), randint(200, 255), randint(150, 200))
                star_type = "dwarf-white"
                hyperlimit = randint(5, 15)
            else:
                #red
                character = chr(7)
                color = (randint(130, 190), 0, 0)
                star_type = "dwarf-red"
                hyperlimit = randint(5, 15)
        elif dieroll < 99:
            #supergiant
            d2 = randint(1, 2)
            if d2 == 1:
                #red
                character = 'O'
                color = (randint(200, 255), 0, 0)
                star_type = "giant-red"
                hyperlimit = randint(50, 70)
            else:
                #blue
                character = 'O'
                color = (0, 0, randint(200, 255))
                star_type = "giant-blue"
                hyperlimit = randint(5, 70)
        else:
            #anomaly(for now brown dwarf)
            character = chr(7)
            color = (randint(120,145), randint(60, 70), randint(12, 18))
            star_type = "dwarf-brown"
            hyperlimit = randint(3, 8)
        return System(x, y, character, color, f"{star_type}: {x}, {y}", star_type, hyperlimit)
    
    def generate_planets(self, system):
        #TODO: Differentiate this by colors
        hot_zone = 0
        bio_zone = 0
        cold_zone = 0
        gas_zone = 0
        frozen_zone = 0
        if system.system_type == ("giant-red" or "giant-blue"):
            return False
        elif (system.system_type == "normal-red") or (system.system_type == "normal-yellow") or (system.system_type == "normal-white") or (system.system_type == "normal-orange"):
            hot_zone = randint(1, 8)
            bio_zone = randint(hot_zone+1, hot_zone+15)
            cold_zone = randint(bio_zone+1, bio_zone+20)
            gas_zone = randint(cold_zone+1, cold_zone+50)
            frozen_zone = randint(gas_zone, gas_zone+100)
        elif system.system_type == ("dwarf-red"):
            hot_zone = randint(1, 3)
            bio_zone = randint(hot_zone+1, hot_zone+7)
            cold_zone = randint(bio_zone+1, bio_zone+10)
            gas_zone = randint(cold_zone+1, cold_zone+20)
            frozen_zone = randint(gas_zone, gas_zone+40)
        elif system.system_type == ("dwarf-white"):
            hot_zone = randint(1, 12)
            bio_zone = randint(hot_zone+1, hot_zone+8)
            cold_zone = randint(bio_zone+1, bio_zone+10)
            gas_zone = randint(cold_zone+1, cold_zone+10)
            frozen_zone = randint(gas_zone, gas_zone+20)
        elif system.system_type == ("dwarf-brown"):
            cold_zone = randint(1, 3)
            gas_zone = randint(cold_zone + 1, cold_zone + 5)
            frozen_zone = randint(gas_zone + 1, gas_zone + 5)
        num_planets = randint(2, 14)
        p1 = randint(3, 10)
        p2 = randint(p1+3, p1+7)
        for i in range(1,num_planets):
            if i == 1:
                planet_radius = p1
            elif i == 2:
                planet_radius = p2
            else:
                planet_radius = self.titus_bode(p1, p2, i)
            if (planet_radius <= hot_zone):
                self.generate_hot_zone_planet(system, planet_radius)
            elif (planet_radius <= bio_zone):
                self.generate_bio_zone_planet(system, planet_radius)
            elif (planet_radius <= cold_zone):
                self.generate_cold_zone_planet(system, planet_radius)
            elif (planet_radius <= gas_zone):
                self.generate_gas_zone_planet(system, planet_radius)
            elif (planet_radius <= frozen_zone):
                self.generate_frozen_zone_planet(system, planet_radius)
            else:
                self.generate_oort_cloud_planet(system, planet_radius)
        if len(system.planet_list) > 0:
            try:
                system.hyperlimit += int((system.planet_list[-1].x**2 + system.planet_list[-1].y**2)**(1/2))
            except AttributeError:
                system.hyperlimit += system.planet_list[-1].radius
        return True
    
    #TODO: add big asteroids as planets inside the belt
    def generate_hot_zone_planet(self, system:System, orbital_radius:int):
        d100 = randint(1, 100)
        xy = self.get_random_point_on_circle(orbital_radius)
        if d100 <= 40:
            #mercury type
            new_planet = Planet(xy['x'], xy['y'], 'o', (randint(120,180),randint(120,180),randint(120,180)), f"Mercurial {orbital_radius}", "mercurial", system, randint(5,8))
        elif d100 <= 60:
            #venus type
            new_planet = Planet(xy['x'], xy['y'], 'o', (randint(125, 175),randint(190,220),randint(40,60)), f"Venusian {orbital_radius}", "venusian", system, randint(5,10))
            num_moons = randint(-5, 2)
            prev_radius = 0
            if num_moons > 0:
                for i in range(0, num_moons):
                    new_moon_radius = randint(prev_radius+1, prev_radius+4)
                    prev_radius = new_moon_radius
                    self.generate_hot_zone_moons(new_planet, new_moon_radius)
        else:
            new_planet = Ring(orbital_radius, '*', (randint(210, 230), randint(170, 190), randint(130, 140)))
        system.add_planet(new_planet)

    def generate_hot_zone_moons(self, planet:Planet, radius:int):
        xy = self.get_random_point_on_circle(radius)
        planet.planetary_radius = radius + randint(3,5)
        planet.moons.append(Moon(xy['x'], xy['y'], 'o', (randint(150, 200), randint(150, 200), randint(150, 200)), 'hot', f"{planet.name} {radius}", planet, flags={'on_collide': stop_collision}))

    def generate_bio_zone_planet(self, system:System, orbital_radius:int):
        d100 = randint(1, 100)
        xy = self.get_random_point_on_circle(orbital_radius)
        if d100 <= 40:
            #temperate type
            new_planet = Planet(xy['x'], xy['y'], 'o', (randint(20, 60),randint(100,200),randint(20, 150)), f"Temperate {orbital_radius}", "temperate", system, randint(5,10))
            num_moons = randint(-1, 2)
            prev_radius = 0
            if num_moons > 0:
                for i in range(0, num_moons):
                    new_moon_radius = randint(prev_radius+1, prev_radius+4)
                    prev_radius = new_moon_radius
                    self.generate_bio_zone_moons(new_planet, new_moon_radius)
        elif d100 <= 50:
            #ocean type
            new_planet = Planet(xy['x'], xy['y'], 'o', (randint(0, 10),randint(0, 40),randint(150, 255)), f"Ocean {orbital_radius}", "ocean", system, randint(5,10))
            num_moons = randint(-1, 2)
            prev_radius = 0
            if num_moons > 0:
                for i in range(0, num_moons):
                    new_moon_radius = randint(prev_radius+1, prev_radius+4)
                    prev_radius = new_moon_radius
                    self.generate_bio_zone_moons(new_planet, new_moon_radius)
        elif d100 <= 60:
            #jungle type
            new_planet = Planet(xy['x'], xy['y'], 'o', (randint(20, 60),randint(200,250),randint(20, 60)), f"Jungle {orbital_radius}", "jungle", system, randint(5,10))
            num_moons = randint(-1, 2)
            prev_radius = 0
            if num_moons > 0:
                for i in range(0, num_moons):
                    new_moon_radius = randint(prev_radius+1, prev_radius+4)
                    prev_radius = new_moon_radius
                    self.generate_bio_zone_moons(new_planet, new_moon_radius)
        elif d100 <= 70:
            #arid type
            new_planet = Planet(xy['x'], xy['y'], 'o', (randint(170, 180),randint(160, 170),randint(130, 140)), f"Arid {orbital_radius}", "arid", system, randint(5,10))
            num_moons = randint(-1, 2)
            prev_radius = 0
            if num_moons > 0:
                for i in range(0, num_moons):
                    new_moon_radius = randint(prev_radius+1, prev_radius+4)
                    prev_radius = new_moon_radius
                    self.generate_bio_zone_moons(new_planet, new_moon_radius)
        elif d100 <= 75:
            #primordial type
            new_planet = Planet(xy['x'], xy['y'], 'o', (randint(220, 255),randint(140,180),0), f"Primordial {orbital_radius}", "primordial", system, randint(5,10))
            num_moons = randint(-1, 2)
            prev_radius = 0
            if num_moons > 0:
                for i in range(0, num_moons):
                    new_moon_radius = randint(prev_radius+1, prev_radius+4)
                    prev_radius = new_moon_radius
                    self.generate_bio_zone_moons(new_planet, new_moon_radius)
        else:
            new_planet = Ring(orbital_radius, '*', (randint(80, 120), randint(80, 100), randint(80, 90)))
        system.add_planet(new_planet)

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

    def generate_cold_zone_planet(self, system:System, orbital_radius:int):
        #TODO: add more cold zone planet types
        d100 = randint(1, 100)
        xy = self.get_random_point_on_circle(orbital_radius)
        if d100 <= 80:
            new_planet = Planet(xy['x'], xy['y'], 'o', (randint(170,190),randint(35,45),randint(45,55)), f"Martian {orbital_radius}", "martian", system, randint(5,8))
            num_moons = randint(-2, 3)
            prev_radius = 0
            if num_moons > 0:
                for i in range(0, num_moons):
                    new_moon_radius = randint(prev_radius+1, prev_radius+4)
                    prev_radius = new_moon_radius
                    self.generate_bio_zone_moons(new_planet, new_moon_radius)
        else:
            new_planet = Ring(orbital_radius, '*', (randint(80, 120), randint(80, 100), randint(80, 90)))
        system.add_planet(new_planet)

    def generate_cold_zone_moons(self, planet:Planet, radius:int):
        #TODO: Add more cold zone moon types
        xy = self.get_random_point_on_circle(radius)
        planet.planetary_radius = radius + randint(3,5)
        d10 = randint(1, 10)
        if d10 <= 5:
            planet.moons.append(Moon(xy['x'], xy['y'], 'o', (randint(80, 90),randint(80, 90),randint(80, 90)), 'barren', f"{planet.name} {radius}", planet, flags={'on_collide': stop_collision}))
        else:
            planet.moons.append(Moon(xy['x'], xy['y'], '*', (randint(80, 120), randint(80, 100), randint(80, 90)), 'asteroid', f"{planet.name} {radius}", planet, flags={'on_collide': stop_collision}))

    def generate_gas_zone_planet(self, system:System, orbital_radius:int):
        d100 = randint(1, 100)
        xy = self.get_random_point_on_circle(orbital_radius)
        if d100 <= 10:
            new_planet = Planet(xy['x'], xy['y'], 'o', (randint(90,100),randint(90,100),randint(90,100)), f"Martian {orbital_radius}", "martian", system, randint(4,8))
            num_moons = randint(-2, 3)
            prev_radius = 0
            if num_moons > 0:
                for i in range(0, num_moons):
                    new_moon_radius = randint(prev_radius+1, prev_radius+4)
                    prev_radius = new_moon_radius
                    self.generate_cold_zone_moons(new_planet, new_moon_radius)
        elif d100 <= 80:
            new_planet = Planet(xy['x'], xy['y'], 'O', (randint(100, 255),randint(50, 150),randint(0, 100)), f"Gas {orbital_radius}", "gas", system, randint(10,15))
            num_moons = randint(0, 15)
            prev_radius = 0
            if num_moons > 0:
                for i in range(0, num_moons):
                    new_moon_radius = randint(prev_radius+1, prev_radius+4)
                    prev_radius = new_moon_radius
                    self.generate_gas_zone_moons(new_planet, new_moon_radius)
        else:
            new_planet = Ring(orbital_radius, '*', (randint(80, 120), randint(80, 100), randint(80, 90)))
        system.add_planet(new_planet)

    def generate_gas_zone_moons(self, planet:Planet, radius:int):
        #TODO: Add more gas zone moon types
        #TODO: Figure out a way to put the asteroids on the outside maybe ???
        xy = self.get_random_point_on_circle(radius)
        planet.planetary_radius = radius + randint(5,10)
        d10 = randint(1, 10)
        if d10 <= 1:
            planet.moons.append(Moon(xy['x'], xy['y'], 'o', (randint(80, 90),randint(80, 90),randint(80, 90)), 'barren', f"{planet.name} {radius}", planet, flags={'on_collide': stop_collision}))
        elif d10 <= 3:
            planet.moons.append(Moon(xy['x'], xy['y'], '*', (randint(80, 120), randint(80, 100), randint(80, 90)), 'asteroid', f"{planet.name} {radius}", planet, flags={'on_collide': stop_collision}))
        elif d10 <= 6:
            planet.moons.append(Moon(xy['x'], xy['y'], 'o', (randint(230, 255), randint(200, 210), 0), 'methane', f"{planet.name} {radius}", planet, flags={'on_collide': stop_collision}))
        elif d10 <= 7:
            planet.moons.append(Moon(xy['x'], xy['y'], 'o', (randint(230, 255), randint(230, 255), randint(120, 170)), 'volcanic', f"{planet.name} {radius}", planet, flags={'on_collide': stop_collision}))
        else:
            planet.entity_list.append(Ring(radius, '*', (randint(150, 170), randint(230, 255), randint(230, 255))))


    def generate_frozen_zone_planet(self, system:System, orbital_radius:int):
        d100 = randint(1, 100)
        xy = self.get_random_point_on_circle(orbital_radius)
        if d100 <= 10:
            new_planet = Planet(xy['x'], xy['y'], 'o', (randint(150, 170), randint(230, 255), randint(230, 255)), f"Frozen {orbital_radius}", "frozen", system, randint(2,3))
            num_moons = randint(-4, 1)
            prev_radius = 0
            if num_moons > 0:
                for i in range(0, num_moons):
                    new_moon_radius = randint(prev_radius+1, prev_radius+4)
                    prev_radius = new_moon_radius
                    self.generate_frozen_zone_moons(new_planet, new_moon_radius)
        elif d100 <= 80:
            new_planet = Planet(xy['x'], xy['y'], 'O', (0,randint(50, 255),randint(150, 255)), f"Liquid {orbital_radius}", "liquid", system, randint(10,15))
            num_moons = randint(0, 8)
            prev_radius = 0
            if num_moons > 0:
                for i in range(0, num_moons):
                    new_moon_radius = randint(prev_radius+1, prev_radius+4)
                    prev_radius = new_moon_radius
                    self.generate_frozen_zone_moons(new_planet, new_moon_radius)
        else:
            new_planet = Ring(orbital_radius, '*', (randint(150, 170), randint(230, 255), randint(230, 255)))
        system.add_planet(new_planet)

    def generate_frozen_zone_moons(self, planet:Planet, radius:int):
        #TODO: Add more frozen zone moon types
        xy = self.get_random_point_on_circle(radius)
        planet.planetary_radius = radius + randint(4,8)
        d10 = randint(1, 10)
        if d10 <= 4:
            planet.moons.append(Moon(xy['x'], xy['y'], 'o', (randint(150, 170), randint(230, 255), randint(230, 255)), 'frozen', f"{planet.name} {radius}", planet, flags={'on_collide': stop_collision}))
        elif d10 <= 8:
            planet.entity_list.append(Ring(radius, '*', (randint(150, 170), randint(230, 255), randint(230, 255))))
        else:
            planet.moons.append(Moon(xy['x'], xy['y'], '*', (randint(150, 170), randint(230, 255), randint(230, 255)), 'frozen-asteroid', f"{planet.name} {radius}", planet, flags={'on_collide': stop_collision}))

    def generate_oort_cloud_planet(self, system:System, orbital_radius:int):
        # system.add_planet(Ring(orbital_radius, '*', (randint(150, 170), randint(230, 255), randint(230, 255))))
        pass

    def get_random_point_on_circle(self, radius):
        randTheta = randint(0, 360) * math.pi/180
        return {'x': int(radius * math.cos(randTheta)), 'y': int(radius * math.sin(randTheta))}

    def titus_bode(self, a, b, n):
        return int(a + ((b - a) * 2 * (n-2)))