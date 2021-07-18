from source.action.action import Action
from source.area.area import Area

class MoveAction(Action):
    def __init__(self, originator, time_remaining:int, dx:int, dy:int, area:Area, resolution_function=lambda: None, **flags):
        Action.__init__(self, originator, time_remaining, resolution_function)
        self.area = area
        self.dx = dx
        self.dy = dy
        self.flags = flags
    
    def resolve_action(self):
        """
        Resolve this action by running any collision functions entities in the new sqaure have. Otherwise just send move.
        """
        entities_at_target = self.area.get_entities_at_coordinates(self.originator.x + self.dx, self.originator.y + self.dy)
        if entities_at_target is not None and len(entities_at_target) > 0:
            result_list = []
            collision = False
            for target_entity in entities_at_target:
                try:
                    result_list.append(target_entity.flags["on_collide"](target_entity, self.originator))
                    collision = True
                except:
                    pass
            if not collision:
                self.area.transfer_entity_between_coordinates(self.originator, self.originator.x, self.originator.y, self.originator.x + self.dx, self.originator.y + self.dy)
                result_list.append({"type": "move"})
            return result_list
        else:
            self.area.transfer_entity_between_coordinates(self.originator, self.originator.x, self.originator.y, self.originator.x + self.dx, self.originator.y + self.dy)
            return [{"type": "move"}]