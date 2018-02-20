import builtins
import sys
import threading
import types


import operator


class Break(Exception):
    pass


class Continue(Exception):
    pass


def break_():
    raise Break()


def continue_():
    raise Continue()


real_build_class = builtins.__build_class__
_ctx = threading.local()
_ctx.func = None


def my_build_class(func, *args, **kwargs):
    old_func = _ctx.func
    _ctx.func = func
    try:
        return real_build_class(func, *args, **kwargs)
    except Break:
        return None
    finally:
        _ctx.func = old_func


builtins.__build_class__ = my_build_class


class LoopVariable:

    def __init__(self, name, value):
        self.name = name
        self.value = value
        self.condition = None
        self.mutate = None

    @property
    def ready(self):
        return self.condition is not None and self.mutate is not None

    def __pos__(self):
        return IncrementingLoopVariable(self)

    def _cmp(f):
        def method(self, value):
            if self.condition is None:
                def condition():
                    return f(self.value, value)

                if not condition():
                    raise Break()

                self.condition = condition
            else:
                raise AssertionError("Multiple comparisons to loop variable.")
            return True
        return method

    __lt__ = _cmp(operator.lt)
    __le__ = _cmp(operator.le)
    __gt__ = _cmp(operator.gt)
    __ge__ = _cmp(operator.ge)
    __eq__ = _cmp(operator.eq)
    __ne__ = _cmp(operator.ne)


class IncrementingLoopVariable:
    def __init__(self, variable):
        self.variable = variable

    def __pos__(self):
        if self.variable.mutate is None:
            variable = self.variable
            def mutate():
                variable.value += 1
            self.variable.mutate = mutate
        else:
            raise AssertionError("mutated twice")
        return self


class LoopBodyMapping(dict):

    def __init__(self):
        self.variable = None
        self.limit = None
        self.frame = None
        self.closure = None
        self.globals = None

        super().__setitem__('break_', break_)
        super().__setitem__('continue_', continue_)

    @property
    def ready(self):
        return (
            self.variable is not None
            and self.variable.condition is not None
            and self.variable.mutate is not None
        )

    def __setitem__(self, key, value):
        if key in ('__module__', '__qualname__'):
            return

        # The first stored variable in the class body is our loop variable.
        if self.variable is None:
            self.frame = sys._getframe(1)
            self.closure = _ctx.func.__closure__
            self.globals = _ctx.func.__globals__
            self.variable = LoopVariable(key, value)
            return
        elif key == self.variable.name:
            return  # Ignore later assignments.

        super().__setitem__(key, value)

    def __getitem__(self, key):
        if key == '__name__':
            return "For"

        if self.variable is None:
            raise AssertionError(key)

        if key != self.variable.name:
            try:
                return super().__getitem__(key)
            except KeyError:
                try:
                    return self.globals[key]
                except KeyError:
                    return vars(builtins)[key]

        if not self.variable.ready:
            assert key == self.variable.name
            return self.variable
        else:
            return self.variable.value


class LoopMeta(type):
    def __prepare__(name, *args, **kwargs):
        return LoopBodyMapping()

    def __new__(mcls, name, bases, clsdict):
        if name == 'Loop':
            return super().__new__(mcls, name, bases, clsdict)

        var = clsdict.variable
        var.mutate()

        frame = clsdict.frame
        run_frame = types.FunctionType(
            frame.f_code, clsdict, name, (), clsdict.closure,
        )

        while var.condition():
            try:
                run_frame()
            except Continue:
                pass
            var.mutate()


class Loop(metaclass=LoopMeta):
    """
    Usage
    -----
    >>> class For(Loop):
    ...     x = 0; x < 10; ++x
    ...     if x == 5:
    ...         print("Skipping 5")
    ...         continue_()
    ...     print("Body:", x)
    ...
    Body: 0
    Body: 1
    Body: 2
    Body: 3
    Body: 4
    Skipping 5
    Body: 6
    Body: 7
    Body: 8
    Body: 9
    """
