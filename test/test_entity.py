from source.draw.entity.entity import Entity

def test_can_instantiate_entity(system):
    """
    Test that Entity can be instantiated
    """
    assert Entity
    new_entity = Entity(1, 1, '@', (255, 255, 255), system)
    assert type(new_entity) is Entity

def test_can_reposition_entity(entity, area):
    """
    Test can transfer entity between different points in an area
    """
    new_x = 2
    new_y = 2
    area.add_entity(entity)
    entity.move_entity_to_coordinates(new_x, new_y)
    assert entity.get_abs_x() == new_x
    assert entity.get_abs_y() == new_y
    assert area.entity_dict[(new_x, new_y)][0] is entity
