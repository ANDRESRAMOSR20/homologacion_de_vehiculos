import unicodedata

def remove_accents(text: str) -> str:
    """
    Removes accents from the input text.
    Example: "camión" -> "camion"
    """
    if not text:
        return ""
    return ''.join(c for c in unicodedata.normalize('NFD', text)
                  if unicodedata.category(c) != 'Mn')
