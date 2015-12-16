class MouseController(object):
    def __init__(self, root, mouse):
        self.root = root
        self.mouse = mouse
        self.mouse.on_drag_release.append(self.on_drag_release)

    def on_drag_release(self, x0, y0, x, y):
        for widget in reversed(self.root.get_children_at_point(x0, y0)):
            # print widget
            try: 
                event_handler = widget.on_drag_release
            except AttributeError:
                continue
            event_handler(self, x0, y0, x, y)
