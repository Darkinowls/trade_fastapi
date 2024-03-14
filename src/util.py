from dataclasses import dataclass


@dataclass(frozen=True)
class Res:
    __slots__ = ["message"]
    message: any
