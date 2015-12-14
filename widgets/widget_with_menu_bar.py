import widget
import debug_rect
import constants
import menu_bar

class WidgetWithMenuBar(widget.Widget):
    def __init__(self, parent):
        super(WidgetWithMenuBar, self).__init__(parent)

        self.menu_bar = menu_bar.MenuBar(self)
        self.children.append(self.menu_bar)
        self.bar_size = constants.BAR_SIZE

    def resize(self, x, y, dx, dy):
        super(WidgetWithMenuBar, self).resize(x, y, dx, dy)
        self.menu_bar.resize(x, y, dx, y+self.bar_size)
        self.body.resize(x, y+self.bar_size, dx, dy-self.bar_size)
    
