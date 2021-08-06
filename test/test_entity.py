from source.entity.entity import Entity

def test_can_instantiate_entity():
    """
    Test that Entity can be instantiated
    """
    assert Entity
    new_entity = Entity(1, 1, '@', (255, 255, 255), None)
    assert type(new_entity) is Entity