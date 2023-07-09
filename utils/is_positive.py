def is_positive(value):
    try:
        value = float(value)
    except (ValueError, TypeError):
        return False
    return value > 0
