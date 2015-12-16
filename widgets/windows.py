import widget
import window

class Windows(widget.Widget):
    def __init__(self, parent):
        super(Windows, self).__init__(parent)
        
        self.add_window()
        self.add_window()
        self.add_window()

    def add_window(self):
        win = window.Window(self)
        self.children.append(win)

    def update(self):
        area_sum = len(self.children)
        ratio_accumulator = 0

        for child in self.children:
            area_share = 1
            area_ratio = float(area_share)/area_sum

            x = self.x
            y = self.y + ratio_accumulator * self.dy
            dx = self.dx
            dy = area_ratio * self.dy

            child.resize(x, y, dx, dy)

            ratio_accumulator += area_ratio

    """
    def on_reposition_window(self, target, x, y):
        if self.contains_point(x, y):
            idx_from = self.get_child_idx(target)
            idx_to = self.get_child_idx_at_point(x, y)
            self.reorder_children(idx_from, idx_to)
            return False
    """
