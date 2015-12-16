
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

    def get_child_idx(self, child):
        return self.children.index(child)

    def get_child_at_point(self, x, y, reverse=False):
        if reverse:
            order = reversed
        else:
            order = lambda a: a
        for child in order(self.children):
            if child.contains_point(x, y):
                return child

    def iter_children_at_point(self, x, y):
        widget = self
        yield widget
        while 1:
            child = widget.get_child_at_point(x, y, reverse=True)
            if not child:
                break
            yield child
            widget = child

    def get_children_at_point(self, x, y):
        return list(self.iter_children_at_point(x, y))


    def reorder_children(self, idx_from, idx_to):
        if idx_from == idx_to:
            return
        item = self.children.pop(idx_from)
        self.children.insert(idx_to, item)
        self.update()

    def attach_child_at_idx(self, idx_to, child):
        self.children.insert(idx_to, child)
        child.reparent(self)
        self.update()
    
    def detach_child_idx(self, idx):
        child = self.children.pop(idx)
        child.unparrent()
        self.update()

    def detach_child(self, child):
        self.children.remove(child)
        child.unparrent()
        self.update()

    def unparrent(self):
        self.parrent = None

    def reparent(self, parent):
        self.parent = parent

    def bubble_event(self, event_name, *args, **kwargs):
        self._bubble_event(event_name, self, *args, **kwargs)

    def _bubble_event(self, event_name, *args, **kwargs):
        # print "bubbling", event_name, "from", args[0], "at", self
        if self.parent == None:
            print "Warning, event", event_name, "has hit the root!"
            return
        handler_name = "on_{}".format(event_name)
        if hasattr(self.parent, handler_name):
            handler_method = getattr(self.parent, handler_name)
            result = handler_method(*args, **kwargs)
            if type(result) == bool and result == False:
                return
        self.parent._bubble_event(event_name, *args, **kwargs)
        
