from transliterate import detect_language, get_available_language_codes, translit


def to_local_script(text, lang, reverse=False):
    """Transliterate into local characters (or reverse)"""
    if lang in get_available_language_codes():
        if reverse:
            if detect_language(text):
                return translit(text, lang, reversed=reverse)
            else:
                return text
        else:
            if not detect_language(text):
                return translit(text, lang, reversed=reverse)
            else:
                return text
    else:
        return text

def detect(text):
    return detect_language(text)
