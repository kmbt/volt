import widget
import debug_rect

class Handle(widget.Widget):
    def __init__(self, parent):
        super(Handle, self).__init__(parent)

        self.background = debug_rect.DebugRect(self)
        self.children.append(self.background)

    def update(self):
        self.background.resize(self.x, self.y, self.dx, self.dy)

    def on_drag_release(self, x0, y0, x, y):
        self.parent.on_drag_release_handle(self, x, y)
        print "drag release at handle!"
        # emit event "on_drag_release_handle" that travels to the root of tree
