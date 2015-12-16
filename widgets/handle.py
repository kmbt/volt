import widget
import debug_rect

class Handle(widget.Widget):
    def __init__(self, parent):
        super(Handle, self).__init__(parent)

        self.background = debug_rect.DebugRect(self)
        self.children.append(self.background)

    def update(self):
        self.background.resize(self.x, self.y, self.dx, self.dy)

    def on_drag_release(self, target, x0, y0, x, y):
        self.bubble_event("drag_release_handle", x, y)
