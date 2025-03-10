from datetime import datetime
import re

def parse_datetime(dt_str: str):
    """
    Parse ISO datetime string and remove any timezone,
    ensuring we have a 'naive' datetime.
    Return None if dt_str is None or empty.
    """
    if not dt_str:
        return None

    # Python's fromisoformat() can't handle a trailing 'Z' in older versions,
    # so let's do a quick fix: replace 'Z' with '+00:00'
    dt_str = re.sub(r"Z$", "+00:00", dt_str)

    try:
        dt = datetime.fromisoformat(dt_str)
        # if dt has a tzinfo, strip it
        if dt.tzinfo is not None:
            dt = dt.replace(tzinfo=None)
        return dt
    except ValueError:
        # if fromisoformat fails, you might use dateutil.parser
        # but let's keep it simple here:
        raise ValueError(f"Unable to parse datetime: {dt_str}")
