from dataclasses import dataclass, field

from src.common.base.dto import Entity


@dataclass(eq=False)
class SelectedFields:
    owner: Entity | str
    all: bool = False
    fields: list[str] = field(default_factory=list)
