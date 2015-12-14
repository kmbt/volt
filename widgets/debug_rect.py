import random
import widget
from graphics import draw_rectangle

class DebugRect(widget.Widget):
    def __init__(self, parent):
        super(DebugRect, self).__init__(parent)
        self.fill = tuple(random.uniform(.0,1.0) for _ in range(3))
        self.border = None

    def draw(self):
        # print("Drawing rect", id(self),  self.x, self.y, self.dx, self.dy)
        draw_rectangle(self.root.window, self.x, self.y, self.dx, self.dy,
                self.fill, self.border)
