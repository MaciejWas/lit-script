from .expressions import Expression, Function, Atom, Variable, AtomExpression

def add_function_to_context(fn: Function, name: str):
    Expression.context.add_variable(
        var=Variable(name=name),
        expr=AtomExpression(
            Atom(value=fn, type="Function")
        )
    )

def raw_add(a: Atom):
    def raw_half_add(b: Atom) -> Atom:
        return a + b
    half_add = Function.from_python_fn(fn=raw_half_add)
    return half_add
    
add = Function.from_python_fn(fn=raw_add)

def raw_mul(a: Atom):
    def raw_half_mul(b: Atom) -> Atom:
        return a + b
    half_mul = Function.from_python_fn(fn=raw_half_mul)
    return half_mul
    
mul = Function.from_python_fn(fn=raw_add)

inbuilt_functions = {
    "add": add,
    "mul": mul
}