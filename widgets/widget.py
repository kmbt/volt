
class Widget(object):
    def __init__(self, parent):
        self.parent = parent
        self.root = parent.root
        self.x, self.y = 0, 0
        self.dx, self.dy = 0, 0

        self.children = []

    def draw(self):
        for child in self.children:
            child.draw()

    def update(self):
        pass

    def resize(self, x, y, dx, dy):
        self.x, self.y = x, y
        self.dx, self.dy = dx, dy
        self.update()

    def contains_point(self, x, y):
        if x < self.x:
            return False
        if x > self.x+self.dx:
            return False
        if y < self.y:
            return False
        if y > self.y+self.dy:
            return False
        return True

    def get_child_idx_at_point(self, x, y):
        for idx, child in enumerate(self.children):
            if child.contains_point(x, y):
                return idx

    def get_child_at_point(self, x, y):
        for child in self.children:
            if child.contains_point(x, y):
                return child

    def iter_children_at_point(self, x, y):
        widget = self
        while 1:
            child = widget.get_child_at_point(x, y)
            if not child:
                break
            yield child
            widget = child

    def get_children_at_point(self, x, y):
        return list(self.get_child_at_point(x, y))


    def reorder_children(self, idx_from, idx_to):
        if idx_from == idx_to:
            return
        item = self.children.pop(idx_from)
        self.children.insert(idx_to, item)
        self.update()
