from source.action.action import Action
from source.area.area import Area

class MoveAction(Action):
    def __init__(self, originator, time_remaining:int, dx:int, dy:int, area:Area, **kwargs):
        Action.__init__(self, originator, time_remaining)
        self.area = area
        self.dx = dx
        self.dy = dy
    
    def resolve_action(self):
        """
        Resolve this action by running any collision functions entities in the new sqaure have.
        """
        entities_at_target = self.area.get_entities_at_coordinates(self.originator.x + self.dx, self.originator.y + self.dy)
        if len(entities_at_target) > 0:
            result_list = []
            for target_entity in entities_at_target:
                try:
                    result_list.append(target_entity.flags["on_collide"](target_entity, self.originator))
                except:
                    result_list.append(self.area.transfer_entity_between_coordinates(self.originator, self.originator.x, self.originator.y, self.originator.x + self.dx, self.originator.y + self.dy))
            return result_list
        else:
            self.area.transfer_entity_between_coordinates(self.originator, self.originator.x, self.originator.y, self.originator.x + self.dx, self.originator.y + self.dy)
            return [{"type": "move"}]