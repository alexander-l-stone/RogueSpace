from source.area.area import Area
from source.entity.entity import Entity
from source.action.action_queue import ActionQueue
from source.action.move_action import MoveAction
from source.helper_functions.colliders import stop_collision

def test_stop_collision_exists():
    assert stop_collision

def test_stop_collision_returns_correct_value():
    first_entity = Entity(0, 0, '@', (255,255,255))
    second_entity = Entity(0, 1, '#', (255, 255, 255))
    result = stop_collision(first_entity, second_entity)
    assert result['type'] == 'stop'

def test_stop_collision_in_area_with_queue(area, entity):
    oldx, oldy = entity.x, entity.y
    collidable_entity = Entity(0, 1, '#', (255, 255, 255), flags={'on_collide': stop_collision})
    area.add_entity(entity)
    area.add_entity(collidable_entity)
    action_queue = ActionQueue()
    move_action = MoveAction(entity, 1, -1, 0, area)
    action_queue.push(move_action)
    action_queue.resolve_actions(1)
    assert entity.x == oldx and entity.y == oldy