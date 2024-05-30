import strawberry
from strawberry.types.nodes import Selection


def get_required_fields(info: strawberry.Info) -> list[Selection]:
    return [f.selections for f in info.selected_fields][0]


def parse_id(id: strawberry.ID | None, to_str: bool = False) -> str | int:
    if to_str:
        return str(id)
    return int(id)
