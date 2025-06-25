from collections import Counter
from typing import List, Dict


def generate_new_entry(existing: List[Dict[str, int]]) -> Dict[str, int]:
    if not existing:
        return {"id": 1, "value": 1}

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

    value_counter = Counter(used_values)

    min_value = 1

    for key, value in sorted(value_counter.items()):
        if value >= 2:
            min_value = key
            break

    max_value = max(used_values)

    if max_value < 0:
        max_value = 1
    else:
        max_value += 1

    for candidate in range(1, max_value + 1):
        if candidate in value_counter:
            continue

        for value, count in sorted(value_counter.items()):
            if value < candidate and count >= 2:
                return {"id": max(used_ids, default=0) + 1, "value": candidate}

    return None
