

import inspect
from typing import Callable, Dict, List, Tuple, get_type_hints
from pydantic import BaseModel


def get_field_info(annotation) -> dict:
    if annotation == int:
        return {"type": "integer"}
    elif annotation == float:
        return {"type": "number"}
    elif annotation == bool:
        return {"type": "boolean"}
    elif annotation == str:
        return {"type": "string"}
    else:
        return {"type": "object"}


def get_sio_data_type(func: Callable) -> Dict[str, type]:
    hints = get_type_hints(func)
    return {
        arg: hints[arg] for arg in hints.keys()
        if arg not in ('self', 'sid')
    }