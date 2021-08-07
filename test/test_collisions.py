from source.entity.entity import Entity
from source.action.action import Action
from source.action.action_queue import ActionQueue
from source.action.resolution_functions import resolve_move_action
from source.helper_functions.colliders import stop_collision

def test_stop_collision_exists():
    assert stop_collision

def test_stop_collision_returns_correct_value():
    first_entity = Entity(0, 0, '@', (255,255,255), None)
    second_entity = Entity(0, 1, '#', (255, 255, 255), None)
    result = stop_collision(first_entity, second_entity)
    assert result['type'] == 'stop'

def test_stop_collision_in_area_with_queue(area, entity):
    oldx, oldy = entity.x, entity.y
    collidable_entity = Entity(0, 1, '#', (255, 255, 255), None, on_collide=stop_collision)
    area.add_entity(entity)
    area.add_entity(collidable_entity)
    action_queue = ActionQueue()
    move_action = Action(entity, 1, resolve_move_action, dx=-1, dy=0, area=area)
    action_queue.push(move_action)
    result_list = action_queue.resolve_actions(1)
    assert entity.x == oldx and entity.y == oldy