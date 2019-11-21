"""
Tests for the decorators in qualifiers.py
"""

import unittest
import random

from qualifiers import qualify, private, protected, public, final, AccessError


@qualify
class A:
    PRIVATE = 1
    PROTECTED = 2
    PUBLIC = 3
    PRIVATE_FINAL = 4
    PROTECTED_FINAL = 5
    PUBLIC_FINAL = 6

    @private
    def private_method(self):
        return A.PRIVATE

    @protected
    def protected_method(self):
        return A.PROTECTED

    @public
    def public_method(self):
        return A.PUBLIC

    @private
    @final
    def private_final_method(self):
        return A.PRIVATE_FINAL

    @protected
    @final
    def protected_final_method(self):
        return A.PROTECTED_FINAL

    @public
    @final
    def public_final_method(self):
        return A.PUBLIC_FINAL

    @private
    def private_method2(self):
        return A.PRIVATE

    @protected
    def protected_method2(self):
        return A.PROTECTED

    @public
    def public_method2(self):
        return A.PUBLIC

    @private
    def private_method3(self):
        return A.PRIVATE

    @protected
    def protected_method3(self):
        return A.PROTECTED

    @public
    def public_method3(self):
        return A.PUBLIC


@qualify
class B(A):

    @public
    def base_private(self):
        return self.private_method()

    @public
    def base_protected(self):
        return self.protected_method()

    @public
    def base_public(self):
        return self.public_method()

    @private
    def base_public_private_method(self):
        return self.public_method()

    @protected
    def base_public_protected_method(self):
        return self.public_method()


@qualify
class C:

    @private
    def private_method(self, arg):
        return arg + 1

    @public
    def public_method(self, kwarg=10):
        return kwarg * 2

    @private
    @final
    def private_final_method(self, kwarg=6):
        return kwarg * 3

    @public
    @final
    def public_final_method(self, arg):
        return arg + 2

    @public
    def public_method_multi(self, arg1, arg2, kwarg1=2, kwarg2=4):
        return arg1 + arg2 + kwarg1 + kwarg2


def override_private_final():
    @qualify
    class D(A):
        def private_final_method(self):
            return A.PRIVATE_FINAL


def override_protected_final():
    @qualify
    class D(A):
        def protected_final_method(self):
            return A.PROTECTED_FINAL


def override_public_final():
    @qualify
    class D(A):
        def public_final_method(self):
            return A.PUBLIC_FINAL


@qualify
class D:
    PRIVATE = 1
    PROTECTED = 2
    PUBLIC = 3
    SUPER = 10

    @private
    def private_method(self):
        return D.PRIVATE

    @protected
    def protected_method(self):
        return D.PROTECTED

    @public
    def public_method(self):
        return D.PUBLIC

    @private
    def private_to_private(self):
        return self.private_method()

    @private
    def private_to_protected(self):
        return self.protected_method()

    @private
    def private_to_public(self):
        return self.public_method()

    @protected
    def protected_to_private(self):
        return self.private_method()

    @protected
    def protected_to_protected(self):
        return self.protected_method()

    @protected
    def protected_to_public(self):
        return self.public_method()

    @public
    def public_to_private(self):
        return self.private_method()

    @public
    def public_to_protected(self):
        return self.protected_method()

    @public
    def public_to_public(self):
        return self.public_method()

    @public
    @final
    def public_dispatcher(self):
        return self.public_dispatch()

    @public
    def public_dispatch(self):
        return D.SUPER

    @public
    @final
    def protected_dispatcher(self):
        return self.protected_dispatch()

    @protected
    def protected_dispatch(self):
        return D.SUPER


@qualify
class E(D):
    SUB = 11

    @public
    def base_private_to_private(self):
        return self.private_to_private()

    @public
    def base_private_to_protected(self):
        return self.private_to_protected()

    @public
    def base_private_to_public(self):
        return self.private_to_public()

    @public
    def base_protected_to_private(self):
        return self.protected_to_private()

    @public
    def base_protected_to_protected(self):
        return self.protected_to_protected()

    @public
    def base_protected_to_public(self):
        return self.protected_to_public()

    @public
    def base_public_to_private(self):
        return self.public_to_private()

    @public
    def base_public_to_protected(self):
        return self.public_to_protected()

    @public
    def base_public_to_public(self):
        return self.public_to_public()

    @private
    def base_public_to_private_private(self):
        return self.public_to_private()

    @protected
    def base_public_to_protected_protected(self):
        return self.public_to_protected()

    @public
    def public_dispatch(self):
        return E.SUB

    @protected
    def protected_dispatch(self):
        return E.SUB


@qualify
class F(A):

    @protected
    @final
    def private_method(self):
        return A.PRIVATE

    @public
    def private_method2(self):
        return A.PRIVATE

    @private
    def protected_method(self):
        return A.PROTECTED

    @public
    @final
    def protected_method2(self):
        return A.PROTECTED

    @private
    @final
    def public_method(self):
        return A.PUBLIC

    @protected
    def public_method2(self):
        return A.PUBLIC

    @private
    def private_method3(self):
        return A.PRIVATE

    @protected
    @final
    def protected_method3(self):
        return A.PROTECTED

    @public
    def public_method3(self):
        return A.PUBLIC


@qualify
class G:
    Y = 2
    Z = 3

    @public
    def __init__(self):
        self.__y = G.Y
        self.__z = G.Z

    @property
    @protected
    def y(self):
        return self.__y

    @y.setter
    @protected
    def y(self, value):
        self.__y = value

    @y.deleter
    @protected
    def y(self):
        del self.__y

    @property
    @public
    def z(self):
        return self.__z

    @z.setter
    @public
    def z(self, value):
        self.__z = value

    @z.deleter
    @public
    def z(self):
        del self.__z


@qualify
class H(G):

    @public
    def base_get_protected(self):
        return self.y

    @public
    def base_set_protected(self, value):
        self.y = value

    @public
    def base_del_protected(self):
        del self.y


@qualify
class I:
    PROTECTED = 1
    PRIVATE = 2

    @public
    def dispatcher1(self):
        return self.protected1()

    @public
    def dispatcher2(self):
        return self.private1()

    @public
    def dispatcher3(self):
        return self.private2()

    @protected
    def protected1(self):
        return I.PROTECTED

    @private
    def private1(self):
        return I.PRIVATE

    @private
    def private2(self):
        return I.PRIVATE


@qualify
class J(I):
    PROTECTED = 3
    PRIVATE = 4

    @protected
    def protected1(self):
        return J.PROTECTED

    @private
    def private1(self):
        return J.PRIVATE


class TestQualifiers(unittest.TestCase):

    def test_simple_visibility(self):
        a = A()
        self.assertRaises(AccessError, a.private_method)
        self.assertRaises(AccessError, a.protected_method)
        self.assertEqual(a.public_method(), A.PUBLIC)
        self.assertRaises(AccessError, a.private_final_method)
        self.assertRaises(AccessError, a.protected_final_method)
        self.assertEqual(a.public_final_method(), A.PUBLIC_FINAL)

    def test_simple_inheritance(self):
        b = B()
        self.assertRaises(AccessError, b.base_private)
        self.assertEqual(b.base_protected(), A.PROTECTED)
        self.assertEqual(b.base_public(), A.PUBLIC)
        self.assertRaises(AccessError, b.base_public_private_method)
        self.assertRaises(AccessError, b.base_public_protected_method)

        # assertRaises doesn't catch exceptions in __getattribute__, so
        # we need to use a context manager
        with self.assertRaises(AccessError):
            b.private_final_method()

        self.assertRaises(AccessError, b.protected_final_method)
        self.assertEqual(b.public_method(), A.PUBLIC)
        self.assertEqual(b.public_final_method(), A.PUBLIC_FINAL)

    def test_method_parameters(self):
        c = C()
        self.assertRaises(AccessError, c.private_method, 2)
        self.assertEqual(c.public_method(kwarg=1), 2)
        self.assertRaises(AccessError, c.private_method, kwarg=3)
        self.assertEqual(c.public_final_method(4), 6)
        self.assertEqual(c.public_method_multi(1, 2, kwarg1=3), 10)

    def test_simple_final(self):
        self.assertRaises(AccessError, override_private_final)
        self.assertRaises(AccessError, override_protected_final)
        self.assertRaises(AccessError, override_public_final)

    def test_simple_visibility_bypass(self):
        a = A()
        private_method1 = getattr(a, 'private_method')
        private_method2 = a.__class__.__dict__['private_final_method']
        protected_method1 = a.__class__.__dict__['protected_final_method']
        protected_method2 = getattr(a, 'protected_method')
        public_method1 = getattr(a, 'public_method')
        public_method2 = a.__class__.__dict__['public_final_method']
        self.assertRaises(AccessError, private_method1)
        self.assertRaises(AccessError, private_method2, a)
        self.assertRaises(AccessError, protected_method1, a)
        self.assertRaises(AccessError, protected_method2)
        self.assertEqual(public_method1(), A.PUBLIC)
        self.assertEqual(public_method2(a), A.PUBLIC_FINAL)

    def test_delegation(self):
        d = D()
        self.assertRaises(AccessError, d.private_to_private)
        self.assertRaises(AccessError, d.private_to_protected)
        self.assertRaises(AccessError, d.private_to_public)
        self.assertRaises(AccessError, d.protected_to_private)
        self.assertRaises(AccessError, d.protected_to_protected)
        self.assertRaises(AccessError, d.protected_to_public)
        self.assertEqual(d.public_to_private(), D.PRIVATE)
        self.assertEqual(d.public_to_protected(), D.PROTECTED)
        self.assertEqual(d.public_to_public(), D.PUBLIC)
        self.assertEqual(d.public_dispatcher(), D.SUPER)
        self.assertEqual(d.protected_dispatcher(), D.SUPER)

    def test_parent_delegation(self):
        e = E()
        self.assertRaises(AccessError, e.base_private_to_private)
        self.assertRaises(AccessError, e.base_private_to_protected)
        self.assertRaises(AccessError, e.base_private_to_public)
        self.assertEqual(e.base_protected_to_private(), D.PRIVATE)
        self.assertEqual(e.base_protected_to_protected(), D.PROTECTED)
        self.assertEqual(e.base_protected_to_public(), D.PUBLIC)
        self.assertEqual(e.base_public_to_private(), D.PRIVATE)
        self.assertEqual(e.base_public_to_protected(), D.PROTECTED)
        self.assertEqual(e.base_public_to_public(), D.PUBLIC)
        self.assertRaises(AccessError, e.base_public_to_private_private)
        self.assertRaises(AccessError, e.base_public_to_protected_protected)
        self.assertEqual(e.public_dispatcher(), E.SUB)
        self.assertEqual(e.protected_dispatcher(), E.SUB)

    def test_qualifier_override(self):
        f = F()
        self.assertRaises(AccessError, f.private_method)
        self.assertEqual(f.private_method2(), A.PRIVATE)
        self.assertRaises(AccessError, f.protected_method)
        self.assertEqual(f.protected_method2(), A.PROTECTED)
        self.assertRaises(AccessError, f.public_method)
        self.assertRaises(AccessError, f.public_method2)
        self.assertRaises(AccessError, f.private_method3)
        self.assertRaises(AccessError, f.protected_method3)
        self.assertEqual(f.public_method3(), A.PUBLIC)

    def test_property(self):
        g = G()
        get = lambda name: getattr(g, name)
        set = lambda name: setattr(g, name, 0)
        dele = lambda name: delattr(g, name)
        self.assertRaises(AccessError, get, 'y')
        self.assertRaises(AccessError, set, 'y')
        self.assertRaises(AccessError, dele, 'y')
        self.assertEqual(g.z, G.Z)
        set('z')
        self.assertEqual(g.z, 0)
        dele('z')
        self.assertRaises(AttributeError, get, 'z')

    def test_parent_property(self):
        h = H()
        self.assertEqual(h.base_get_protected(), G.Y)
        h.base_set_protected(-1)
        self.assertEqual(h.base_get_protected(), -1)
        h.base_del_protected()
        self.assertRaises(AttributeError, h.base_get_protected)

    def test_simple_dispatch(self):
        i = I()
        j = J()
        self.assertEqual(i.dispatcher1(), I.PROTECTED)
        self.assertEqual(i.dispatcher2(), I.PRIVATE)
        self.assertEqual(i.dispatcher3(), I.PRIVATE)
        self.assertEqual(j.dispatcher1(), J.PROTECTED)
        self.assertEqual(j.dispatcher2(), J.PRIVATE)
        self.assertEqual(j.dispatcher3(), I.PRIVATE)


def main():
    unittest.TestLoader.sortTestMethodsUsing = lambda _, x, y: random.randint(-1, 1)
    unittest.main()


if __name__ == '__main__':
    main()
