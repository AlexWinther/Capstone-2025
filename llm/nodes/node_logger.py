import json
import logging

# --- Error handling and logging decorator ---

logger = logging.getLogger("node_logger")
logger.setLevel(logging.INFO)


def _truncate_value(value, limit=20):
    try:
        serialized = json.dumps(value, default=str)
    except TypeError:
        serialized = str(value)
    return serialized[:limit] + ("..." if len(serialized) > limit else "")


def _truncate_payload(payload, limit=20):
    """Trim each value in payload to the limit for clearer logs."""
    if isinstance(payload, dict):
        return {k: _truncate_value(v, limit) for k, v in payload.items()}
    if isinstance(payload, list):
        return [_truncate_value(v, limit) for v in payload]
    return _truncate_value(payload, limit)


def node_logger(node_name, input_keys=None, output_keys=None):
    """
    Decorator for logging input and output of stategraph agent nodes.
    Args:
        node_name (str): Name of the node for logging.
        input_keys (list, optional): Keys to log from the input state.
        output_keys (list, optional): Keys to log from the output state.
    Returns:
        function: Wrapped function with logging and error handling.
    """

    def decorator(func):
        def wrapper(state):
            logger = logging.getLogger("StategraphAgent")
            # Log input state
            input_payload = (
                {k: state.get(k) for k in input_keys} if input_keys else state
            )
            truncated_input = _truncate_payload(input_payload)
            print(
                f"[{node_name}] Input: {json.dumps(truncated_input, default=str)}"
                if isinstance(truncated_input, (dict, list))
                else f"[{node_name}] Input: {truncated_input}"
            )
            try:
                result = func(state)
                # Log output state
                output_payload = (
                    {k: result.get(k) for k in output_keys} if output_keys else result
                )
                truncated_output = _truncate_payload(output_payload)
                print(
                    f"[{node_name}] Output: {json.dumps(truncated_output, default=str)}"
                    if isinstance(truncated_output, (dict, list))
                    else f"[{node_name}] Output: {truncated_output}"
                )
                return result
            except Exception as e:
                logger.exception(f"[{node_name}] Exception occurred: %s", e)
                state["error"] = str(e)
                return state

        return wrapper

    return decorator
