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

class Mouse(object):
    def __init__(self):
        self.press_x = 0
        self.press_y = 0

        self.on_drag_release = Event()

    def press(self, x, y, buttons, modifiers):
        self.press_x = x
        self.press_y = y

    def release(self, x, y, buttons, modifiers):
        self.on_drag_release( self.press_x, self.press_y, x, y)
