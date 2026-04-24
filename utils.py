
from typing import Any

ENGL_COLOR='#aa1111'
FR_COLOR='#1111aa'

def getkwarg(kwargs : dict, key: str, default: Any = None, exception: str|None = None, typecheck : type|None = None) -> Any:
    if exception is not None and key not in kwargs:
        raise Exception(exception)
    value = kwargs.get(key) if key in kwargs else default
    if typecheck is not None and not isinstance(value, typecheck):
        raise Exception(f'{value} is not of type {typecheck}')
    return value
