import debug_rect
import widget_with_menu_bar
import windows

class Window(widget_with_menu_bar.WidgetWithMenuBar):
    def __init__(self, parent):
        super(Window, self).__init__(parent)

        self.body = debug_rect.DebugRect(self)

        self.children.append(self.body)


