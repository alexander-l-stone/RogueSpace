
from source.stellar_objects.planet import Planet

def test_can_instantiate_planet():
    """
    Test that Planet imports properly and its constructor works.
    """
    assert Planet
    planet = Planet(1, 1, 'o', (255, 0, 0), 'test', 'test', None, 5)
    assert type(planet) is Planet