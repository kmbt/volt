
class MouseController(object):
    def __init__(self, root, mouse):
        self.root = root
        self.mouse = mouse
        self.mouse.on_drag_release.append(self.on_drag_release)

    def on_drag_release(self, x0, y0, x, y):
        for widget in self.root.iter_children_at_point(x0, y0):
            print widget
