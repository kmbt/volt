from __future__ import print_function
from pyglet.gl import *
import pyglet.gl as gl
import random
import copy


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

class Event(object):
    pass


class Observable(object):
    def __init__(self):
        self.callbacks = []
    def subscribe(self, callback):
        self.callbacks.append(callback)
    def fire(self, **attrs):
        e = Event()
        e.source = self
        for k, v in attrs.iteritems():
            setattr(e, k, v)
        for fn in self.callbacks:
            fn(e)

class MappingObservable(Observable):
    def __init__(self, map_fn, observed):
        super(MappingObservable, self).__init__()
        self.map_fn = map_fn
        self.observed = observed
        self.observed.subscribe(self.update)
    def update(self, e):
        self.fire(self.map_fn(e))
    def fire(self, e):
        for fn in self.callbacks:
            fn(e)

class FilteringObservable(Observable):
    def __init__(self, filter_fn, observed):
        super(FilteringObservable, self).__init__()
        self.filter_fn = filter_fn
        self.observed = observed
        self.observed.subscribe(self.update)
    def update(self, e):
        if self.filter_fn(e):
            self.fire(e)
    def fire(self, e):
        for fn in self.callbacks:
            fn(e)

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

        """
        self.streams = StreamCollection()
        self.streams.resize = BoxDimensions()
        self.streams.draw = ObservableStream()
        print(type(self.streams.resize))
        """
    

    def draw(self, e):
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
        self.streams.resize.update(x=x, y=y, dx=dx, dy=dy)
        print(x,y,dx,dy)
        self.streams.resize.fire()
        self.draw(None)
        # self.fire()
        


class StreamDispatcher(object):
    def __init__(self, stream_bundle):
        self.streams = stream_bundle
        self.items = []
        self.resize_streams = []
    def add(self, item):
        self.items.append(item)
        self.rewire()
    def rewire(self):
        pass

class ColumnsDispatcher(StreamDispatcher):
    def __init__(self, window, stream_bundle):
        self.window = window
        super(ColumnsDispatcher, self).__init__(stream_bundle)
        """
        self.streams.mouse_drag_release.subscribe(
                self.on_drag_release)
        """

    def add_column(self):
        self.add(Column(window, self.streams))

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
        self.resize_streams = []

        def make_fit_func(column):
            return lambda e: column.fit_to_rect(e.x, e.y, e.dx, e.dy)

        for column in self.items:
            print("wiring column", id(column))
            area_ratio = float(column.area_share) / area_sum
            map_fn = self.child_map_factory(ratio_accumulator, area_ratio)

            child_resize_stream = omap(map_fn, self.streams.columns_size)
            fun = column.fit_to_rect

            child_resize_stream.subscribe(make_fit_func(column))
            self.streams.draw.subscribe(column.draw)
            ratio_accumulator += area_ratio

    def child_filter_factory(self, x, dx):
        def filter_fn(e):
            if e.x >= x and e.x < (y+dx):
                return True
        return filter_fn

    def child_map_factory(self, r_acc, r_delta):
        def map_fn(e):
            print("acc", r_acc, "delta", r_delta)
            o = Event()
            o.x = e.x + r_acc * e.dx
            o.dx = r_delta * e.dx
            o.y, o.dy = e.y, e.dy
            print("-------o:", o.x, o.y, o.dx, o.dy)
            return o
        return map_fn
        


class Root(Widget):
    def __init__(self, window, streams):
        super(Root, self).__init__(window, streams)


        columns_streams = self.streams.clone()
        columns_streams.columns_size = columns_streams.window_size

        self.columns_dispatcher = ColumnsDispatcher(window, columns_streams)



    def add_column(self):
        self.columns_dispatcher.add_column()


    def add_zeropos(self, e):
        f = Event()
        f.x, f.y = 0, 0
        f.dx, f.dy = e.dx, e.dy
        return f

    def draw(self, e):
        # print("draw root", self.x, self.y, self.dx, self.dy)
        self.streams.draw.fire()


class Column(Widget):
    def __init__(self, window, streams):
        super(Column, self).__init__(window, streams)
        self.area_share = 1.0

        self.debug_rect = DebugRect(window, streams)
        """
        self.streams.resize.subscribe(lambda e:
                self.debug_rect.fit_to_rect(e.x, e.y, e.dx, e.dy))
        """
        self.streams.draw.subscribe(self.debug_rect.draw)
        
    def draw(self, e):
        # print("drawing column", id(self), self.x, self.y, self.dx, self.dy)
        self.streams.draw.fire()



class DebugRect(Widget):
    def __init__(self, window, streams):
        super(DebugRect, self).__init__(window, streams)
        self.window = window
        self.fill = tuple(random.uniform(.5,1.0) for _ in range(3))
        self.border = None

    def draw(self, e):
        # print("Drawing rect", id(self),  self.x, self.y, self.dx, self.dy)
        draw_rectangle(self.window, self.x, self.y, self.dx, self.dy,
                self.fill, self.border)

class ObservableStream(Observable):
    def __init__(self):
        super(ObservableStream, self).__init__()
        self.data = dict()
    def update(self, **kwargs):
        self.data = kwargs
        self.fire()
    def fire(self):
        return super(ObservableStream, self).fire(**self.data)

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
        e = Event()
        e.x, e.y = x, y
        self.start[1] = e

    def mouse_release(self, x, y, buttons, modifiers):
        print("mouse release")
        p = self.start[1]
        self.update(x=x, y=y, x0=p.x, y0=p.y)

    def mouse_drag(self, x, y, buttons, modifiers):
        pass

# class DrawEvent(Observable):

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

we.window_size.subscribe(lambda e: root.fit_to_rect(x=0, y=0, dx=e.dx, dy=e.dy))
we.draw.subscribe(lambda e: root.draw(e))

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
    we.mouse_position.update(x=x, y=window.height-y)

@window.event
def on_mouse_press(x, y, buttons, modifiers):
    we.mouse_drag_release.mouse_press(x=x, y=window.height-y, buttons=buttons, modifiers=modifiers)

@window.event
def on_mouse_release(x, y, buttons, modifiers):
    we.mouse_drag_release.mouse_release(x=x, y=window.height-y, buttons=buttons, modifiers=modifiers)


@window.event
def on_resize(dx, dy):
    print("resize!")
    we.window_size.update(x=0, y=0, dx=dx, dy=dy)

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
