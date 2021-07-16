from _pytest.monkeypatch import resolve
from source.planet.planet import Planet
from source.entity.entity import Entity
from source.area.area import Area
from source.action.move_action import MoveAction

def test_can_instantiate_planet():
    """
    Test that Planet imports properly and its constructor works.
    """
    assert Planet
    planet = Planet(1, 1, 'o', (255, 0, 0), 'test', 'test', None, 5)
    assert type(planet) is Planet

def test_can_generate_planetary_area(planet):
    assert isinstance(planet.generate_area(), Area)

def test_exit_planetary_area_works(planet):
    entity = Entity(4, 4, 'e', (0, 255, 0))
    area = planet.generate_area()
    area.add_entity(entity)
    result = planet.test_for_exit_planetary_area(area)
    assert result == [{'type': 'exit', 'exiting_entity': entity, 'exiting_too': None}]
    second_entity = Entity(1, 1, 'e', (255, 0, 0))
    area.add_entity(second_entity)
    result = planet.test_for_exit_planetary_area(area)
    assert result == [{'type': 'exit', 'exiting_entity': entity, 'exiting_too': None}]

def test_system_level_collide(planet, action_queue):
    area = Area()
    area.add_entity(planet.generate_planetary_entity())
    moving_entity = Entity(3, 5, 'e', (255,0,0))
    area.add_entity(moving_entity)
    move_action = MoveAction(moving_entity, 1, 1, 0, area)
    action_queue.push(move_action)
    result = action_queue.resolve_actions(1)
    assert result == [{
        'type': 'enter',
        'entering_entity': moving_entity,
        'target_entity': planet
    }]