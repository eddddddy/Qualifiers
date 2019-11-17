"""
This module has not been tested extensively and should only
    be used for simple class hierarchies.
"""

import functools
import string
import random
import inspect


def __random_string():
    return ''.join(random.choices(string.ascii_letters, k=30))


def __caller_has_token(token, init_frames=2):
    frame = inspect.stack()[0].frame
    count = init_frames
    while "self" not in frame.f_locals or count > 0:
        frame = frame.f_back
        if frame is None:
            return False
        if "self" in frame.f_locals:
            count -= 1
    return token in frame.f_locals["self"].__dir__()


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


__PRIVATE = []
__FINAL = []
__CLASS = {}


def __raise_private(base_cls, attr):
    def __do_raise(*args, **kwargs):
        raise AttributeError(f"Attribute {attr} is private "
                             f"in class {base_cls.__qualname__}")

    return __do_raise


def __raise_final(base_cls, attr):
    def __do_raise(*args, **kwargs):
        raise AttributeError(f"Attribute {attr} is final "
                             f"in class {base_cls.__qualname__}")

    return __do_raise


def qualify(cls):
    """
    Make a class qualifiable
    """
    dct = dict(cls.__dict__)
    bases = cls.__bases__
    for base_cls in bases:
        for key in base_cls.__dict__:
            if f"{base_cls.__qualname__}.{key}" in __FINAL and key in dct:
                __raise_final(base_cls, key)()
            if f"{base_cls.__qualname__}.{key}" in __PRIVATE and key not in dct:
                dct[key] = __raise_private(base_cls, key)
    return type(cls.__name__, bases, dct)


def private(func):
    """
    Qualify a method to be private
    """
    token = __random_string()
    __PRIVATE.append(func.__qualname__)

    @functools.wraps(func)
    def __make_private(self, *args, **kwargs):
        setattr(self.__class__, token, 1)
        if not __caller_has_token(token):
            raise AttributeError(f"Attribute {func.__name__} is private "
                                 f"in class {self.__class__.__qualname__}")
        __class = self.__class__
        if func.__qualname__ in __CLASS:
            __base = __CLASS[func.__qualname__]
        else:
            __base = __get_class_with_method(func)
            __CLASS[func.__qualname__] = __base
        self.__class__ = __base
        __return = func.__get__(self, type(self))(*args, **kwargs)
        self.__class__ = __class
        return __return

    return __make_private


def protected(func):
    """
    Qualify a method to be protected
    """
    token = __random_string()

    @functools.wraps(func)
    def __make_protected(self, *args, **kwargs):
        setattr(self.__class__, token, 1)
        if not __caller_has_token(token):
            raise AttributeError(f"Attribute {func.__name__} is protected "
                                 f"in class {self.__class__.__qualname__}")
        __class = self.__class__
        if func.__qualname__ in __CLASS:
            __base = __CLASS[func.__qualname__]
        else:
            __base = __get_class_with_method(func)
            __CLASS[func.__qualname__] = __base
        self.__class__ = __base
        __return = func.__get__(self, type(self))(*args, **kwargs)
        self.__class__ = __class
        return __return

    return __make_protected


def public(func):
    """
    Qualify a method to be public
    """

    @functools.wraps(func)
    def __make_public(self, *args, **kwargs):
        __class = self.__class__
        if func.__qualname__ in __CLASS:
            __base = __CLASS[func.__qualname__]
        else:
            __base = __get_class_with_method(func)
            __CLASS[func.__qualname__] = __base
        self.__class__ = __base
        __return = func.__get__(self, type(self))(*args, **kwargs)
        self.__class__ = __class
        return __return

    return __make_public


def final(func):
    """
    Qualify a method to be final
    """
    __FINAL.append(func.__qualname__)

    @functools.wraps(func)
    def __make_final(self, *args, **kwargs):
        __class = self.__class__
        if func.__qualname__ in __CLASS:
            __base = __CLASS[func.__qualname__]
        else:
            __base = __get_class_with_method(func)
            __CLASS[func.__qualname__] = __base
        self.__class__ = __base
        __return = func.__get__(self, type(self))(*args, **kwargs)
        self.__class__ = __class
        return __return

    return __make_final
