def test_equal(a, b, message):
    if a == b:
        print message
    else:
        print message, 'failed'


def test_true(a, message):
    if a:
        print message
    else:
        print message, 'failed'


def test_false(a, message):
    if not a:
        print message
    else:
        print message, 'failed'


tests = list()


def test_issubclass():
    class A:
        pass

    class B(A):
        pass

    class C(B):
        pass

    class D:
        pass

    class E(C, D):
        pass

    test_true(issubclass(C, C), 'C is a subclass of C')
    test_true(issubclass(C, B), 'C is a subclass of B')
    test_true(issubclass(C, A), 'C is a subclass of A')
    test_true(issubclass(B, B), 'B is a subclass of B')
    test_true(issubclass(B, A), 'B is a subclass of A')
    test_true(issubclass(A, A), 'A is a subclass of A')

    test_false(issubclass(A, B), 'A is not a subclass of B')
    test_false(issubclass(B, C), 'B is not a subclass of C')

    test_false(issubclass(D, A), 'D is not a subclass of A')
    test_false(issubclass(D, C), 'D is not a subclass of C')

    test_true(issubclass(E, E), 'E is subclass of E')
    test_true(issubclass(E, D), 'E is subclass of D')
    test_true(issubclass(E, C), 'E is subclass of C')
    test_true(issubclass(E, B), 'E is subclass of B')
    test_true(issubclass(E, A), 'E is subclass of A')

tests.append(test_issubclass)


def test_isinstance():
    class A:
        pass

    class B(A):
        pass

    class X:
        pass

    class Y(X):
        pass

    test_true(isinstance(A(), A), 'A() is an instance of A')
    test_true(isinstance(B(), A), 'B() is an instance of A')
    test_true(isinstance(B(), A), 'B() is an instance of B')
    test_false(isinstance(B, B), 'B is not an instance of B')
    test_false(isinstance(B, A), 'B is not an instance of A')
    test_false(isinstance(B(), X), 'B() is not an instance of X')
    test_false(isinstance(B(), Y), 'B() is not an instance of Y')


tests.append(test_isinstance)


for test in tests:
    test()
