from strawberry.utils.str_converters import to_snake_case
from strawberry.types.nodes import Selection

from src.common.utils.fields import ModelFields


class BaseStrawberryResolver:
    @classmethod
    def _selections_to_strings(
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
                    list_fields.append(f'{field.name}.{related_field.name}')

        # TODO: remove
        print(list_fields)
        return list_fields

    def _selections_to_model_fields(
        cls,
        fields: list[Selection],
        remove_related: bool = True,
    ) -> list[ModelFields]:
        ...
