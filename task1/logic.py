from collections import Counter
from typing import List, Dict, Optional
from .helpers import extract_used_ids_and_values, find_valid_candidate_value


def generate_new_entry(existing: List[Dict[str, int]]) -> Optional[Dict[str, int]]:
    if not existing:
        return {"id": 1, "value": 1}

    used_ids, used_values = extract_used_ids_and_values(existing)
    value_counter = Counter(used_values)
    candidate_value = find_valid_candidate_value(value_counter)

    if candidate_value is not None:
        return {"id": max(used_ids, default=0) + 1, "value": candidate_value}

    return None
