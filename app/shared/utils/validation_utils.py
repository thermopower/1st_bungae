"""Validation Utils"""

from typing import Any, List


def is_in_range(value: int, min_value: int, max_value: int) -> bool:
    """
    값이 범위 내에 있는지 검사 (경계 포함)

    Args:
        value: 검사할 값
        min_value: 최소값
        max_value: 최대값

    Returns:
        범위 내에 있으면 True, 아니면 False
    """
    return min_value <= value <= max_value


def is_in_list(value: Any, valid_values: List[Any], case_insensitive: bool = False) -> bool:
    """
    값이 리스트에 포함되는지 검사

    Args:
        value: 검사할 값
        valid_values: 유효한 값 리스트
        case_insensitive: 대소문자 무시 여부 (문자열인 경우)

    Returns:
        리스트에 포함되면 True, 아니면 False
    """
    if case_insensitive and isinstance(value, str):
        return value.lower() in [str(v).lower() for v in valid_values]
    return value in valid_values
