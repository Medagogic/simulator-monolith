

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


def generate_socketio_openapi_schema(all_handlers: List[Tuple[str, Callable]]) -> Dict:
    openapi_schema = {
        "openapi": "3.0.0",
        "info": {
            "title": "Socket.IO API",
            "version": "1.0.0"
        },
        "paths": {},
        "components": {
            "schemas": {}
        }
    }

    for handler_name, handler_func in all_handlers:
        if handler_name.startswith('on_'):
            # Get parameter information, excluding 'self' and 'sid'
            fullargspec = inspect.getfullargspec(handler_func)
            arg_names = [
                arg for arg in fullargspec.args
                if arg not in ('self', 'sid')  # exclude 'self' and 'sid'
            ]
            arg_annotations = [
                fullargspec.annotations.get(arg, None) for arg in arg_names
            ]

            # Create a path for each Socket.IO event
            event = handler_name[3:]
            parameters = []

            type_hints = get_type_hints(handler_func)
            # Filter out 'self' and 'sid'
            arg_type_hints = {
                arg: hint for arg, hint in type_hints.items()
                if arg not in ('self', 'sid')
            }

            for arg_name, annotation in arg_type_hints.items():
                if annotation is not None and issubclass(annotation, BaseModel):
                    # If it's a Pydantic model, use it for the schema
                    schema = annotation.model_json_schema()
                    param = {
                        "name": arg_name,
                        "in": "query",
                        "required": True,
                        "schema": schema
                    }
                else:
                    # Otherwise, assume it's a simple string parameter
                    param = {
                        "name": arg_name,
                        "in": "query",
                        "required": True,
                        "schema": get_field_info(annotation)
                    }
                parameters.append(param)

            openapi_schema["paths"][f"/{event}"] = {
                "post": {
                    "summary": f"Handle {event} event",
                    "operationId": handler_name,
                    "parameters": parameters,
                    "responses": {
                        "200": {
                            "description": "Successful operation"
                        }
                    }
                }
            }

    return openapi_schema