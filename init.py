from __future__ import print_function
from pyglet.gl import *
import pyglet.gl as gl
import random
import copy
import widgets.root
import input_system.mouse
from widgets.widget import Widget
import inspect
from pprint import pprint
from controllers import mouse_controller



# after http://stackoverflow.com/questions/1092531/event-system-in-python/2022629#2022629

def EventCollection(object):
    pass


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



class StreamDispatcher(object):
    def __init__(self, window, streams):
        # self.streams = streams
        self.items = []
    def add(self, item):
        self.items.append(item)
        self.rewire()
    def rewire(self):
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
root = widgets.root.Root(window)


for _ in range(4):
    root.add_column()

# self.streams.resize = omap(self.add_zeropos, parent_streams.window_size)

# we.window_size.subscribe(lambda e: root.fit_to_rect(x=0, y=0, dx=e.dx, dy=e.dy))
# we.draw.subscribe(lambda e: root.draw(e))


"""
widgets = []
rectangle = Rectangle(window, 10, 10, 30, 30, (.5, .5, .5), (1.0, 0, 1.0))
widgets.append(rectangle)
"""



def debug_event(*args, **kwargs):
    print(inspect.stack()[2][3], args, kwargs)

mouse = input_system.mouse.Mouse()
mouse.on_drag_release.append(debug_event)

mc = mouse_controller.MouseController(root, mouse)

@window.event
def on_mouse_motion(x, y, dx, dy):
    pass

@window.event
def on_mouse_press(x, y, buttons, modifiers):
    mouse.press(x, y, buttons, modifiers)

@window.event
def on_mouse_release(x, y, buttons, modifiers):
    mouse.release(x, y, buttons, modifiers)


@window.event
def on_resize(dx, dy):
    root.resize(0,0,dx,dy)



@window.event
def on_draw():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    root.draw()

pyglet.app.run()
