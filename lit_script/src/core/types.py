from dataclasses import dataclass

from .expressions import Variable


class LitType:
    pass


@dataclass
class AtomType(LitType):
    var: Variable


@dataclass
class FunctionType(LitType):
    from_: LitType
    to: LitType
