import widget
import column

class Columns(widget.Widget):
    def __init__(self, parent):
        super(Columns, self).__init__(parent)
        # self.root.mouse.on_drag_release.append(self.on_drag_release)

    """
    def on_drag_release(self, x0, y0, x, y):
        if not self.contains_point(x0, y0):
            return None
        if not self.contains_point(x, y):
            return None

        idx_from = self.get_child_idx_at_point(x0, y0)
        idx_to = self.get_child_idx_at_point(x, y)

        self.reorder_children(idx_from, idx_to)
    """
        

    def add_column(self):
        col = column.Column(self)
        self.children.append(col)


    def update(self):
        area_sum = len(self.children)
        ratio_accumulator = 0

        for child in self.children:
            area_share = 1
            area_ratio = float(area_share)/area_sum

            x = self.x + ratio_accumulator * self.dx
            y = self.y
            dx = area_ratio * self.dx
            dy = self.dy

            child.resize(x, y, dx, dy)

            ratio_accumulator += area_ratio

    def on_reposition_window(self, target, x, y):
        if self.contains_point(x, y):
            windows_from = target.parent
            windows_to = self.get_child_at_point(x, y).windows
            windows_from.detach_child(target)
            idx_to = windows_to.get_child_idx_at_point(x, y)
            if idx_to is None:
                idx_to = 0
            else:
                idx_to += 1
            windows_to.attach_child_at_idx(idx_to, target)

