__all__ = ["compare_lists"]

from typing import List, Tuple, TypeVar

T = TypeVar('T')

def compare_lists(old: List[T], new: List[T]) -> Tuple[List[T], List[T], List[T]]:
    removed = []
    added = []
    unchanged = []

    obj_set2 = set(new)

    for obj1 in old:
        if obj1 not in obj_set2:
            removed.append(obj1)
        else:
            unchanged.append(obj1)
            obj_set2.remove(obj1)

    added = list(obj_set2)

    return removed, added, unchanged