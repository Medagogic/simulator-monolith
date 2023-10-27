from difflib import SequenceMatcher
from enum import Enum
from typing import Generic, Optional, Type, TypeVar

T = TypeVar("T", bound=Enum)
V = TypeVar("V")

class FuzzyEnumMatcher(Generic[T, V]):
    @staticmethod
    def str_to_enum(input_str: str, enum_cls: Type[T]) -> Optional[T]:
        best_match = None
        best_ratio = 0.0

        for enum_item in enum_cls:
            ratio = SequenceMatcher(None, input_str, str(enum_item.value)).ratio()
            if ratio > best_ratio:
                best_ratio = ratio
                best_match = enum_item

        return best_match if best_ratio > 0.9 else None
