from typing import Union, Callable, Any
from dataclasses import dataclass

AtomFn = Callable[["Atom"], "Atom"]


@dataclass
class Atom:
    value: Union[int, float, str, AtomFn]
    type: str

    @property
    def is_function(self) -> bool:
        return callable(self.value)

    def __repr__(self) -> str:
        return f"<Atom {self.value} :: {self.type}>"

    def __call__(self, *args, **kwargs) -> "Atom":
        raise Exception(f"You were trying to call an Atom instead of it's value.")

    def __add__(self, other: "Atom") -> "Atom":
        if self.type != other.type:
            raise NotImplementedError("Cant add that m8.")

        if self.type not in ["Int", "Float"]:
            raise NotImplementedError("Cant add that m8.")

        assert isinstance(self.value, (float, int))
        assert isinstance(other.value, (float, int))

        return Atom(value=self.value + other.value, type=self.type)

    def __mul__(self, other: "Atom") -> "Atom":
        if self.type != other.type:
            raise NotImplementedError("Cant mul that m8.")

        if self.type not in ["Int", "Float"]:
            raise NotImplementedError("Cant mul that m8.")

        assert isinstance(self.value, (float, int))
        assert isinstance(other.value, (float, int))

        return Atom(value=self.value * other.value, type=self.type)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Atom):
            return False

        return self.value == other.value  # TODO: Types
