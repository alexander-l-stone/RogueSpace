from source.galaxy.galaxy import Galaxy
from source.system.system import System

def test_can_instantiate_galaxy():
    assert Galaxy
    new_galaxy = Galaxy()
    assert type(new_galaxy) is Galaxy

def test_galaxy_exploration(galaxy):
    galaxy.explored_dict = {(0,0): True, (1,0): True, (-1,0): True}
    assert galaxy.check_if_coordinate_is_explored(1, galaxy.sector_size - 1) == True
    assert galaxy.check_if_coordinate_is_explored(1, -1) == False

def test_galaxy_create_area(galaxy):
    galaxy.explored_dict = {(0,0): True, (1,0): True}
    in_area_system = System(50,50, 'O', (255,0,0), 'in-area', 'test', 10)
    out_of_area_system = System(520, 20, 'O', (255, 0, 0), 'test', 'test', 10)
    galaxy.system_dict[(in_area_system.x, in_area_system.y)] = in_area_system
    galaxy.system_dict[(out_of_area_system.x, out_of_area_system.y)] = out_of_area_system
    galaxy_area = galaxy.generate_local_area(250, 250)
    in_area_star = in_area_system.generate_star_entity()
    out_area_star = out_of_area_system.generate_star_entity()
    in_area = False
    out_area = False
    for item in galaxy_area.entity_dict.values():
        if (item[0].x == in_area_star.x and item[0].y == in_area_star.y and item[0].char == in_area_star.char):
            in_area = True
        if (item[0].x == out_area_star.x and item[0].y == out_area_star.y and item[0].char == out_area_star.char):
            out_area = True
    assert in_area == True
    assert out_area == False