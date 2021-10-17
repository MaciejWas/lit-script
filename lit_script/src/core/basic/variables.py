from dataclasses import dataclass


@dataclass
class Variable:
    name: str

    def __hash__(self) -> int:
        return hash(self.name)

    def __repr__(self) -> str:
        return f"<Variable {self.name}>"
