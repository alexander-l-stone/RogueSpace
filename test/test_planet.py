from source.planet.planet import Planet
from source.entity.entity import Entity
from source.area.area import Area

def test_can_instantiate_planet():
    """
    Test that Planet imports properly and its constructor works.
    """
    assert Planet
    planet = Planet(1, 1, 'o', (255, 0, 0), 'test', 'test', None, 5)
    assert isinstance(planet, Planet)

def test_can_generate_planetary_area(planet):
    assert isinstance(planet.generate_planetary_area(), Area)