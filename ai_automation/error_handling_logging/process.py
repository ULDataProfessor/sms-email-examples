from typing import List, Dict

from .utils import ProcessingError


def process_records(records: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """Simple processing step that capitalizes a `name` field."""
    processed = []
    try:
        for rec in records:
            if 'name' not in rec:
                raise ProcessingError("Missing 'name' field")
            processed.append({'name': rec['name'].upper()})
    except Exception as exc:
        raise ProcessingError(str(exc)) from exc
    return processed
