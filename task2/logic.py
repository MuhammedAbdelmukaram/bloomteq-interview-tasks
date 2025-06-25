from typing import Any, Dict


def lookup(obj: Dict, path: str) -> Any:
    try:
        for key in path.split("."):
            if not isinstance(obj, Dict):
                return None

            if key in obj:
                obj = obj[key]
            else:
                try:
                    obj = obj[int(key)]
                except(ValueError, KeyError):
                    return None
        return obj
    except(KeyError, TypeError):
        return None
