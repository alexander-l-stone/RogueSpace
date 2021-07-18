from source.action.action import Action

#TODO: Remove this
class JumpAction(Action):
    def __init__(self, originator, time_remaining:int, x, y, area, resolution_function: lambda: True, **flags):
        Action.__init__(self, originator, time_remaining, resolution_function)
        self.x = x
        self.y = y
        self.area = area
        self.flags = flags
    
    def resolve_action(self):
        return [{'type': 'jump', 'area': self.area, 'x': self.x, 'y': self.y}]