class BarSegment:
    """
    Bar types: 
    additive- if True, segment goes on the end of the bar
    if false, segment replaces the end of the bar
    """

    def __init__(self, parent, color_full, data_obj, value_param):
        self.parent = parent
        self.color_full = color_full
        self.data_obj = data_obj
        self.data_value_name = value_param
        self.visible = True
        self.segment_priority = 2

    