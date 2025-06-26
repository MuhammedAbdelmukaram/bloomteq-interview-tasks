from collections import Counter
from typing import List, Dict, Tuple, Optional


def extract_used_ids_and_values(existing: List[Dict[str, int]]) -> Tuple[set, List[int]]:
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
    Finds the smallest unused positive integer candidate that can be used as a 'value'.

    A candidate is valid if it is not in the value_counter,
    and if there exists at least one smaller number that appears at least twice.

    Returns:
        The valid candidate value if found, otherwise None.
    """
    min_value = 1

    # Determine starting point based on smallest repeated positive value
    for key, value in sorted(value_counter.items()):
        if value >= 2 and key < 1:
            break
        elif value >= 2 and key > 0:
            min_value = key
            break

    # Determine upper bound for candidate range
    max_value = max(value_counter.keys(), default=0)

    if max_value < 0:
        max_value = 1
    else:
        max_value += 1

    # Look for smallest unused candidate starting from min_value
    for candidate in range(min_value, max_value + 1):
        if candidate in value_counter:
            continue

        # Check if a smaller value exists that is repeated
        for value, count in sorted(value_counter.items()):
            if value < candidate and count >= 2:
                return candidate

    return None
