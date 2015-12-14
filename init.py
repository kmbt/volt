from __future__ import print_function
from pyglet.gl import *
import pyglet.gl as gl
import random
import copy


# after http://stackoverflow.com/questions/1092531/event-system-in-python/2022629#2022629
class Event(list):
    """Event subscription.

    A list of callable objects. Calling an instance of this will cause a
    call to each item in the list in ascending order by index.

    Example Usage:
    >>> def f(x):
    ...     print 'f(%s)' % x
    >>> def g(x):
    ...     print 'g(%s)' % x
    >>> e = Event()
    >>> e()
    >>> e.append(f)
    >>> e(123)
    f(123)
    >>> e.remove(f)
    >>> e()
    >>> e += (f, g)
    >>> e(10)
    f(10)
    g(10)
    >>> del e[0]
    >>> e(2)
    g(2)

    """
    def __call__(self, *args, **kwargs):
        for f in self:
            f(*args, **kwargs)

    def __repr__(self):
        return "Event(%s)" % list.__repr__(self)

def EventCollection(object):
    pass

def draw_rectangle(window, x, y, dx, dy, fill=None, border=None):
    glColor3f(*fill)

    glBegin(GL_QUADS)
    glVertex2f(x, window.height-y)
    glVertex2f(x, window.height-y-dy)
    glVertex2f(x+dx, window.height-y-dy)
    glVertex2f(x+dx, window.height-y)
    glEnd()

    if border:
        glColor3f(*border)
        glBegin(GL_LINE_LOOP)
        glVertex2f(x, window.height-y)
        glVertex2f(x, window.height-y-dy)
        glVertex2f(x+dx, window.height-y-dy)
        glVertex2f(x+dx, window.height-y)
        glEnd()

class EventSignal(object):
    pass


class Observable(object):
    def __init__(self):
        self.callbacks = []
    def subscribe(self, callback):
        self.callbacks.append(callback)
    def fire(self, **attrs):
        e = EventSignal()
        e.source = self
        for k, v in attrs.iteritems():
            setattr(e, k, v)
        self.inject(e)
    def inject(self, e):
        for fn in self.callbacks:
            fn(e)

class ObservableStream(Observable):
    def feed_to(self, stream):
        self.subscribe(stream.inject)

class MappingObservable(ObservableStream):
    def __init__(self, map_fn, observed):
        super(MappingObservable, self).__init__()
        self.map_fn = map_fn
        self.observed = observed
        self.observed.subscribe(self.inject)
    def inject(self, e):
        super(MappingObservable, self).inject(self.map_fn(e))

class FilteringObservable(ObservableStream):
    def __init__(self, filter_fn, observed):
        super(FilteringObservable, self).__init__()
        self.filter_fn = filter_fn
        self.observed = observed
        self.observed.subscribe(self.inject)
    def inject(self, e):
        if self.filter_fn(e):
            super(MappingObservable, self).inject(e)


"""
    def __init__(self):
        super(ObservableStream, self).__init__()
        self.data = dict()
    def update(self, **kwargs):
        self.data = kwargs
        self.fire()
    def fire(self):
        return super(ObservableStream, self).fire(**self.data)
    def feed_into(self, streams):
        pass
        #TODO
"""

def ofilter(function, observable):
    return FilteringObservable(function, observable)

def omap(function, observable):
    return MappingObservable(function, observable)

class Widget(object):
    def __init__(self, window, streams):
        self.x, self.y = 0, 0
        self.dx, self.dy = 0, 0
        self.streams = streams
        self.window = window

        self.events = []
        self.children = []

        self.events = {}
        self.events["draw"] = Event()
        self.events["draw"].append(self.on_draw)


    def on_draw(self):
        pass


    def resize(self):
        pass


    def connect_streams(self, **kwargs):
        for key, value in kwargs.iteritems():
            setattr(self.streams, key, value)

    def fit_to_rect(self, x, y, dx, dy):
        print("fit to rect", type(self), id(self),  x, y, dx, dy)
        self.x, self.y = x, y
        self.dx, self.dy = dx, dy
        """
        print("bedzie kiszka")
        print(type(self))
        print(type(self.streams.resize))
        """
        # self.streams.resize.update(x=x, y=y, dx=dx, dy=dy)
        # print(x,y,dx,dy)
        # self.streams.resize.fire()
        # self.draw(None)
        # self.fire()
        


class StreamDispatcher(object):
    def __init__(self, window, streams):
        # self.streams = streams
        self.items = []
    def add(self, item):
        self.items.append(item)
        self.rewire()
    def rewire(self):
        pass

class ColumnsDispatcher(StreamDispatcher, Widget):
    def __init__(self, window, streams):
        # super(ColumnsDispatcher, self).__init__(window, streams)
        StreamDispatcher.__init__(self, window, streams)
        Widget.__init__(self, window, streams)

    def add_column(self):
        column_streams = self.streams.clone()
        self.add(Column(window, column_streams))

    def reorder(self, idx_from, idx_to):
        if idx_from == idx_to:
            return
        item = self.items.pop(idx_from)
        self.items.insert(idx_to, item)
        self.rewire()

    def on_drag_release(self, e):
        idx_from = -1
        idx_to = -1
        for idx, column in enumerate(self.items):
            if column.contains_point(e.x0, e.y0):
                idx_from = idx
            if column.contains_point(e.x, e.y):
                idx_to = idx
        if idx_from == idx_to:
            pass
        elif idx_from >= 0 and idx_to >= 0:
            self.reorder(idx_from, idx_to)

    def rewire(self):
        area_sum = sum(c.area_share for c in self.items)
        ratio_accumulator = 0
        # TODO: detach former resize streams
        # self.resize_streams = []

        def make_fit_func(column):
            return lambda e: column.fit_to_rect(e.x, e.y, e.dx, e.dy)

        for column in self.items:
            print("wiring column", id(column))

            column_streams = self.streams.clone()

            area_ratio = float(column.area_share) / area_sum
            map_fn = self.child_map_factory(ratio_accumulator, area_ratio)

            child_resize_stream = omap(map_fn, self.streams.columns_size)

            # fun = column.fit_to_rect

            # child_resize_stream.subscribe(make_fit_func(column))
            # self.streams.draw.subscribe(column.draw)
            ratio_accumulator += area_ratio

    def child_filter_factory(self, x, dx):
        def filter_fn(e):
            if e.x >= x and e.x < (y+dx):
                return True
        return filter_fn

    def child_map_factory(self, r_acc, r_delta):
        def map_fn(e):
            print("acc", r_acc, "delta", r_delta)
            o = EventSignal()
            o.x = e.x + r_acc * e.dx
            o.dx = r_delta * e.dx
            o.y, o.dy = e.y, e.dy
            print("-------o:", o.x, o.y, o.dx, o.dy)
            return o
        return map_fn
        


class Root(Widget):
    def __init__(self, window, streams):
        super(Root, self).__init__(window, streams)

        self.streams.window_size.subscribe(lambda e: self.fit_to_rect(x=0, y=0, dx=e.dx, dy=e.dy))
        self.streams.draw.subscribe(lambda e: root.draw(e))

        columns_streams = self.streams.clone()
        columns_streams.columns_size = columns_streams.window_size

        self.columns_dispatcher = ColumnsDispatcher(window, columns_streams)


    def add_column(self):
        self.columns_dispatcher.add_column()


    def add_zeropos(self, e):
        f = EventSignal()
        f.x, f.y = 0, 0
        f.dx, f.dy = e.dx, e.dy
        return f

    def draw(self, e):
        print("draw root", self.x, self.y, self.dx, self.dy)
        # self.streams.draw.fire()
        pass


class Column(Widget):
    def __init__(self, window, streams):
        super(Column, self).__init__(window, streams)
        self.area_share = 1.0

        debug_rect_streams = streams.clone()
        self.debug_rect = DebugRect(window, debug_rect_streams)
        
        self.streams.column_size.feed_to(self.debug_rect.streams.resize)
        """
        self.streams.resize.subscribe(lambda e:
                self.debug_rect.fit_to_rect(e.x, e.y, e.dx, e.dy))
        """
        # self.streams.draw.subscribe(self.debug_rect.draw)
        
    def draw(self, e):
        print("drawing column", id(self), self.x, self.y, self.dx, self.dy)



class DebugRect(Widget):
    def __init__(self, window, streams):
        super(DebugRect, self).__init__(window, streams)
        self.window = window
        self.fill = tuple(random.uniform(.5,1.0) for _ in range(3))
        self.border = None

        self.streams.draw.subscribe(self.draw)

        self.streams.resize = ObservableStream()
        self.streams.resize.subscribe(self.resize)

    def resize(self, e):
        self.fit_to_rect(x=e.x, y=e.y, dx=e.dx, dy=e.dy)

    def draw(self, e):
        print("Drawing rect", id(self),  self.x, self.y, self.dx, self.dy)
        draw_rectangle(self.window, self.x, self.y, self.dx, self.dy,
                self.fill, self.border)


class WindowSize(ObservableStream):
    pass

class MousePosition(ObservableStream):
    pass

class MouseDragRelease(ObservableStream):
    def __init__(self):
        super(MouseDragRelease, self).__init__()
        self.start = {}
        for i in range(1,4):
            self.start[i] = None
        
    def mouse_press(self, x, y, buttons, modifiers):
        e = EventSignal()
        e.x, e.y = x, y
        self.start[1] = e

    def mouse_release(self, x, y, buttons, modifiers):
        print("mouse release")
        p = self.start[1]
        self.fire(x=x, y=y, x0=p.x, y0=p.y)

    def mouse_drag(self, x, y, buttons, modifiers):
        pass

# class DrawEventSignal(Observable):

class BoxDimensions(ObservableStream):
    pass

class StreamCollection(object):
    def clone(self):
        return copy.copy(self)

class WindowStreams(StreamCollection):
    def __init__(self):
        self.mouse_position = MousePosition()
        self.mouse_drag_release  = MouseDragRelease()
        self.window_size = WindowSize()
        self.draw = Observable()


we = WindowStreams()

window = pyglet.window.Window()
root = Root(window, we)


for _ in range(4):
    root.add_column()

# self.streams.resize = omap(self.add_zeropos, parent_streams.window_size)

# we.window_size.subscribe(lambda e: root.fit_to_rect(x=0, y=0, dx=e.dx, dy=e.dy))
# we.draw.subscribe(lambda e: root.draw(e))

root.connect_streams(
        mouse_drag_release = we.mouse_drag_release
        )

"""
widgets = []
rectangle = Rectangle(window, 10, 10, 30, 30, (.5, .5, .5), (1.0, 0, 1.0))
widgets.append(rectangle)
"""





# we.mouse_position.subscribe(lambda e: print("moved!", e.x, e.y))
we.mouse_drag_release.subscribe(lambda e: print("dragged", e.__dict__))
@window.event
def on_mouse_motion(x, y, dx, dy):
    we.mouse_position.fire(x=x, y=window.height-y)

@window.event
def on_mouse_press(x, y, buttons, modifiers):
    we.mouse_drag_release.mouse_press(x=x, y=window.height-y, buttons=buttons, modifiers=modifiers)

@window.event
def on_mouse_release(x, y, buttons, modifiers):
    we.mouse_drag_release.mouse_release(x=x, y=window.height-y, buttons=buttons, modifiers=modifiers)


@window.event
def on_resize(dx, dy):
    we.window_size.fire(x=0, y=0, dx=dx, dy=dy)

# mouse_buttons = MouseButtons()
# gth = ofilter(lambda e: e.x>100 and e.y>100, mouse_position)
# mouse_position.subscribe(gth.input)
# gth.subscribe(lambda e: print("hi", e.x, e.y))
# gth.subscribe(lambda e: rectangle.move_to(e.x, e.y))





@window.event
def on_draw():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    we.draw.fire()


pyglet.app.run()
