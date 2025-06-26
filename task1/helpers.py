from collections import Counter
from typing import List, Dict, Tuple, Optional


def extract_used_ids_and_values(existing: List[Dict[str, int]]) -> Tuple[set, List[int]]:
    used_ids = set()
    used_values = []

    for entry in existing:
        if not isinstance(entry, Dict):
            continue
        if "id" not in entry or not isinstance(entry["id"], int):
            continue
        if "value" not in entry or not isinstance(entry["value"], int):
            continue
        if entry["id"] in used_ids:
            continue

        used_ids.add(entry["id"])
        used_values.append(entry["value"])

    return used_ids, used_values


def find_valid_candidate_value(value_counter: Counter) -> Optional[int]:
    min_value = 1

    for key, value in sorted(value_counter.items()):
        if value >= 2:
            min_value = key
            break

    max_value = max(value_counter.keys(), default=0)

    if max_value < 0:
        max_value = 1
    else:
        max_value += 1

    for candidate in range(1, max_value + 1):
        if candidate in value_counter:
            continue

        for value, count in sorted(value_counter.items()):
            if value < candidate and count >= 2:
                return candidate

    return None