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
        entity_at_target = self.area.get_entity_at_coordinates(self.originator.x + self.dx, self.originator.y + self.dy)
        if entity_at_target is not None:
            try:
                return entity_at_target.on_collide()
            except:
                self.area.transfer_entity_between_coordinates(self.originator.x, self.originator.y, self.originator.x + self.dx, self.originator.y + self.dy)
                return True
        else:
            self.area.transfer_entity_between_coordinates(self.originator.x, self.originator.y, self.originator.x + self.dx, self.originator.y + self.dy)
            return True