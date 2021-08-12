class UIMessage:
    def __init__(self, parent, x, y, message, color):
        self.x = parent.x + x
        self.y = parent.y + y
        self.message = message
        self.color = color
        self.hidden = False
    
    def draw(self, root_console) -> None:
        if self.hidden:
            return
        root_console.print(self.x, self.y, self.message, fg=self.color)
