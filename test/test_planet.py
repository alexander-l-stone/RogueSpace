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

def test_exit_planetary_area_works(planet):
    entity = Entity(4, 4, 'e', (0, 255, 0))
    area = planet.generate_planetary_area()
    area.add_entity(entity)
    result = planet.test_for_exit_planetary_area(area)
    assert result == [{'type': 'exit', 'exiting_entity': entity, 'exiting_too': None}]
    second_entity = Entity(1, 1, 'e', (255, 0, 0))
    area.add_entity(second_entity)
    result = planet.test_for_exit_planetary_area(area)
    assert result == [{'type': 'exit', 'exiting_entity': entity, 'exiting_too': None}]