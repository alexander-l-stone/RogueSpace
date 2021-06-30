from source.entity.entity import Entity

class Action:
    """
    Class for holding an action, extend this to make new actions
    """
    def __init__(self, originator, time_remaining:int, **kwargs):
        self.originator = originator
        self.time:int = time_remaining
        self.kwargs:dict = kwargs
    
    def __add__(self, o:int):
        # Raise a type error if there is not an int being added here
        if not isinstance(o, int):
            raise TypeError
        self.time += 1

    def __sub__(self, o:int):
        if not isinstance(o, int):
            raise TypeError
        self.time -= 1
    
    def __eq__(self, obj):
        if isinstance(obj, int):
            return self.time == obj
        if isinstance(obj, Action):
            return self.time == obj.time
        raise TypeError(f"incomparable types Action == {type(obj)}")
    
    def __lt__(self, obj):
        if isinstance(obj, int):
            return self.time < obj
        if isinstance(obj, Action):
            return self.time < obj.time
        raise TypeError(f"incomparable types Action < {type(obj)}")

    def __gt__(self, obj):
        if isinstance(obj, int):
            return self.time > obj
        if isinstance(obj, Action):
            return self.time < obj.time
        raise TypeError(f"incomparable types Action < {type(obj)}")

    def resolve_action(self):
        """
        Resolve this action
        """
        return True