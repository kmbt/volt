import widget
import debug_rect
import constants

class MenuBar(widget.Widget):
    def __init__(self, parent):
        super(MenuBar, self).__init__(parent)

        self.background = debug_rect.DebugRect(self)
        self.handle = debug_rect.DebugRect(self)
        self.text_field = debug_rect.DebugRect(self)

        self.children.append(self.background)
        self.children.append(self.handle)
        self.children.append(self.text_field)

        self.bar_size = constants.BAR_SIZE
        self.handle_size = int(0.6*constants.BAR_SIZE)
        self.handle_spacing = int((constants.BAR_SIZE-self.handle_size)/2)

    def update(self):
        self.background.resize(self.x, self.y, self.dx, self.dy)

        self.handle.resize(
                self.x + self.handle_spacing,
                self.y + self.handle_spacing,
                self.handle_size,
                self.handle_size
                )

        self.text_field.resize(
                self.x + self.bar_size,
                self.y,
                self.dx - self.bar_size,
                self.dy
                )
