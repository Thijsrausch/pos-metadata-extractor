def convert_keys_to_string(obj):
    """
    Recursively ensure all dictionary keys are strings.
    Works for nested dicts and lists.
    """
    if isinstance(obj, dict):
        new_dict = {}
        for k, v in obj.items():
            new_dict[str(k)] = convert_keys_to_string(v)
        return new_dict
    elif isinstance(obj, list):
        return [convert_keys_to_string(i) for i in obj]
    else:
        return obj