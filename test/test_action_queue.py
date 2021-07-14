from source.action.action_queue import ActionQueue
from source.action.action import Action
from source.action.move_action import MoveAction
import random

def test_can_instantiate_action():
    """
    Tests that Action imports properly and its constructor works.
    """
    assert Action
    action = Action('test', 1)
    assert type(action) is Action

def test_can_instantiate_move_action(area):
    assert MoveAction
    move_action = MoveAction('test', 1, 1, 1, area)
    assert type(move_action) is MoveAction

def test_can_instantiate_action_queue():
    """
    Tests that Action Queue imports properly and its constructor works.
    """
    assert ActionQueue
    action_queue = ActionQueue()
    assert type(action_queue) is ActionQueue

def test_can_pop_empty_queue_for_no_effect():
    """
    Tests that popping an empty queue does nothing
    """
    action_queue = ActionQueue()
    action_queue.pop()
    assert len(action_queue.heap) == 0

def test_can_add_actions(action):
    """
    Tests that actions can be added to the queue
    """
    action_queue = ActionQueue()
    action_queue.push(action)
    assert action in action_queue.heap

def test_can_pop_actions(action):
    """
    Tests that after an action is pushed, pop will remove it
    """
    action_queue = ActionQueue()
    action_queue.push(action)
    action_queue.pop()
    assert action not in action_queue.heap


def test_can_resolve_actions(action):
    """
    Tests that an action with time will be removed by resolving time 1 actions
    """
    action_queue = ActionQueue()
    action_queue.push(action)
    action_queue.resolve_actions(1)
    assert action not in action_queue.heap

def test_long_actions_remain_after_pop(long_action):
    """
    Tests that actions with sufficient time are not resolved by sending less than their time
    """
    action_queue = ActionQueue()
    action_queue.push(long_action)
    action_queue.resolve_actions(1)
    assert long_action in action_queue.heap

def test_multiple_actions_resolve_at_once(action):
    """
    This tests to see if multiple actions can get resolved at once
    """
    action_queue = ActionQueue()
    action_queue.push(action)
    second_action = Action('action_queue', 1)
    action_queue.push(second_action)
    action_queue.resolve_actions(1)
    assert action not in action_queue.heap 
    assert second_action not in action_queue.heap

def test_actions_of_different_times_handled_properly(action, long_action):
    """
    This tests to see if this can handle actions of different times
    """
    second_action = Action('action_queue', 1)
    action_queue = ActionQueue()
    action_queue.push(second_action)
    action_queue.push(long_action)
    action_queue.resolve_actions(1)
    assert long_action in action_queue.heap
    assert second_action not in action_queue.heap

def test_pop_order():
    """
    This tests to see if the queue returns actions in temporal order
    """
    action_queue = ActionQueue()
    rand_order = list(range(0,10))
    random.shuffle(rand_order)
    for i in rand_order:
        action = Action('test', i)
        action_queue.push(action)
    for i in range(0,10):
        action = action_queue.pop()
        assert action.time == i

def test_multiple_resolve():
    """
    This tests to see if the queue handles nonadjacent resolution
    """
    action_queue = ActionQueue()
    rand_order = list(range(0,10))
    random.shuffle(rand_order)
    for i in rand_order:
        action = Action(f'test {i}', i)
        action_queue.push(action)
    assert len(action_queue.heap) == 10
    for time,length in ((2,7),(4,5),(8,1),(10,0)):
        action_queue.resolve_actions(time)
        assert len(action_queue.heap) == length

def test_can_resolve_move_action(area, entity):
    """"
    Test that move actions can resolve and move an entity.
    """
    dx = 0
    dy = 1
    oldx = entity.x
    oldy = entity.y
    area.add_entity(entity)
    action_queue = ActionQueue()
    action_queue.push(MoveAction(entity, 1, dx, dy, area))
    results = action_queue.resolve_actions(1)
    assert results[0] == {'type': 'move'}
    assert (entity.x == oldx + dx) and (entity.y == oldy + dy)