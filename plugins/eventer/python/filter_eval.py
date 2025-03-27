import datetime
from typing import Any, Dict

VALID_OPERATORS = ["==", "!=", ">", "<", ">=", "<=", "in", "not in"]
VALID_VARIABLES = ["category", "start_time", "end_time", "assigned_users", "name"]


def evaluate_filter_block(block: Dict[str, Any], context: Dict[str, Any]) -> bool:
    """
    Recursively evaluate a filter block, handling:
      - 'and': [ ... ]
      - 'or': [ ... ]
      - A single operator block, e.g. { "==": [ X, Y ] }
    Automatically merges 'rules' and 'conditions' if present.
    """
    # 🛠 Normalize 'rules' + 'conditions' if both present
    if "rules" in block and "conditions" in block:
        merged = {
            "and": [
                block["rules"],
                block["conditions"]
            ]
        }
        return evaluate_filter_block(merged, context)

    # 👇 Or just 'rules' or just 'conditions' (treat them as-is)
    if "rules" in block:
        return evaluate_filter_block(block["rules"], context)
    
    if "conditions" in block:
        return evaluate_filter_block(block["conditions"], context)

    # Is this an 'and' block?
    if "and" in block:
        return all(evaluate_filter_block(sub, context) for sub in block["and"])

    # Is this an 'or' block?
    if "or" in block:
        return any(evaluate_filter_block(sub, context) for sub in block["or"])

    # Otherwise, assume it's a single operator block
    return evaluate_operator(block, context)


def evaluate_operator(operator_block: Dict[str, Any], context: Dict[str, Any]) -> bool:
    """
    Evaluates expressions like { ">": [ "18:00", { "var": "start_time" } ] }
    """
    if len(operator_block) != 1:
        raise ValueError(f"Malformed operator block: {operator_block}")

    op = list(operator_block.keys())[0]
    if op not in VALID_OPERATORS:
        raise ValueError(f"Unsupported operator '{op}'. Must be one of {VALID_OPERATORS}.")

    args = operator_block[op]
    if not isinstance(args, list) or len(args) != 2:
        raise ValueError(f"Operator '{op}' requires exactly two arguments, got: {args}")

    left_raw, right_raw = args

    # Resolve values from context
    left_val = resolve_value(left_raw, context)
    right_val = resolve_value(right_raw, context)

    # Handle datetime.time conversions
    if isinstance(left_val, datetime.datetime):
        left_val = left_val.time()  # Extract time component
    if isinstance(right_val, str):  # Convert "18:00" string to time
        right_val = parse_time_literal(right_val)

    # Perform the comparison (WITHOUT swapping order)
    if op == "==":
        return left_val == right_val
    elif op == "!=":
        return left_val != right_val
    elif op == ">":
        return left_val > right_val
    elif op == "<":
        return left_val < right_val
    elif op == ">=":
        return left_val >= right_val
    elif op == "<=":
        return left_val <= right_val
    elif op == "in":
        return left_val in right_val
    elif op == "not in":
        return left_val not in right_val

    raise ValueError(f"Unhandled operator: {op}")

def resolve_value(raw: Any, context: Dict[str, Any]) -> Any:
    """
    Convert a 'var' reference or literal into a real Python value.
    """
    if isinstance(raw, dict) and "var" in raw:
        var_name = raw["var"]
        return context.get(var_name, None)  # Get actual variable value
    return parse_time_literal(raw)  # Convert time literals

def parse_time_literal(value: Any) -> Any:
    """
    Converts a string like "18:00" into a `datetime.time` object.
    """
    if isinstance(value, str):
        parts = value.split(":")
        if len(parts) == 2 and all(p.isdigit() for p in parts):
            return datetime.time(int(parts[0]), int(parts[1]))
    return value