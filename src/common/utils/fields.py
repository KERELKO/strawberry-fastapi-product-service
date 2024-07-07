from dataclasses import dataclass, field


@dataclass(eq=False)
class ModelFields:
    model: str
    all: bool = False
    fields: list[str] = field(default_factory=list)
