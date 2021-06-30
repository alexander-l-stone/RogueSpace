from source.area.area import Area
from source.entity.entity import Entity

def test_can_instantiate_area():
    """
    Test that Area can be instantiated
    """
    assert Area
    new_area = Area()
    assert isinstance(new_area, Area)

def test_can_add_entity(entity, area):
    """
    Test that you can add an entity to an area
    """
    area.add_entity(entity)
    assert area.entity_dict[(entity.x, entity.y)] is entity
    assert entity.curr_area is area

def test_can_add_entity_to_coordinates(entity, area):
    """
    Test that you can add an entity to an area at a specific set of coordinates
    """
    new_x = 2
    new_y = 2
    area.add_entity_at_coordinates(new_x, new_y, entity)
    assert entity.x == new_x
    assert entity.y == new_y
    assert entity.curr_area is area
    assert area.entity_dict[(new_x, new_y)] is entity

def test_can_delete_entity(area_with_entity):
    """
    Test that you can delete an entity from an area
    
    area_with_entity has an Entity at 1,1
    """
    deleted_entity = area_with_entity.delete_entity_at_coordinates(1, 1)
    assert deleted_entity.curr_area is None
    assert (deleted_entity.x, deleted_entity.y) not in area_with_entity.entity_dict

def test_can_transfer_entity(entity, area):
    """
    Test can transfer entity between different points in an area
    """
    new_x = 2
    new_y = 2
    area.add_entity(entity)
    area.transfer_entity_between_coordinates(entity.x, entity.y, new_x, new_y)
    assert entity.x == new_x
    assert entity.y == new_y
    assert area.entity_dict[(new_x, new_y)] is entity

def test_can_get_entity_at_coordiantes(area_with_entity):
    """
    Test can get entity at coordinates
    
    area_with_entity has an Entity at 1,1
    """
    actual_entity = area_with_entity.get_entity_at_coordinates(1, 1)
    not_an_entity = area_with_entity.get_entity_at_coordinates(2, 2)
    assert isinstance(actual_entity, Entity)
    assert actual_entity.curr_area == area_with_entity
    assert not_an_entity is None