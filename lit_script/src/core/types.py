from dataclasses import dataclass


class LitType:
    pass


@dataclass
class BasicType(LitType):
    type: str


@dataclass
class FunctionType(LitType):
    from_: LitType
    to: LitType
