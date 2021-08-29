from source.helper_functions.circle_conversions import convert_delta_to_theta,convert_theta_to_delta
from source.system.system import System

def resolve_jump_charge_action(originator, **flags):
    if(originator.fuel >= 4):
        originator.charging_jump = True
        originator.fuel -= 4
        originator.jump_charge -= 4
        return [{'type': 'charge', 'succeeded': True, 'originator':originator}]
    else:
        originator.charging_jump = False
        return [{'type': 'charge', 'succeeded': False, 'originator':originator}]
    

def resolve_jump_action(originator, **flags):
    if(not isinstance(flags['current_location'], System) ==True):
        return [{'type': 'jump', 'succeeded': False, 'originator':originator}]
    else:
        new_x = flags['current_location'].x
        new_y = flags['current_location'].y
        flags['game'].current_location = flags['game'].galaxy
        originator.relocate(new_x, new_y)
        for key, value in flags['game'].current_location.check_explored_corners(originator.get_x(), originator.get_y(), flags['game'].render_engine.SCREEN_WIDTH, flags['game'].render_engine.SCREEN_HEIGHT).items():
            if (value == False):
                flags['game'].current_location.generate_new_sector(key[0], key[1])
        flags['game'].current_area = flags['game'].current_location.generate_local_area(originator.get_x(), originator.get_y())
        flags['game'].current_area.add_entity(originator.entity_repr)
        flags['game'].render_engine.ui['game_window'].area = flags['game'].current_area
        return [{'type': 'jump', 'succeeded': True, 'x': originator.x, 'y': originator.y}]
 
def resolve_no_action(originator, **flags):
    return [{"type": 'none'}]

def resolve_wait_action(originator, **flags):
    return [{"type": 'wait'}]

def resolve_move_action(originator, **flags):
    """
    Resolve this action by running any collision functions entities in the new sqaure have. Otherwise just send move.
    """
    entities_at_target = flags['area'].get_entities_at_coordinates(originator.x + flags['dx'], originator.y + flags['dy'])
    if entities_at_target is not None and len(entities_at_target) > 0:
        result_list = []
        collision = False
        for target_entity in entities_at_target:
            try:
                result_list.append(target_entity.flags["on_collide"](target_entity, originator))
                collision = True
            except:
                pass
        if not collision:
            originator.relocate(originator.x + flags['dx'], originator.y + flags['dy'])
            result_list.append({"type": "move"})
        return result_list
    else:
        originator.relocate(originator.x + flags['dx'], originator.y + flags['dy'])
        return [{"type": "move"}]
    

def resolve_thrust_action(originator, **flags):
    return [{"type": "thrust", "value": {"dx": flags['dx'], "dy": flags['dy']}}]