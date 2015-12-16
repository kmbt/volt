import debug_rect
import widget_with_menu_bar
import windows
import widget

class Window(widget_with_menu_bar.WidgetWithMenuBar):
    def __init__(self, parent):
        super(Window, self).__init__(parent)

        # self.body = debug_rect.DebugRect(self)
        self.body = widget.Widget(self)

        self.children.append(self.body)
    
    def on_drag_release_handle(self, target, x, y):
        print "drag release"
        self.bubble_event("reposition_window", x, y)
        return False
