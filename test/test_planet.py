
from source.planet.planet import Planet
from source.entity.entity import Entity
from source.area.area import Area
from source.action.action import Action
from source.action.resolution_functions import resolve_move_action

def test_can_instantiate_planet():
    """
    Test that Planet imports properly and its constructor works.
    """
    assert Planet
    planet = Planet(1, 1, 'o', (255, 0, 0), 'test', 'test', None, 5)
    assert type(planet) is Planet