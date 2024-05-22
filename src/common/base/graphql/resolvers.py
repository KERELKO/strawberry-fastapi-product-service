from strawberry.utils.str_converters import to_snake_case
from strawberry.types.nodes import Selection


class BaseStrawberryResolver:
    @classmethod
    async def _get_list_fields(
        cls,
        fields: list[Selection],
        remove_related: bool = True,
    ) -> list[str]:
        list_fields: list[str] = []
        for field in fields:
            if remove_related and field.selections:
                continue
            list_fields.append(to_snake_case(field.name))
        return list_fields
