class UIBar:
    def __init__(self, parent, x, y, width, height, color_full, color_empty, text_color, curr_value, max_value):
        self.parent = parent
        self.x = parent.x + x
        self.y = parent.y + y
        self.width = width
        self.height = height
        self.color_full = color_full
        self.color_empty = color_empty
        self.text_color = text_color
        self.curr_value = curr_value
        self.max_value = max_value


    def draw(self, root_console) -> None:
        full_width = int(self.width * (self.curr_value / self.max_value))
        empty_width = self.width - full_width

        root_console.draw_rect(self.x, self.y, full_width, self.height, ord(' '), bg=self.color_full)
        root_console.draw_rect(self.x + full_width, self.y, empty_width, self.height, ord(' '), bg=self.color_empty)
        

        text = str(self.curr_value) + ' / ' + str(self.max_value)
        text_center = self.x + (self.width / 2) # do not integer divide; will only compound rounding error
        text_start = int(text_center - (len(text) / 2))
        text_height = self.height // 2
        root_console.print(text_start, self.y + text_height, text, fg=self.text_color)
