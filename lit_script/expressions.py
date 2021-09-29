from typing import Optional, Any, Callable, Protocol, runtime_checkable
from dataclasses import dataclass

@dataclass
class Value:
    value: Any
    type: str

@dataclass
class Variable:
    name: str


class Expression:

    def resolve(self) -> Value:
        raise NotImplementedError()


