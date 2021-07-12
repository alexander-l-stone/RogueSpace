from source.planet.moon import Moon

def test_can_instantiate_moon():
    assert Moon
    new_moon = Moon(0, 0, 'o', (255, 255, 255), 'test', 'test', None)
    assert isinstance(new_moon, Moon)

def test_can_create_moon_entity():
    new_moon = Moon(0, 0, 'o', (255, 255, 255), 'test', 'test', None)
    moon_entity = new_moon.generate_entity()
    assert moon_entity.x == new_moon.x
    assert moon_entity.y == new_moon.y
    assert moon_entity.char == new_moon.char
    assert moon_entity.color == new_moon.color