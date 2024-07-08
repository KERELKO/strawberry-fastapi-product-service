from typing import NoReturn


def raise_exc(exc: Exception) -> NoReturn:
    raise exc


__all__ = ['raise_exc']
