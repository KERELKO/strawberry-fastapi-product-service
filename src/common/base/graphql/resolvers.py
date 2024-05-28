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
            if remove_related:
                if not field.selections:
                    list_fields.append(to_snake_case(field.name))
            else:
                if not field.selections:
                    list_fields.append(to_snake_case(field.name))
                    continue
                for related_field in field.selections:
                    list_fields.append(f'{field.name}_{related_field.name}')
        return list_fields
