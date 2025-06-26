from collections import Counter
from typing import List, Dict, Optional

from .helpers import extract_used_ids_and_values, find_valid_candidate_value


def generate_new_entry(existing: List[Dict[str, int]]) -> Optional[Dict[str, int]]:
    """
    Generates a new entry with a unique 'id' and the smallest positive integer 'value'
    not already used, but only if a smaller number appears at least twice among existing values.

    Returns None if no such candidate value is found.
    """
    if not existing:
        return {"id": 1, "value": 1}

    # Extract all valid unique IDs and values
    used_ids, used_values = extract_used_ids_and_values(existing)

    # Count occurrences of each value
    value_counter = Counter(used_values)

    # Find a valid candidate value not already used, based on repeat rules
    candidate_value = find_valid_candidate_value(value_counter)

    # Return new entry if a valid candidate was found
    if candidate_value is not None:
        return {
            "id": max(used_ids, default=0) + 1,
            "value": candidate_value
        }

    return None
