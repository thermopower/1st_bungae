"""String Utils"""


def truncate(text: str, max_length: int, suffix: str = "...") -> str:
    """
    문자열을 지정된 길이로 자르기

    Args:
        text: 원본 문자열
        max_length: 최대 길이
        suffix: 말줄임표 (기본값: "...")

    Returns:
        잘린 문자열
    """
    if len(text) <= max_length:
        return text
    return text[:max_length] + suffix


def normalize_whitespace(text: str) -> str:
    """
    공백 정규화 (앞뒤 공백 제거, 연속 공백 단일화)

    Args:
        text: 원본 문자열

    Returns:
        정규화된 문자열
    """
    import re

    text = text.strip()
    text = re.sub(r"\s+", " ", text)
    return text
