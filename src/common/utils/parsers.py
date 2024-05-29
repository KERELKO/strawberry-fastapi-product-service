from src.common.base.dto import ID


# TODO: catch specific exception
def parse_id(id: ID) -> str | int:
    try:
        parsed_id = int(id)
    except Exception:
        parsed_id = str(id)
    return parsed_id
