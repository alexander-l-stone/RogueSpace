from source.draw.area.area import Area
from source.draw.entity.entity import Entity

def test_can_instantiate_area():
    """
    Test that Area can be instantiated
    """
    assert Area
    new_area = Area()
    assert type(new_area) is Area

def test_can_add_entity(entity, area):
    """
    Test that you can add an entity to an area
    """
    area.add_entity(entity)
    assert area.entity_dict[(entity.x, entity.y)][0] is entity
    assert entity.curr_area is area
    assert area.entity_dict[(entity.get_abs_x(), entity.get_abs_y())][0] is entity

def test_can_delete_entity(area, entity):
    """
    Test that you can delete an entity from an area
    """
    area.add_entity(entity)
    deleted_entity = area.delete_entity(entity)
    assert deleted_entity.curr_area is None
    assert area.entity_dict[(deleted_entity.x, deleted_entity.y)] == []


def test_can_get_entity_at_coordiantes(area_with_entity):
    """
    Test can get entity at coordinates
    
    area_with_entity has an Entity at 1,1
    """
    actual_entity = area_with_entity.get_entities_at_coordinates(1, 1)[0]
    not_an_entity = area_with_entity.get_entities_at_coordinates(2, 2)
    assert isinstance(actual_entity, Entity)
    assert actual_entity.curr_area == area_with_entity
    assert not_an_entity == []