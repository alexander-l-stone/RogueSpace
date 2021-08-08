class UIMessage:
    def __init__(self, parent, x, y, message, color):
        self.x = parent.x + x
        self.y = parent.y + y
        self.message = message
        self.color = color
    
    def draw(self, root_console) -> None:
        root_console.print(self.x, self.y, self.message, fg=self.color)
