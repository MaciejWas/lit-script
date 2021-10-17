from .basic import Atom, Variable
from .functions import Function
from .concrete_expressions import AtomExpression


def raw_decides(a: Atom) -> Atom:
    def raw_inner_decides(b: Atom) -> Atom:
        if a.value == True:
            raw_resulting_fn = lambda c: b
        else:
            raw_resulting_fn = lambda c: c

        resulting_fn = Function.from_python_fn(raw_resulting_fn)

        return Atom(value=resulting_fn, type="Function")

    inner_decides = Function.from_python_fn(raw_inner_decides)
    return Atom(value=inner_decides, type="Function")


decides = Function.from_python_fn(raw_decides)


def raw_add(a: Atom) -> Atom:
    def raw_half_add(b: Atom) -> Atom:
        return a + b

    half_add = Function.from_python_fn(fn=raw_half_add)
    return Atom(value=half_add, type="Function")


add = Function.from_python_fn(fn=raw_add)


def raw_mul(a: Atom) -> Atom:
    print(f"a is {a}")

    def raw_half_mul(b: Atom) -> Atom:
        return a * b

    half_mul = Function.from_python_fn(fn=raw_half_mul)
    return Atom(value=half_mul, type="Function")


mul = Function.from_python_fn(fn=raw_mul)


def raw_increase(a: Atom) -> Atom:
    assert isinstance(a.value, int)
    return Atom(a.value + 100, type="Int")


increase = Function.from_python_fn(fn=raw_increase)


def raw_neg(a: Atom) -> Atom:
    assert isinstance(a.value, int)
    return Atom(-a.value, type="Int")


neg = Function.from_python_fn(fn=raw_neg)


inbuilt_functions = {
    Variable(name="decides"): AtomExpression(atom=Atom(value=decides, type="Function")),
    Variable(name="add"): AtomExpression(atom=Atom(value=add, type="Function")),
    Variable(name="mul"): AtomExpression(atom=Atom(value=mul, type="Function")),
    Variable(name="increase"): AtomExpression(
        atom=Atom(value=increase, type="Function")
    ),
    Variable(name="neg"): AtomExpression(atom=Atom(value=neg, type="Function")),
}
