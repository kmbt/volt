import widget
import window

class Windows(widget.Widget):
    def __init__(self, parent):
        super(Windows, self).__init__(parent)

        self.child_weights = []
        
        self.add_window()
        self.add_window()
        self.add_window()

    def add_window(self):
        win = window.Window(self)
        self.children.append(win)
        self.child_weights.append(1.0)

    def detach_child_idx(self, idx):
        self.child_weights.pop(idx)
        super(Windows, self).detach_child_idx(idx)

    def attach_child_at_idx(self, idx_to, child):
        self.child_weights.insert(idx_to, 1.0)
        super(Windows, self).attach_child_at_idx(idx_to, child)

    def update(self):
        weight_sum = sum(self.child_weights)
        ratio_accumulator = 0

        for child, weight in zip(self.children, self.child_weights):
            area_ratio = float(weight)/weight_sum

            x = self.x
            y = self.y + round(ratio_accumulator * self.dy)
            dx = self.dx
            dy = round(area_ratio * self.dy)

            child.resize(x, y, dx, dy)

            ratio_accumulator += area_ratio

    def on_reposition_window(self, target, x, y):
        if self.contains_point(x, y):
            idx_from = self.get_child_idx(target)
            idx_to = self.get_child_idx_at_point(x, y)
            self.reorder_children(idx_from, idx_to)
            return False
