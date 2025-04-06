def parse_available(value):
    """Converte string ou booleano em booleano padrão."""
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() == 'true'
    return False
