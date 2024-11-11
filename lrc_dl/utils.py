from typing import Iterator, Optional, TypeVar


def threshold_equal(a: float, b: float, epsilon: float) -> bool:
    return abs(a - b) <= epsilon


T = TypeVar('T')

def next_or_none(iterator: Iterator[T]) -> Optional[T]:
    try:
        return next(iterator)
    except StopIteration:
        return None
