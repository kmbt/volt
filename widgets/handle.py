import widget
import debug_rect

class Handle(widget.Widget):
    def __init__(self, parent):
        super(Handle, self).__init__(parent)

        self.background = debug_rect.DebugRect(self)
        self.children.append(self.background)

    def update(self):
        self.background.resize(self.x, self.y, self.dx, self.dy)
