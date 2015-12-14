import debug_rect
import widget_with_menu_bar
import windows

class Column(widget_with_menu_bar.WidgetWithMenuBar):
    def __init__(self, parent):
        super(Column, self).__init__(parent)

        self.windows = windows.Windows(self)
        self.body = self.windows

        self.children.append(self.windows)


