#TODO: move the area, x, and y of the resolve jump action into a value dict
from source.area.tilesetarea import TilesetArea

def resolve_jump_action(originator, flags):
        return [{'type': 'jump', 'area': flags['area'], 'x': originator.x, 'y': originator.y}]

def resolve_no_action(originator, flags):
    return [{"type": 'none'}]

def resolve_wait_action(originator, flags):
    return [{"type": 'wait'}]

def resolve_move_action(originator, flags):
    """
    Resolve this action by running any collision functions entities in the new sqaure have. Otherwise just send move.
    """
    if type(flags['area']) is TilesetArea:
        result_list = []
        entities_at_target = flags['area'].get_entities_at_coordinates(originator.x + flags['dx'], originator.y + flags['dy'])
        if entities_at_target is not None and len(entities_at_target) > 0:
            collision = False
            for target_entity in entities_at_target:
                try:
                    result_list.append(target_entity.flags["on_collide"](target_entity, originator))
                    collision = True
                except:
                    pass
            if not collision:
                flags['area'].transfer_entity_between_coordinates(originator, originator.x, originator.y, originator.x + flags['dx'], originator.y + flags['dy'])
                result_list.append({"type": "move"})
        if flags['area'].tileset.tiles[flags['area'].entity_array[originator.x + flags['dx']][originator.y + flags['dy']]].flags["on_collide"]:
            result_list.append(flags['area'].tileset.tiles[flags['area'].entity_array[originator.x + flags['dx']][originator.y + flags['dy']]].flags["on_collide"])
        else:
            flags['area'].transfer_entity_between_coordinates(originator, originator.x, originator.y, originator.x + flags['dx'], originator.y + flags['dy'])
            result_list.append({"type": "move"})
        return result_list
    else:
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
                flags['area'].transfer_entity_between_coordinates(originator, originator.x, originator.y, originator.x + flags['dx'], originator.y + flags['dy'])
                result_list.append({"type": "move"})
            return result_list
        else:
            flags['area'].transfer_entity_between_coordinates(originator, originator.x, originator.y, originator.x + flags['dx'], originator.y + flags['dy'])
            return [{"type": "move"}]

def resolve_thrust_action(originator, flags):
    return [{"type": "thrust", "value": {"dx": flags['dx'], "dy": flags['dy']}}]