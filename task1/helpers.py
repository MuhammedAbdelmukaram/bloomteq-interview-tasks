from collections import Counter
from typing import List, Dict, Tuple, Optional, Set


def extract_used_ids_and_values(existing: List[Dict[str, int]]) -> Tuple[Set[int], List[int]]:
    """
    Extracts unique 'id' values and collects all valid 'value' entries from a list of dictionaries.

    Skips any entry that is invalid (not a dict or missing/wrong types for 'id' or 'value'),
    or has a duplicate 'id'.

    Returns:
        A tuple containing:
            - A set of unique ids
            - A list of valid values
    """
    used_ids = set()
    used_values = []

    for entry in existing:
        # Ensure entry is a dictionary
        if not isinstance(entry, Dict):
            continue

        # Check if 'id' is present and is an int
        if "id" not in entry or not isinstance(entry["id"], int):
            continue

        # Check if 'value' is present and is an int
        if "value" not in entry or not isinstance(entry["value"], int):
            continue

        # Skip duplicate ids
        if entry["id"] in used_ids:
            continue

        used_ids.add(entry["id"])
        used_values.append(entry["value"])

    return used_ids, used_values



def find_valid_candidate_value(value_counter: Counter) -> Optional[int]:
    """
    Finds the smallest unused positive integer candidate for 'value'.

    A candidate is valid if:
      1. It is not already in value_counter.keys().
      2. There is at least one repeated entry (count >= 2) anywhere (positive, zero or negative),
         and either:
         • A positive number repeats — start at the smallest positive repeated.
         • Otherwise (only zero/negative repeat) — start at 1.

    Returns:
        The valid candidate if found, otherwise None.
    Time: O(n)    Space: O(n)
    """
    # Build a set of all used values for O(1) lookups
    used_values = set(value_counter.keys())

    # Collect all values that appear >= 2 times
    repeats = []
    for value, count in value_counter.items():
        if count >= 2:
            repeats.append(value)

    # If no repeats at all, no valid candidate
    if not repeats:
        return None

    # Determine starting point: smallest positive repeated, or 1
    start = 1
    for value in repeats:
        if value < 1:
            break
        if value > 0:
            if start == 1 or value < start:
                start = value

    # 3) Determine the upper bound to scan (max + 1, or 1 if all negative)
    if used_values:
        max_val = max(used_values)
    else:
        max_val = 0

    if max_val < 0:
        upper = 1
    else:
        upper = max_val + 1

    # 4) Scan for the first missing candidate in [start..upper]
    for candidate in range(start, upper + 1):
        if candidate in used_values:
            continue
        return candidate

    return None