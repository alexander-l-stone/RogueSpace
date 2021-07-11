from source.action.action import Action

class JumpAction(Action):
    def __init__(self, originator, time_remaining:int, x, y, area, **kwargs):
        Action.__init__(self, originator, time_remaining)
        self.x = x
        self.y = y
        self.area = area
        self.kwargs = kwargs
    
    def resolve_action(self):
        return [{'type': 'jump', 'area': self.area, 'x': self.x, 'y': self.y}]