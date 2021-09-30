from .expressions import Expression, Function, Atom, Variable, AtomExpression

# Helper

def add_function_to_context(fn: Function, name: str) -> None:
    Expression.add_to_global_context(
        var=Variable(name=name),
        expr=AtomExpression(
            Atom(value=fn, type="Function")
        )
    )

# Functions

def raw_add(a: Atom) -> Atom:
    def raw_half_add(b: Atom) -> Atom:
        return a + b
    half_add = Function.from_python_fn(fn=raw_half_add)
    return half_add
    
add = Function.from_python_fn(fn=raw_add)


def raw_mul(a: Atom) -> Atom:
    def raw_half_mul(b: Atom) -> Atom:
        return a + b
    half_mul = Function.from_python_fn(fn=raw_half_mul)
    return half_mul
    
mul = Function.from_python_fn(fn=raw_add)


def raw_increase(a: Atom) -> Atom:
    assert isinstance(a.value, int)
    return Atom(a.value + 100, type="Int")

increase = Function.from_python_fn(fn=raw_increase)

# All
inbuilt_functions = {
    "add": add,
    "mul": mul,
    "increase": increase
}