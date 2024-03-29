from source.action.action_queue import ActionQueue
from source.action.action import Action
from source.action.resolution_functions import *
from source.ship.ship import Ship
import random

def test_can_instantiate_action():
    """
    Tests that Action imports properly and its constructor works.
    """
    assert Action
    action = Action('test', 1, resolve_no_action)
    assert type(action) is Action


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
    second_action = Action('action_queue', 1, resolve_no_action)
    action_queue.push(second_action)
    action_queue.resolve_actions(1)
    assert action not in action_queue.heap 
    assert second_action not in action_queue.heap

def test_actions_of_different_times_handled_properly(long_action):
    """
    This tests to see if this can handle actions of different times
    """
    second_action = Action('action_queue', 1, resolve_no_action)
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
        action = Action('test', i, resolve_no_action)
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
        action = Action(f'test {i}', i, resolve_no_action)
        action_queue.push(action)
    assert len(action_queue.heap) == 10
    for time,length in ((2,7),(4,5),(8,1),(10,0)):
        action_queue.resolve_actions(time)
        assert len(action_queue.heap) == length

def test_can_resolve_move_action(area):
    """"
    Test that move actions can resolve and move an entity.
    """
    dx = 0
    dy = 1
    new_object = Ship('?', (255, 0, 0), curr_area=area)
    oldx = new_object.x
    oldy = new_object.y
    action_queue = ActionQueue()
    action_queue.push(Action(new_object, 1, resolve_move_action, dx=dx, dy=dy, area=area))
    results = action_queue.resolve_actions(1)
    assert results[0] == {'type': 'move'}
    assert (new_object.x == oldx + dx) and (new_object.y == oldy + dy)