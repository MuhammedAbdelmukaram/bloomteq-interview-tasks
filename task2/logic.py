from typing import Any, Dict


def lookup(obj: Dict, path: str) -> Any:
    """
    Safely looks up a value in a nested dictionary using a dot-separated string path.

    Each segment in the path is used to traverse one level deeper in the nested structure.
    Supports both string and integer keys (when strings can be cast to integers).
    Returns None if the path is invalid or intermediate levels are not dictionaries.

    Args:
        obj: The dictionary to traverse.
        path: Dot-separated string representing the lookup path.

    Returns:
        The value at the end of the path if valid, otherwise None.
    """
    if not isinstance(path, str):
        return None  # Reject non-string path input early

    try:
        for key in path.split("."):
            # If current obj is not a dictionary, stop traversal
            if not isinstance(obj, Dict):
                return None

            # Try to access using string key first
            if key in obj:
                obj = obj[key]
            else:
                # If that fails, try using integer conversion
                try:
                    obj = obj[int(key)]
                except (ValueError, KeyError):
                    return None

        return obj
    except (KeyError, TypeError):
        return None
