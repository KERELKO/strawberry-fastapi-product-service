from typing import Generic, TypeVar

import strawberry


Item = TypeVar('Item')


@strawberry.type
class PaginationWindow(Generic[Item]):
    items: list[Item] = strawberry.field(default_factory=list)
    total_items_count: int = strawberry.field(default=0)
