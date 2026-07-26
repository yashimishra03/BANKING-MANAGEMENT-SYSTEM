"""
algorithms.py
-------------
Searching and sorting algorithms used by the Banking Management System.

Implemented:
    - merge_sort        -> O(n log n) stable sort, used to sort customers
                            by balance / name for reports
    - binary_search      -> O(log n) search on a sorted list
    - linear_search       -> O(n) baseline search for comparison
"""


def merge_sort(records, key):
    """
    Sorts a list of dicts by `key` using merge sort. O(n log n).
    Returns a new sorted list (does not mutate the input).
    """
    if len(records) <= 1:
        return records[:]

    mid = len(records) // 2
    left = merge_sort(records[:mid], key)
    right = merge_sort(records[mid:], key)

    return _merge(left, right, key)


def _merge(left, right, key):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i][key] <= right[j][key]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


def binary_search(sorted_records, key, target):
    """
    O(log n) search on a list already sorted (ascending) by `key`.
    Returns the matching record or None.
    """
    lo, hi = 0, len(sorted_records) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        val = sorted_records[mid][key]
        if val == target:
            return sorted_records[mid]
        elif val < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return None


def linear_search(records, key, target):
    """O(n) baseline search — useful to show the speed-up BST/binary search gives."""
    for r in records:
        if r[key] == target:
            return r
    return None
