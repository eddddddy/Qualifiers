"""
Tests for the decorators in qualifiers.py
"""

import unittest
import random

from qualifiers import qualify, private, protected, public, final


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


@qualify
class E(D):

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


class TestQualifiers(unittest.TestCase):

    def test_simple_visibility(self):
        a = A()
        self.assertRaises(AttributeError, a.private_method)
        self.assertRaises(AttributeError, a.protected_method)
        self.assertEqual(a.public_method(), A.PUBLIC)
        self.assertRaises(AttributeError, a.private_final_method)
        self.assertRaises(AttributeError, a.protected_final_method)
        self.assertEqual(a.public_final_method(), A.PUBLIC_FINAL)

    def test_simple_inheritance(self):
        b = B()
        self.assertRaises(AttributeError, b.base_private)
        self.assertEqual(b.base_protected(), A.PROTECTED)
        self.assertEqual(b.base_public(), A.PUBLIC)
        self.assertRaises(AttributeError, b.base_public_private_method)
        self.assertRaises(AttributeError, b.base_public_protected_method)
        self.assertRaises(AttributeError, b.private_final_method)
        self.assertRaises(AttributeError, b.protected_final_method)
        self.assertEqual(b.public_final_method(), A.PUBLIC_FINAL)

    def test_method_parameters(self):
        c = C()
        self.assertRaises(AttributeError, c.private_method, 2)
        self.assertEqual(c.public_method(kwarg=1), 2)
        self.assertRaises(AttributeError, c.private_method, kwarg=3)
        self.assertEqual(c.public_final_method(4), 6)
        self.assertEqual(c.public_method_multi(1, 2, kwarg1=3), 10)

    def test_simple_final(self):
        self.assertRaises(AttributeError, override_private_final)
        self.assertRaises(AttributeError, override_protected_final)
        self.assertRaises(AttributeError, override_public_final)

    def test_simple_visibility_bypass(self):
        a = A()
        private_method1 = getattr(a, 'private_method')
        private_method2 = a.__class__.__dict__['private_final_method']
        protected_method1 = a.__class__.__dict__['protected_final_method']
        protected_method2 = getattr(a, 'protected_method')
        public_method1 = getattr(a, 'public_method')
        public_method2 = a.__class__.__dict__['public_final_method']
        self.assertRaises(AttributeError, private_method1)
        self.assertRaises(AttributeError, private_method2, a)
        self.assertRaises(AttributeError, protected_method1, a)
        self.assertRaises(AttributeError, protected_method2)
        self.assertEqual(public_method1(), A.PUBLIC)
        self.assertEqual(public_method2(a), A.PUBLIC_FINAL)

    def test_delegation(self):
        d = D()
        self.assertRaises(AttributeError, d.private_to_private)
        self.assertRaises(AttributeError, d.private_to_protected)
        self.assertRaises(AttributeError, d.private_to_public)
        self.assertRaises(AttributeError, d.protected_to_private)
        self.assertRaises(AttributeError, d.protected_to_protected)
        self.assertRaises(AttributeError, d.protected_to_public)
        self.assertEqual(d.public_to_private(), D.PRIVATE)
        self.assertEqual(d.public_to_protected(), D.PROTECTED)
        self.assertEqual(d.public_to_public(), D.PUBLIC)

    def test_parent_delegation(self):
        e = E()
        self.assertRaises(AttributeError, e.base_private_to_private)
        self.assertRaises(AttributeError, e.base_private_to_protected)
        self.assertRaises(AttributeError, e.base_private_to_public)
        self.assertEqual(e.base_protected_to_private(), D.PRIVATE)
        self.assertEqual(e.base_protected_to_protected(), D.PROTECTED)
        self.assertEqual(e.base_protected_to_public(), D.PUBLIC)
        self.assertEqual(e.base_public_to_private(), D.PRIVATE)
        self.assertEqual(e.base_public_to_protected(), D.PROTECTED)
        self.assertEqual(e.base_public_to_public(), D.PUBLIC)
        self.assertRaises(AttributeError, e.base_public_to_private_private)
        self.assertRaises(AttributeError, e.base_public_to_protected_protected)

    def test_qualifier_override(self):
        f = F()
        self.assertRaises(AttributeError, f.private_method)
        self.assertEqual(f.private_method2(), A.PRIVATE)
        self.assertRaises(AttributeError, f.protected_method)
        self.assertEqual(f.protected_method2(), A.PROTECTED)
        self.assertRaises(AttributeError, f.public_method)
        self.assertRaises(AttributeError, f.public_method2)
        self.assertRaises(AttributeError, f.private_method3)
        self.assertRaises(AttributeError, f.protected_method3)
        self.assertEqual(f.public_method3(), A.PUBLIC)

    def test_property(self):
        g = G()
        get = lambda name: getattr(g, name)
        set = lambda name: setattr(g, name, 0)
        dele = lambda name: delattr(g, name)
        self.assertRaises(AttributeError, get, 'y')
        self.assertRaises(AttributeError, set, 'y')
        self.assertRaises(AttributeError, dele, 'y')
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


def main():
    unittest.TestLoader.sortTestMethodsUsing = lambda _, x, y: random.randint(-1, 1)
    unittest.main()


if __name__ == '__main__':
    main()
