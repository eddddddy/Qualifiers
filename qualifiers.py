"""
This module has not been tested extensively and should only
    be used for simple class hierarchies.
"""

import functools
import inspect


class Visibility:
    PRIVATE = 1
    PROTECTED = 2
    PUBLIC = 3


class AccessError(Exception):
    def __init__(self, message):
        self.message = message


def __get_calling_object(init_frames=3):
    frame = inspect.stack()[0].frame
    count = init_frames
    while 'self' not in frame.f_locals or count > 0:
        frame = frame.f_back
        if frame is None:
            return False
        if 'self' in frame.f_locals:
            count -= 1
    return frame.f_locals['self']


def __get_class_with_method(func):
    if inspect.ismethod(func):
        for cls in inspect.getmro(func.__self__.__class__):
            if cls.__dict__.get(func.__name__) is func:
                return cls
        func = func.__func__
    if inspect.isfunction(func):
        cls = getattr(inspect.getmodule(func),
                      func.__qualname__.split('.<locals>', 1)[0].rsplit('.', 1)[0])
        if isinstance(cls, type):
            return cls
    return getattr(func, '__objclass__', None)


__FUNCS = {}
__FINAL = []
__CLASS = {}


def __new_getattribute(self, name):
    if name in ['__dispatch__', '__class__', '__mro__']:
        return object.__getattribute__(self, name)

    __dispatch = self.__dispatch__ if hasattr(self, '__dispatch__') else self.__class__
    __mro = __dispatch.__mro__
    for __class in __mro:
        if f"{__class.__qualname__}.{name}" in __FUNCS:
            visibility = __FUNCS[f"{__class.__qualname__}.{name}"]
            if visibility in (Visibility.PUBLIC, Visibility.PROTECTED):
                return object.__getattribute__(self, name)
            elif __class is __dispatch:
                return object.__getattribute__(self, name)
            else:
                raise AccessError(f"Attribute {name} is private "
                                  f"in class {__class.__qualname__}")
    return object.__getattribute__(self, name)


def qualify(cls):
    """
    Make a class qualifiable
    """
    dct = dict(cls.__dict__)
    bases = cls.__bases__
    for base_cls in bases:
        for key in base_cls.__dict__:
            if f"{base_cls.__qualname__}.{key}" in __FINAL and key in dct:
                raise AccessError(f"Attribute {key} is final "
                                  f"in class {base_cls.__qualname__}")
    dct['__getattribute__'] = __new_getattribute
    return type(cls.__name__, bases, dct)


def private(func):
    """
    Qualify a method to be private
    """
    __FUNCS[func.__qualname__] = Visibility.PRIVATE

    @functools.wraps(func)
    def __make_private(self, *args, **kwargs):
        __caller = __get_calling_object()
        if not hasattr(__caller, '__dispatch__'):
            raise AccessError(f"Attribute {func.__name__} is private "
                              f"in class {self.__class__.__qualname__}")

        __old_dispatch__ = self.__dispatch__ if hasattr(self, '__dispatch__') else self.__class__
        if func.__qualname__ in __CLASS:
            __dispatch = __CLASS[func.__qualname__]
        else:
            __dispatch = __get_class_with_method(func)
            __CLASS[func.__qualname__] = __dispatch

        if not isinstance(__caller, __dispatch):
            raise AccessError(f"Attribute {func.__name__} is private "
                              f"in class {self.__class__.__qualname__}")

        self.__dispatch__ = __dispatch
        __return = func.__get__(self, type(self))(*args, **kwargs)
        self.__dispatch__ = __old_dispatch__
        return __return

    return __make_private


def protected(func):
    """
    Qualify a method to be protected
    """
    __FUNCS[func.__qualname__] = Visibility.PROTECTED

    @functools.wraps(func)
    def __make_protected(self, *args, **kwargs):
        __caller = __get_calling_object()
        if not hasattr(__caller, '__dispatch__'):
            raise AccessError(f"Attribute {func.__name__} is protected "
                              f"in class {self.__class__.__qualname__}")

        __old_dispatch__ = self.__dispatch__ if hasattr(self, '__dispatch__') else self.__class__
        if func.__qualname__ in __CLASS:
            __dispatch = __CLASS[func.__qualname__]
        else:
            __dispatch = __get_class_with_method(func)
            __CLASS[func.__qualname__] = __dispatch

        if not isinstance(__caller, __dispatch):
            raise AccessError(f"Attribute {func.__name__} is protected "
                              f"in class {self.__class__.__qualname__}")

        self.__dispatch__ = __dispatch
        __return = func.__get__(self, type(self))(*args, **kwargs)
        self.__dispatch__ = __old_dispatch__
        return __return

    return __make_protected


def public(func):
    """
    Qualify a method to be public
    """
    __FUNCS[func.__qualname__] = Visibility.PUBLIC

    @functools.wraps(func)
    def __make_public(self, *args, **kwargs):
        __old_dispatch__ = self.__dispatch__ if hasattr(self, '__dispatch__') else self.__class__
        if func.__qualname__ in __CLASS:
            __dispatch = __CLASS[func.__qualname__]
        else:
            __dispatch = __get_class_with_method(func)
            __CLASS[func.__qualname__] = __dispatch
        self.__dispatch__ = __dispatch
        __return = func.__get__(self, type(self))(*args, **kwargs)
        self.__dispatch__ = __old_dispatch__
        return __return

    return __make_public


def final(func):
    """
    Qualify a method to be final
    """
    __FINAL.append(func.__qualname__)

    @functools.wraps(func)
    def __make_final(self, *args, **kwargs):
        __old_dispatch__ = self.__dispatch__ if hasattr(self, '__dispatch__') else self.__class__
        if func.__qualname__ in __CLASS:
            __dispatch = __CLASS[func.__qualname__]
        else:
            __dispatch = __get_class_with_method(func)
            __CLASS[func.__qualname__] = __dispatch
        self.__dispatch__ = __dispatch
        __return = func.__get__(self, type(self))(*args, **kwargs)
        self.__dispatch__ = __old_dispatch__
        return __return

    return __make_final
