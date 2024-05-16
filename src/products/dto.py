from dataclasses import dataclass, field


@dataclass
class Review:
    id: int | None = None
    user_id: int | None = None
    text: str = ''


@dataclass
class Product:
    id: int | None = None
    title: str = ''
    description: str = ''
    reviews: list[Review] = field(default_factory=list)
