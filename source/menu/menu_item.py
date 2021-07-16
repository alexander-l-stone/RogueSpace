class MenuItem:
    def __init__(self, message, default_color=(255, 255, 255), active_color=(0, 255, 0), disabled_color=(120,120,120), disabled=False, **kwargs):
        self.message:str = message
        self.default_color:tuple = default_color
        self.active_color:tuple = active_color
        self.disabled_color:tuple = disabled_color
        self.disabled:bool = disabled
        self.kwargs:dict = kwargs

    def __str__(self):
        return self.message

    def __repr__(self):
        return f"Message: {self.message}\nDefault Color: {self.default_color}\nActive Color: {self.active_color}\nDisabled Color: {self.disabled_color}"