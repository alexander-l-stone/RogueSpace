class UIBar:
    def __init__(self, parent, x, y, width, height, color_full, color_empty, text_color, data_obj, value_param, max_param):
        self.parent = parent
        self.x = parent.x + x
        self.y = parent.y + y
        self.width = width
        self.height = height
        self.color_full = color_full
        self.color_empty = color_empty
        self.text_color = text_color
        
        self.additive_segments = []
        self.contractive_segments = []

        self.data_obj = data_obj
        self.data_value_name = value_param
        self.data_max_name = max_param

        self.visible = True
        self.priority = 2

    def draw(self, root_console, tick_count) -> None:
        if not self.visible:
            return

        max_value = getattr(self.data_obj, self.data_max_name)
        curr_value = getattr(self.data_obj, self.data_value_name)

        extended_max = max_value
        contracted_value = curr_value
        for ui_segment in self.additive_segments:
            extended_max += getattr(ui_segment.data_obj, ui_segment.data_value_name)
        for ui_segment in self.contractive_segments:
            contracted_value -=getattr(ui_segment.data_obj, ui_segment.data_value_name)

        if(len(self.contractive_segments) > 0):
            print(contracted_value)

        if(contracted_value < 0):
            contracted_value = 0

        full_width = int(self.width * contracted_value / extended_max)

        root_console.draw_rect(self.x, self.y, full_width, self.height, ord(' '), bg=self.color_full)

        tile_value = extended_max / self.width
        if curr_value < extended_max:
            tile_fill = contracted_value % tile_value
            rs = [self.color_full[0]]
            gs = [self.color_full[1]]
            bs = [self.color_full[2]]
            ps = [tile_fill/tile_value]
            bar_progress = full_width

            for ui_segment in self.contractive_segments:
                #Tile fill should always be the leftover stuff from the previous segment(s) bleeding into the first tile of this segment
                if(tile_fill + getattr(ui_segment.data_obj, ui_segment.data_value_name) >= tile_value):
                    rs.append(ui_segment.color_full[0]) 
                    gs.append(ui_segment.color_full[1]) 
                    bs.append(ui_segment.color_full[2]) 
                    ps.append(1 - tile_fill/tile_value) 

                    color_partial = self.erp_color(rs,gs,bs,ps)
                    root_console.print(self.x + bar_progress, self.y, ' ', bg=color_partial)

                    bar_progress += 1
                    
                    print(f"fill:{tile_fill} value:{tile_value}")
                    full_start = getattr(ui_segment.data_obj, ui_segment.data_value_name) - (tile_value - tile_fill) #The amount of barstuff disregarding the interpolated portion
                    full_width = int(  full_start / tile_value )
                    root_console.draw_rect(self.x + bar_progress, self.y, full_width, self.height, ord(' '), bg=ui_segment.color_full)

                    bar_progress += full_width

                    tile_fill = full_start % tile_value
                    rs = [ui_segment.color_full[0]]
                    gs = [ui_segment.color_full[1]]
                    bs = [ui_segment.color_full[2]]
                    ps = [tile_fill/tile_value]
                else:
                    rs.append(ui_segment.color_full[0]) 
                    gs.append(ui_segment.color_full[1]) 
                    bs.append(ui_segment.color_full[2]) 
                    curr_value = getattr(ui_segment.data_obj, ui_segment.data_value_name)
                    ps.append(curr_value/tile_value) 
                    tile_fill += curr_value % tile_value
            rs.append(self.color_empty[0]) 
            gs.append(self.color_empty[1]) 
            bs.append(self.color_empty[2]) 
            ps.append(1 - tile_fill/tile_value) 
            
            color_partial = self.erp_color(rs,gs,bs,ps)
            root_console.print(self.x + bar_progress, self.y, ' ', bg=color_partial)

            bar_progress += 1

            root_console.draw_rect(self.x + bar_progress, self.y, self.width - bar_progress, self.height, ord(' '), bg=self.color_empty)

                



       # root_console.draw_rect(self.x + full_width, self.y, empty_width, self.height, ord(' '), bg=self.color_empty)
        # partially full tile

        #TODO uncertain if this text will always accurately reflect 'real' values
        #e.g. temp health will not increase 'current' health according to this text display
        text = str(curr_value) +  ' / ' + str(max_value)
        text_center = self.x + (self.width / 2) # do not integer divide; will only compound rounding error
        text_start = int(text_center - (len(text) / 2))
        text_height = self.height // 2
        root_console.print(text_start + 25, self.y + text_height, text, fg= (255,255,255))#self.text_color)

        root_console.print(self.x, self.y + text_height, '1234567890abcdefghij', fg=(0,0,255))

    def lerp_color(self, s, e, p):
        return (
            int(self.lerp(s[0], e[0], p)),
            int(self.lerp(s[1], e[1], p)),
            int(self.lerp(s[2], e[2], p))
        )

    def lerp(self, start, end, p):
        return start * (1 - p) + end * p

    #ps should be an array of values summing to 1
    def erp_color(self, rs, gs, bs, ps):
        return( 
            int(self.erp(rs,ps)),
            int(self.erp(gs,ps)),
            int(self.erp(bs,ps))
        )

    def erp(self, points, ps):
        result = 0
        for i in range(len(points)):
            result += ps[i] * points[i]
        return result
