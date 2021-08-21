class UIMessage:
    def __init__(self, parent, x, y, message, color):
        self.x = parent.x + x
        self.y = parent.y + y
        self.message = message
        self.color = color
        self.visible = True
        self.priority = 2
    
    def draw(self, root_console, tick_count) -> None:
        if not self.visible:
            return
        root_console.print(self.x, self.y, self.message, fg=self.color)
