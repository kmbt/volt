import debug_rect
import columns
import widget_with_menu_bar

from constants import *


class Root(widget_with_menu_bar.WidgetWithMenuBar):
    def __init__(self, window):
        self.root = self
        self.window = window
        # self.mouse = input_system.mouse.Mouse()
        super(Root, self).__init__(self)
        self.parent = None

        # self.menu_bar = debug_rect.DebugRect(self)
        self.columns = columns.Columns(self)

        self.body = self.columns

        self.children.append(self.menu_bar)
        self.children.append(self.columns)

        self.bar_size = BAR_SIZE

    def add_column(self):
        self.columns.add_column()
